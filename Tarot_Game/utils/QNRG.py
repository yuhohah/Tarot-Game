import os
from dotenv import load_dotenv
import requests
import json

class QNRG:
    def __init__(self):
        load_dotenv()
        self.api_url = os.getenv("API_URL")
        self.api_key = os.getenv("QUANTUM_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "x-id-api-key": self.api_key
        }

    def _fetch_from_api(self, amount, bits_per_block = 8):
        data = {
            "encoding": "raw",
            "format": "decimal",
            "bits_per_block": bits_per_block,
            "number_of_blocks": amount
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)

            if response.status_code == 200:
                result = response.json()
                decimal_numbers = self._decimal_list(result.get('random_numbers', []))
                return decimal_numbers
            else:
                return None
        except Exception as e:
            return None
    
    def _decimal_list(self, random_numbers):
        return [int(block['decimal']) for block in random_numbers]

    