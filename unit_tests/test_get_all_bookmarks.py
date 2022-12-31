from unit_tests.BaseCase import BaseCase, User, Bookmark
import json
import base64

class GetAllBookmarks(BaseCase):
    """ Create a user, get a token for the user, create 2 bookmark, get all the bookmarks """
    def test_get_all_bookmarks(self):
        email = "email@email.com"
        password = "mypass2"
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
        url1 = "https://ndufitimana.github.io/"
        headline = "Test Headline"
        payload = json.dumps({
            "url":url1,
            "headline":headline
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        
       
        response = self.app.post('http://127.0.0.1:5000/bookmark', headers = headers, data = payload)
        self.assertEqual(201, response.status_code)
        
          #create a bookmark
        url2 = "https://docs.python.org/3/library/unittest.html"
        headline = "Test Headline 2"
        payload = json.dumps({
            "url":url2,
            "headline":headline
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        
       
        response = self.app.post('http://127.0.0.1:5000/bookmark', headers = headers, data = payload)
        self.assertEqual(201, response.status_code)
        
       #user should have 2 bookmarks. 
       
        response = self.app.get('http://127.0.0.1:5000/users/'+str(user_id), headers = headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.get_json()['bookmark_count'], 2 )
        
    
        # #get all the bookmark
        bookmark_id = response.get_json()['id']
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        
        response = self.app.get('http://127.0.0.1:5000/bookmarks', headers = headers)
        self.assertEqual(200, response.status_code)
        bookmarks = response.get_json()['bookmarks']
        self.assertEqual(len(bookmarks), 2)
        self.assertEqual(bookmarks[1]["bookmark_url"], url2 )
        self.assertEqual(bookmarks[0]["bookmark_url"], url1 )
        
        