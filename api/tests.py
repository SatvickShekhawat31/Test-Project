from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UploadedFile

User = get_user_model()

class FileSharingTests(APITestCase):
    def setUp(self):
        # Create Ops user
        self.ops_user = User.objects.create_user(username='ops1', password='pass1234', role='ops')
        self.ops_token = Token.objects.create(user=self.ops_user)

        # Create Client user
        self.client_user = User.objects.create_user(username='client1', password='pass1234', role='client')
        self.client_token = Token.objects.create(user=self.client_user)

    def test_register(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'new@x.com', 'password': 'pass1234', 'role': 'client'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        data = {'username': 'client1', 'password': 'pass1234'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_ops_upload_file(self):
        url = reverse('file-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.ops_token.key)
        file = SimpleUploadedFile("test.docx", b"dummy content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_upload_file(self):
        url = reverse('file-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token.key)
        file = SimpleUploadedFile("test.docx", b"dummy content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_files(self):
        # Upload one file with ops
        UploadedFile.objects.create(uploader=self.ops_user, file='uploads/test.docx')
        url = reverse('file-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_download_file_link(self):
        file = UploadedFile.objects.create(uploader=self.ops_user, file='uploads/test.docx')
        url = reverse('download-file', args=[file.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('download-link', response.data)

