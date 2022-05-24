from django.test import TestCase
import unittest

from .models import User, Profile, Post
from .views import profile
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.test import Client

csrf_client = Client(enforce_csrf_checks=True)

# Create your tests here.
def test_follow(self):
    """test following self"""
    u1 = User.objects.create(username="test_red", email="test.email@red.com", password="123")
    with self.assertRaises(HttpResponseBadRequest):
        self.client.login(username="test_red", password="123")
        profile.client.post(profile_name=u1.username)
        
def setUp(self):
    # Creater Users
    u1 = User.objects.create(username="test_red", email="test.email@red.com", password="123")
    u2 = User.objects.create(username="test_blue", email="test.email@blue.com", password="123")
    
# Run each of the testing functions
if __name__ == "__main__":
    unittest.main()