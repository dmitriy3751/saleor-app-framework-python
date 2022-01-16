import warnings
from typing import Awaitable, Callable, Optional

from fastapi import APIRouter, Depends, FastAPI
from fastapi.routing import APIRoute

from saleor_app.deps import verify_saleor_domain, verify_webhook_signature
from saleor_app.endpoints import handle_webhook, install, manifest
from saleor_app.errors import ConfigurationError
from saleor_app.http import WebhookRoute
from saleor_app.schemas.core import DomainName, WebhookData
from saleor_app.schemas.handlers import SQSHandlers, WebhookHandlers
from saleor_app.schemas.manifest import Manifest
from saleor_app.settings import SaleorAppSettings


class SaleorApp(FastAPI):
    def __init__(
        self,
        *,
        manifest: Manifest,
        validate_domain: Callable[[DomainName], Awaitable[bool]],
        save_app_data: Callable[[DomainName, WebhookData], Awaitable],
        get_webhook_details: Callable[[DomainName], Awaitable[WebhookData]],
        app_settings: SaleorAppSettings,
        http_webhook_handlers: Optional[WebhookHandlers] = None,
        sqs_handlers: Optional[SQSHandlers] = None,
        use_insecure_saleor_http: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.manifest = manifest
        self.http_webhook_handlers = http_webhook_handlers
        self.sqs_handlers = sqs_handlers

        if not isinstance(app_settings, SaleorAppSettings):
            raise ConfigurationError(
                "app_settings must inherit from saleor_app.settings.SaleorAppSettings"
            )

        self.app_settings = app_settings
        if self.sqs_handlers:
            warnings.simplefilter("always", RuntimeWarning)
            warnings.warn(
                "SQS support is highly experimental, be warned!",
                category=RuntimeWarning,
            )
            if not app_settings.aws:
                raise ConfigurationError(
                    "To leverage SQS webhook handlers you must provide settings.aws"
                )

        self.validate_domain = validate_domain
        self.save_app_data = save_app_data
        self.get_webhook_details = get_webhook_details

        self.use_insecure_saleor_http = use_insecure_saleor_http

        self.configuration_router = APIRouter(
            prefix="/configuration", tags=["configuration"]
        )
        if self.http_webhook_handlers:
            self.include_webhook_router()

    def include_saleor_app_routes(self):
        self.configuration_router.get(
            "/manifest", response_model=Manifest, name="manifest"
        )(manifest)
        self.configuration_router.post(
            "/install",
            responses={
                400: {"description": "Missing required header"},
                403: {"description": "Incorrect token or not enough permissions"},
            },
            name="app-install",
        )(install)

        self.include_router(self.configuration_router)

    def include_webhook_router(self):
        router = APIRouter(
            prefix="/webhook",
            responses={
                400: {"description": "Missing required header"},
                401: {"description": "Incorrect signature"},
                404: {"description": "Incorrect saleor event"},
            },
            dependencies=[
                Depends(verify_saleor_domain),
                Depends(verify_webhook_signature),
            ],
            route_class=WebhookRoute,
        )

        router.post("", name="handle-webhook")(handle_webhook)
        self.webhook_handler_routes = {
            name: APIRoute(
                "",
                handler,
            )
            for name, handler in self.http_webhook_handlers
            if handler
        }
        self.include_router(router)
