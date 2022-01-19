from enum import Enum
from typing import Awaitable, Callable, List, Optional

from pydantic import AnyHttpUrl, BaseModel

from saleor_app.schemas.core import DomainName
from saleor_app.schemas.webhook import Webhook


class SaleorEventType(str, Enum):
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_CONFIRMED = "ORDER_CONFIRMED"
    ORDER_FULLY_PAID = "ORDER_FULLY_PAID"
    ORDER_UPDATED = "ORDER_UPDATED"
    ORDER_CANCELLED = "ORDER_CANCELLED"
    ORDER_FULFILLED = "ORDER_FULFILLED"
    DRAFT_ORDER_CREATED = "DRAFT_ORDER_CREATED"
    DRAFT_ORDER_UPDATED = "DRAFT_ORDER_UPDATED"
    DRAFT_ORDER_DELETED = "DRAFT_ORDER_DELETED"
    SALE_CREATED = "SALE_CREATED"
    SALE_UPDATED = "SALE_UPDATED"
    SALE_DELETED = "SALE_DELETED"
    INVOICE_REQUESTED = "INVOICE_REQUESTED"
    INVOICE_DELETED = "INVOICE_DELETED"
    INVOICE_SENT = "INVOICE_SENT"
    CUSTOMER_CREATED = "CUSTOMER_CREATED"
    CUSTOMER_UPDATED = "CUSTOMER_UPDATED"
    PRODUCT_CREATED = "PRODUCT_CREATED"
    PRODUCT_UPDATED = "PRODUCT_UPDATED"
    PRODUCT_DELETED = "PRODUCT_DELETED"
    PRODUCT_VARIANT_CREATED = "PRODUCT_VARIANT_CREATED"
    PRODUCT_VARIANT_UPDATED = "PRODUCT_VARIANT_UPDATED"
    PRODUCT_VARIANT_DELETED = "PRODUCT_VARIANT_DELETED"
    PRODUCT_VARIANT_OUT_OF_STOCK = "PRODUCT_VARIANT_OUT_OF_STOCK"
    PRODUCT_VARIANT_BACK_IN_STOCK = "PRODUCT_VARIANT_BACK_IN_STOCK"
    CHECKOUT_CREATED = "CHECKOUT_CREATED"
    CHECKOUT_UPDATED = "CHECKOUT_UPDATED"
    FULFILLMENT_CREATED = "FULFILLMENT_CREATED"
    FULFILLMENT_CANCELED = "FULFILLMENT_CANCELED"
    NOTIFY_USER = "NOTIFY_USER"
    PAGE_CREATED = "PAGE_CREATED"
    PAGE_UPDATED = "PAGE_UPDATED"
    PAGE_DELETED = "PAGE_DELETED"
    PAYMENT_AUTHORIZE = "PAYMENT_AUTHORIZE"
    PAYMENT_CAPTURE = "PAYMENT_CAPTURE"
    PAYMENT_CONFIRM = "PAYMENT_CONFIRM"
    PAYMENT_LIST_GATEWAYS = "PAYMENT_LIST_GATEWAYS"
    PAYMENT_PROCESS = "PAYMENT_PROCESS"
    PAYMENT_REFUND = "PAYMENT_REFUND"
    PAYMENT_VOID = "PAYMENT_VOID"
    SHIPPING_LIST_METHODS_FOR_CHECKOUT = "SHIPPING_LIST_METHODS_FOR_CHECKOUT"
    TRANSLATION_CREATED = "TRANSLATION_CREATED"
    TRANSLATION_UPDATED = "TRANSLATION_UPDATED"


WebHookHandlerSignature = Optional[Callable[[List[Webhook], DomainName], Awaitable]]


class SQSUrl(AnyHttpUrl):
    allowed_schemes = {"awssqs"}


class SQSHandler(BaseModel):
    target_url: SQSUrl
    handler: WebHookHandlerSignature
