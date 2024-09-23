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
        #using seeion auth (create.login)
        logged_in = self.client.login(username='testuser', password='testpass')
        print(f"Logged in: {logged_in}")  # Check if login is successful
        
        # using token auth to login
        #self.token = Token.objects.create(user=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        #not a best practice using force_auth
        #logged_in = self.client.force_authenticate(user=self.user)
        
        # Create an Author instance
        self.author = Author.objects.create(name='Test Author')        
        # Create a test book
        self.book = Book.objects.create(title='Test Book', author=self.author, publication_year='2020')
          # Adjust according to your URL name

    def test_create_book(self):
        book_url = reverse('book-create')
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year':'2020'
        }
        response = self.client.post(book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Check if the book is created
        

    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'author': self.author.id,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        


    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book should be listed
        
        
    def test_update_book_without_permission(self):
        # Create another user without update permissions
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='otheruser', password='otherpass')
        data = {'title': 'Unauthorized Update', 'author': self.author.id}
        url = reverse('book-update-test', args=[self.book.id])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_filter_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check that the correct book is returned
        self.assertEqual(response.data[0]['title'], 'Test Book') 


    def test_search_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books(self):
        url = reverse('book-list')
        # Assuming ordering is implemented, e.g., by title
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add checks based on the expected order