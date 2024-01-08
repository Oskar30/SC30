import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse

url = 'http://127.0.0.1:8000/repair/api/orders/'


@pytest.fixture
def get_or_create_token(db, create_user):
   user = create_user()
   token, _ = Token.objects.get_or_create(user=user)
   return token


@pytest.mark.django_db
def test_unauthorized_request(api_client, get_or_create_token):
   url = 'http://127.0.0.1:8000/repair/api/orders/'
   token = get_or_create_token('asd')
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200