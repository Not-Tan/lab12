import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class CurrencyConversionTools:
    
    def __init__(self):
        self.api_key = os.getenv("EXCHANGE_API_KEY")
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/"

    def get_all_currencies(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("API key not configured")
        
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/codes"
        response = requests.get(url)
        data = response.json()
        
        if data['result'] != 'success':
            raise ValueError("Error fetching currency codes")
        
        return { code: name for code, name in data['supported_codes'] }
    
    def get_exchange_rates(self, from_currency: str) -> List[Dict[str, Any]]:
        if not self.api_key:
            raise ValueError("API key not configured")
        
        url = f"{self.base_url}{from_currency}"
        response = requests.get(url)
        data = response.json()
        
        if data['result'] != 'success':
            raise ValueError("Error fetching exchange rates")
        
        rates = data['conversion_rates']
        

        return [ {
                  "from_currency": from_currency, 
                  "rates": rates
                  }
            ]
    
    def convert_currency(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        rates = self.get_exchange_rates(from_currency)[0]['rates']
        
        if to_currency not in rates:
            raise ValueError(f"Conversion rate for {to_currency} not found")
        
        converted_amount = amount * rates[to_currency]
        
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "original_amount": amount,
            "converted_amount": converted_amount,
            "rate": rates[to_currency]
        }