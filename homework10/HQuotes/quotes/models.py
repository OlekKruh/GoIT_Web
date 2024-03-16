from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.DateField(null=True, blank=True)
    born_location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="quotes", verbose_name="Author")
    text = models.TextField(verbose_name="Quote", unique=True)  # Считаем, что текст цитаты уникален
    tags = models.CharField(max_length=200, verbose_name="Tag", help_text="Split tags with coma(,).")

    def __str__(self):
        return f"{self.author.fullname}: {self.text[:50]}..."


