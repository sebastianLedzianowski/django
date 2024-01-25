from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.CharField(blank=True, max_length=50)
    born_location = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


