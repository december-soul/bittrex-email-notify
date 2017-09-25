# bittrex-email-notify
Short and simple script to notify you via email whenever one of your open orders on Bittrex completes (or gets cancelled).

## Usage
Create a `secret.py` file in the same folder and declare the following variables:

```python
BITTREX_KEY = 'bittrex api key here'
BITTREX_SECRET = 'bittrex secret key here'

EMAIL_HOST = 'mail.gmx.net'
EMAIL_USER = 'MyUsername'
EMAIL_PASS = 'MyPass'

EMAIL_FROM = 'myemail@gmx.de'
EMAIL_TO = 'myinform@gmx.de'
```

Run the script with `python notifications.py`.
