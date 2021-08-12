from django.db import models


# Create your models here.
class DogSize(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.label


class Dog(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120)
    owner = models.UUIDField()
    size = models.OneToOneField(DogSize, on_delete=models.CASCADE, related_name='size', unique=False)

    def __str__(self):
        return self.name
