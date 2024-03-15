from django.db import models


# Create your models here.
class Quote(models.Model):
    quote_text = models.CharField(max_length=500)
    author_name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)

    def __str__(self):
        return self.quote_text


class AuthorBio(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.fullname
