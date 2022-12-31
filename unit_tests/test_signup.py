from unit_tests.BaseCase import BaseCase, User, Bookmark
import json
import json

class SignUp(BaseCase):


    def test_sign_up(self):
        payload = json.dumps({
            "email":"nelsond153306@email.com",
            "password":"mypass"
        })
        headers = {
            "Content-Type":"application/json"
        }
        response = self.app.post('http://127.0.0.1:5000/users', headers = headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual(json.loads(payload)['email'], response.get_json()['email'])
        
        payload = json.dumps({
            "email":"example@email.com",
            "password":"mypass2"
        })
        headers = {
            "Content-Type":"application/json"
        }
        response = self.app.post('http://127.0.0.1:5000/users', headers = headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual(json.loads(payload)['email'], response.get_json()['email'])
    
        
        

