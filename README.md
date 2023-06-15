[![PyPI version](https://img.shields.io/pypi/v/XoxoDay.svg)](https://pypi.python.org/pypi/XoxoDay)

# XoxoDay Api Client Python PyPackage

XoxoDay Api Client is a Python library to access services quickly.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install XoxoDay
```
## Environment Variables

```bash
XOXODAY_ENV = 'dev|prod'
XOXODAY_ACCESS_TOKEN = 'access_token'
XOXODAY_REFRESH_TOKEN = 'refresh_token'
XOXODAY_CLIENT_ID = 'client_id'
XOXODAY_CLIENT_SECRET = 'client_secret'
```
### Note
If you don't want to set this variables from global environment you can pass them to class.
You can see usage below
## Usage

```python
from XoxoDay import XoxoDayService

kwargs = {
    # you can also set XoxoDay environment from environment.
    'environment': 'dev|prod',  # Default value : dev
    'access_token': 'XoxoDay Access Token',  # Default value : None
    'refresh_token': 'XoxoDay Refresh Token',  # Default value : None
    'client_id': 'XoxoDay Client Id',  # Default value : None
    'client_secret': 'XoxoDay Client Secret',  # Default value : None
}
# Initialize client with
XoxoDay_service = XoxoDayService()
# or XoxoDay_service = XoxoDayService(**kwargs)

# Get Vouchers
#filters = [{"key": "productName", "value": "Paypal International"}]
#includeProducts= "productId"
funding_source = XoxoDay_service.getVouchers(filters=None, includeProducts=None)

# Place Order
order = XoxoDay_service.placeOrder(email="xoxo@mail.com",  productId='productId', denomination='amount', poNumber="Unique Number for Order")

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
