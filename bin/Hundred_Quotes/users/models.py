from django.db import models


# Create your models here.


class UserQuote(models.Model):
    quote_text = models.CharField(max_length=500)
    author_name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)

    def __str__(self):
        return self.quote_text
