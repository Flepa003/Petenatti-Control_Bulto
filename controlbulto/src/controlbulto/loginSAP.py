import http.client
import json
import ssl
import codecs
import base64

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

        
    def login_to_sap_b1(company_db, username, password):
        # Defino vble para retornar
        session_id = None
        error_code = None
        error_msg = None
        # Conexion HTTP
        conn = http.client.HTTPSConnection("192.168.220.161", 50000)
        payload = json.dumps({
            "CompanyDB": company_db,
            "UserName": username,
            "Password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/b1s/v1/Login", payload, headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode('utf-8'))
        try:
            session_id = json_data['SessionId']
            # print(session_id)
            return session_id
        except Exception as e:
            error_code = json_data['error']['code']
            error_msg = json_data['error']['message']['value']
            # print(error_msg)
            return None

