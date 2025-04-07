import requests
import pyotp
from config import KITE_USERNAME, KITE_PASSWORD, KITE_TOTP_KEY

class ZerodhaLogin:
    def __init__(self):
        """Initialize session and login variables"""
        self.session = requests.Session()
        self.enctoken = None

    def login(self):
        """Performs login and two-factor authentication"""
        try:
            # Step 1: Login Request
            res1 = self.session.post(
                'https://kite.zerodha.com/api/login', 
                data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"}
            )
            login_res = res1.json()
            
            if 'data' not in login_res or 'request_id' not in login_res['data']:
                raise Exception(f"Login failed: {login_res.get('message', 'Unknown error')}")

            # Step 2: Two-Factor Authentication
            return self._twofa_auth(login_res['data']['request_id'], login_res['data']['user_id'])

        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def _twofa_auth(self, request_id, user_id):
        """Handles two-factor authentication"""
        try:
            final_res = self.session.post(
                'https://kite.zerodha.com/api/twofa',
                data={
                    "request_id": request_id,
                    "twofa_value": pyotp.TOTP(KITE_TOTP_KEY).now(),
                    "user_id": user_id,
                    "twofa_type": "totp"
                }
            )
            final_res_json = final_res.json()

            if 'status' not in final_res_json or final_res_json['status'] != 'success':
                raise Exception(f"2FA failed: {final_res_json.get('message', 'Unknown error')}")

            # Step 3: Extract enctoken
            self.enctoken = self.session.cookies.get_dict().get('enctoken')

            if not self.enctoken:
                raise Exception("Failed to retrieve enctoken.")

            return self.enctoken

        except Exception as e:
            print(f"Error during two-factor authentication: {e}")
            return None

    def get_enctoken(self):
        """Returns the stored enctoken after successful login"""
        return self.enctoken
