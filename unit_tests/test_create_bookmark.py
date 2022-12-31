from unit_tests.BaseCase import BaseCase, User, Bookmark
import json
import base64

class CreateBookmark(BaseCase):
    """ Create a user, get a token for the user, then create a bookmark """
    def test_create_bookmark(self):
        email = "email@email.com"
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
        
        #set up to get the token by encoding credentials
        credentials = f'{email}:{password}'.encode('utf-8')
        encoded = base64.b64encode(credentials).decode('utf-8')
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + encoded
        }
       
        response = self.app.post('http://127.0.0.1:5000/tokens', headers = headers)
        self.assertEqual(200, response.status_code)
        
        token = response.get_json()['token']

        #create a bookmark
        url = "https://ndufitimana.github.io/"
        headline = "Test Headline"
        payload = json.dumps({
            "url":url,
            "headline":headline
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        
       
        response = self.app.post('http://127.0.0.1:5000/bookmark', headers = headers, data = payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual(url, response.get_json()['bookmark_url'])
        
        #test invalid url
        url = "example.com" #invalid
        headline = "Test Invalid Url"
        payload = json.dumps({
            "url":url,
            "headline":headline
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        
       
        response = self.app.post('http://127.0.0.1:5000/bookmark', headers = headers, data = payload)
        self.assertEqual(400, response.status_code)
        
        

        
        