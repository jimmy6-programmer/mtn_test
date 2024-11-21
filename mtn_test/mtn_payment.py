# my_app/mtn_payment.py
import requests

class MTNMoMoPayment:
    def __init__(self, api_key, subscription_key, user_id):
        self.api_key = api_key
        self.subscription_key = subscription_key
        self.user_id = user_id
        self.base_url = "https://sandbox.momodeveloper.mtn.com"  # Use production URL for live payments

    def get_access_token(self):
        url = f"{self.base_url}/collection/token/"
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Authorization": f"Basic {self.api_key}",
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")

    def initiate_payment(self, phone_number, amount, transaction_id):
        token = self.get_access_token()
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": transaction_id,
            "X-Target-Environment": "sandbox",  # Change to "mtnlive" for production
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }
        data = {
            "amount": str(amount),
            "currency": "EUR",
            "externalId": transaction_id,
            "payer": {"partyIdType": "MSISDN", "partyId": phone_number},
            "payerMessage": "Ticket Payment",
            "payeeNote": "Thank you for your payment",
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.status_code == 202
