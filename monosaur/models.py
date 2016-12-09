from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Company(models.Model):
    name = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name
