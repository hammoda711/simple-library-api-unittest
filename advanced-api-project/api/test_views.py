from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Author, Book  # Assuming the Book model is in the 'api' app
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BookAPITest(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        #self.token = Token.objects.create(user=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(username='testuser', password='testpassword')

        # Create an Author instance
        self.author = Author.objects.create(name='Test Author')        
        # Create a test book
        self.book = Book.objects.create(title='Test Book', author=self.author, publication_year='2020')
        self.book_url = reverse('book-create')  # Adjust according to your URL name

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year':'2020'
        }
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Check if the book is created
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')