from unit_tests.BaseCase import BaseCase, User, Bookmark
import json
import base64

class GetToken(BaseCase):
    def test_get_token(self):
        email = "nelsond153306@email.com"
        password = "mypass"
        payload = json.dumps({
            "email":email,
            "password":password
        })
        headers = {
            "Content-Type":"application/json"
        }
         #first create the user, then get a token for the user
        response = self.app.post('http://127.0.0.1:5000/users', headers = headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual(json.loads(payload)['email'], response.get_json()['email'])
        
        #set up to get the token
        credentials = f'{email}:{password}'.encode('utf-8')

        #encode the credentials
        encoded = base64.b64encode(credentials).decode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + encoded
        }
       
        response = self.app.post('http://127.0.0.1:5000/tokens', headers = headers)
        self.assertEqual(200, response.status_code)

        
        