from unit_tests.BaseCase import BaseCase, User, Bookmark
import json
import base64



class GetUser(BaseCase):
    """ Create a a user, get the user a token, then look up the user """
    def test_get_user(self):
        email = "nelsond@email.com"
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
        user_id = response.get_json()['id']
        
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
        
        token = response.get_json()['token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        #then get the user using the token
        response = self.app.get('http://127.0.0.1:5000/users/'+str(user_id), headers = headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(user_id,response.get_json()['id'] )

        
        