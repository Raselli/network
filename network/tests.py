from django.test import Client, TestCase
import unittest
from .models import User, Profile, Post
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.test import Client
from django.test.client import Client
from django.contrib import auth
from .views import PostForm

csrf_client = Client(enforce_csrf_checks=True)


# Test GET responses
class WebpageTestsGet(unittest.TestCase):
    
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        
    def test_edit(self):
        c = Client()
        response = c.get("/edit")
        self.assertEqual(response.status_code, 302)
        
    def test_like(self):
        c = Client()
        response = c.get("/like")
        self.assertEqual(response.status_code, 302)

    def test_follow(self):
        c = Client()
        response = c.get("/follow")
        self.assertEqual(response.status_code, 302)
        
    def test_following(self):
        c = Client()
        response = c.get("/following")
        
        # check login
        c.login(username='fred', password='secret')
        self.assertEqual(response.status_code, 200)
        
        # check anonym. -> redirect login
        c.logout()
        self.assertEqual(response.status_code, 200)
        
        
    def test_profile(self):
        c = Client()
        response = c.get("/profile/nonExistingUsername")
        self.assertEqual(response.status_code, 404)

    def test_new_post(self):
        c = Client()
        c.login(username='red', password='123')
        response = c.post('/', {'content': 'fred'})
        self.assertEqual(response.status_code, 202)

    def test_long_post(self):
        c = Client()
        c.login(username='red', password='123')
        content = 2 ** 1500
        response = c.post('/', {'content': content})
        self.assertFalse(PostForm.is_valid())


    
# Run each of the testing functions
if __name__ == "__main__":
    unittest.main()