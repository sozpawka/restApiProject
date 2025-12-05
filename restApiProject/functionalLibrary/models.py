from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField()
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
