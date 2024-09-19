from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField( max_length=50)
    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title} by {self.author}'