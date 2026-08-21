import base64
import datetime
from django.conf import settings
import requests


class MpesaAPI:
    """M-Pesa Daraja API Integration"""
    
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.shortcode = settings.MPESA_SHORTCODE
        self.environment = settings.MPESA_ENVIRONMENT
        
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def get_access_token(self):
        """Get M-Pesa API access token"""
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        
        auth = base64.b64encode(
            f'{self.consumer_key}:{self.consumer_secret}'.encode()
        ).decode()
        
        headers = {
            'Authorization': f'Basic {auth}',
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")
    
    def generate_password(self):
        """Generate password for M-Pesa API"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f'{self.shortcode}{self.passkey}{timestamp}'
        password = base64.b64encode(password_str.encode()).decode()
        return password, timestamp
    
    def initiate_stk_push(self, phone_number, amount, callback_url, account_reference=None):
        """Initiate STK Push for customer payment"""
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()
        
        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': self.shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': callback_url,
            'AccountReference': account_reference or 'LiamTraders',
            'TransactionDesc': 'Payment to Liam Traders',
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to initiate STK push: {str(e)}")
    
    def initiate_b2c_payment(self, phone_number, amount, callback_url, command_id='SalaryPayment'):
        """Initiate B2C payment (withdrawal)"""
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()
        
        url = f'{self.base_url}/mpesa/b2c/v1/paymentrequest'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'InitiatorName': 'testapi',
            'SecurityCredential': password,
            'CommandID': command_id,
            'Amount': amount,
            'PartyA': self.shortcode,
            'PartyB': phone_number,
            'Remarks': 'Withdrawal from Liam Traders',
            'QueueTimeOutURL': callback_url,
            'ResultURL': callback_url,
            'Occasion': 'Withdrawal',
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to initiate B2C payment: {str(e)}")
    
    def check_transaction_status(self, transaction_id):
        """Check transaction status"""
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()
        
        url = f'{self.base_url}/mpesa/transactionstatus/v1/query'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'Initiator': 'testapi',
            'SecurityCredential': password,
            'CommandID': 'TransactionStatusQuery',
            'TransactionID': transaction_id,
            'PartyA': self.shortcode,
            'IdentifierType': '4',
            'ResultURL': 'https://yourdomain.com/mpesa/callback',
            'QueueTimeOutURL': 'https://yourdomain.com/mpesa/callback',
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to check transaction status: {str(e)}")
