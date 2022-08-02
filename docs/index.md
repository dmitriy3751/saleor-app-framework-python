# Welcome to Saleor App Framework 

You are reading the Saleor App Framework (Python) documentation. This document should help you to quickly bootstrap a 3rd Party Saleor App, read more about those [:saleor-saleor: Saleor's documentation](https://docs.saleor.io/docs/3.0/developer/extending/apps/key-concepts){ target=_blank }.

The only supported web framework is **FastAPI**.

## Quickstart

### Install the framework

Using Poetry (recommended, [:material-file-link: installing poetry](https://python-poetry.org/docs/#installation){ target=_blank }):

```bash
poetry add git+https://github.com/mirumee/saleor-app-framework-python.git@main
# (1)
```

1. Not on PyPi yet, you must install from git
   
Using Pip:

```bash
pip install git+https://github.com/mirumee/saleor-app-framework-python.git@main 
```

### Create the Saleor app

To run your Saleor App you can use the ```#!python SaleorApp``` class which overloads the usual ```#!python FastAPI``` class.

```python linenums="1"
from saleor_app.app import SaleorApp

app = SaleorApp(
    # more arguments to come
)
```

You can use the ```#!python app``` instance as you would normally use the standard one, i.e. to initialize Sentry or add Middleware. None of the core FastAPI logic is changed by the framework.

#### Manifest

As described in [:saleor-saleor: App manifest](https://docs.saleor.io/docs/3.0/developer/extending/apps/manifest){ target=_blank } an app needs a manifest, the framework provides a Pydantic representation of that which needs to be provided when initializing the app.

```python linenums="1" hl_lines="2-3 6-18 22"
from saleor_app.app import SaleorApp
from saleor_app.schemas.manifest import Manifest
from saleor_app.schemas.utils import LazyUrl


manifest = Manifest(
    name="Sample Saleor App",
    version="0.1.0",
    about="Sample Saleor App seving as an example.",
    data_privacy="",
    data_privacy_url="http://samle-saleor-app.example.com/dataPrivacyUrl",
    homepage_url="http://samle-saleor-app.example.com/homepageUrl",
    support_url="http://samle-saleor-app.example.com/supportUrl",
    id="saleor-simple-sample",
    permissions=["MANAGE_PRODUCTS", "MANAGE_USERS"],
    configuration_url=LazyUrl("configuration-form"),
    extensions=[],
)


app = SaleorApp(
    manifest=manifest,
    # more arguments to come
)
```

??? info "LazyUrl"

    ```#!python saleor_app.schemas.utils.LazyUrl``` is a lazy loader for app url paths, when a manifest is requested the app will resolve the path name to a full url of that endpoint.

#### Validate Domain

3rd Patry Apps work in a multi-tenant fashion - one app service can serve multiple Saleor instances. To prevent any Saleor instance from using your app the app need to authorize a Saleor instance that's done by a simple function that can be as simple as comparing the incoming Saleor domain or as complex to check the allowed domains in a database.

```python linenums="1" hl_lines="2 7-8 28"
from saleor_app.app import SaleorApp
from saleor_app.schemas.core import DomainName
from saleor_app.schemas.manifest import Manifest
from saleor_app.schemas.utils import LazyUrl


async def validate_domain(saleor_domain: DomainName) -> bool:
    return saleor_domain == "172.17.0.1:8000"


manifest = Manifest(
    name="Sample Saleor App",
    version="0.1.0",
    about="Sample Saleor App seving as an example.",
    data_privacy="",
    data_privacy_url="http://samle-saleor-app.example.com/dataPrivacyUrl",
    homepage_url="http://samle-saleor-app.example.com/homepageUrl",
    support_url="http://samle-saleor-app.example.com/supportUrl",
    id="saleor-simple-sample",
    permissions=["MANAGE_PRODUCTS", "MANAGE_USERS"],
    configuration_url=LazyUrl("configuration-form"),
    extensions=[],
)


app = SaleorApp(
    manifest=manifest,
    validate_domain=validate_domain,
    # more arguments to come
)
```


#### Saving Application Data

When Saleor is authorized to install the app an authentication key is issued, that key needs to be securely stored by the app as it provides as much access as the app requested in the manifest.

```python linenums="1" hl_lines="2 11-17 39"
from saleor_app.app import SaleorApp
from saleor_app.schemas.core import DomainName, WebhookData
from saleor_app.schemas.manifest import Manifest
from saleor_app.schemas.utils import LazyUrl


async def validate_domain(saleor_domain: DomainName) -> bool:
    return saleor_domain == "172.17.0.1:8000"


async def store_app_data(
    saleor_domain: DomainName, auth_token: str, webhook_data: WebhookData
):
    print("Called store_app_data")
    print(saleor_domain)
    print(auth_token)
    print(webhook_data) #



manifest = Manifest(
    name="Sample Saleor App",
    version="0.1.0",
    about="Sample Saleor App serving as an example.",
    data_privacy="",
    data_privacy_url="http://sample-saleor-app.example.com/dataPrivacyUrl",
    homepage_url="http://sample-saleor-app.example.com/homepageUrl",
    support_url="http://sample-saleor-app.example.com/supportUrl",
    id="saleor-simple-sample",
    permissions=["MANAGE_PRODUCTS", "MANAGE_USERS"],
    configuration_url=LazyUrl("configuration-form"),
    extensions=[],
)


app = SaleorApp(
    manifest=manifest,
    validate_domain=validate_domain,
    save_app_data=store_app_data, # (1)
)
```

1. :material-database: Typically, you'd store all the data passed to this function to a DB table


#### Configuration URL

To finalize, you need to provide the endpoint named ```#!python configuration-form``` specified in the [#Manifest](#manifest).

```python linenums="1" hl_lines="1 3-4 8 48-100"
import json

from fastapi.param_functions import Depends
from fastapi.responses import HTMLResponse, PlainTextResponse

from saleor_app.app import SaleorApp
from saleor_app.deps import ConfigurationFormDeps
from saleor_app.schemas.core import DomainName, WebhookData
from saleor_app.schemas.manifest import Manifest
from saleor_app.schemas.utils import LazyUrl


async def validate_domain(saleor_domain: DomainName) -> bool:
    return saleor_domain == "172.17.0.1:8000"


async def store_app_data(
    saleor_domain: DomainName, auth_token: str, webhook_data: WebhookData
):
    print("Called store_app_data")
    print(saleor_domain)
    print(auth_token)
    print(webhook_data) 


manifest = Manifest(
    name="Sample Saleor App",
    version="0.1.0",
    about="Sample Saleor App seving as an example.",
    data_privacy="",
    data_privacy_url="http://samle-saleor-app.example.com/dataPrivacyUrl",
    homepage_url="http://samle-saleor-app.example.com/homepageUrl",
    support_url="http://samle-saleor-app.example.com/supportUrl",
    id="saleor-simple-sample",
    permissions=["MANAGE_PRODUCTS", "MANAGE_USERS"],
    configuration_url=LazyUrl("configuration-form"),
    extensions=[],
)


app = SaleorApp(
    manifest=manifest,
    validate_domain=validate_domain,
    save_app_data=store_app_data,
)


@app.configuration_router.get(
    "/", response_class=HTMLResponse, name="configuration-form"
)
async def get_public_form(commons: ConfigurationFormDeps = Depends()):
    context = {
        "request": str(commons.request),
        "form_url": str(commons.request.url),
        "saleor_domain": commons.saleor_domain,
    }
    return PlainTextResponse(json.dumps(context, indent=4)) # (1)


app.include_saleor_app_routes() # (2)
```

1. This view would normally return a UI that will be rendered in the Dashboard
1. Once you are done defining all the configuration routes you need to tell the app to load them

> This is a complete example that will work as is.

!!! warning "Remember about `app.include_saleor_app_routes()`"

### Running the App

To run the app you can save the above example in `simple_app/app.py` and run it with:

```bash
uvicorn simple_app.app:app --host 0.0.0.0 --port 5000 --reload
```

Or create a `simple_app/__main__.py` with:

```python linenums="1" 
import uvicorn


def main():
    uvicorn.run(
        "simple_app.app:app", host="0.0.0.0", port=5000, debug=True, reload=True
    )


if __name__ == "__main__":
    main()
```

and run the module as a script with Python's `-m` flag:

```bash
python -m simple_app
```

## Examples

Visit the [:material-github: Samples directory](https://github.com/saleor/saleor-app-framework-python/tree/main/samples){ target=_blank } to check apps that were built as examples of how the framework can be used.
