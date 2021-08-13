from django.core.validators import MaxValueValidator
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
    size = models.ForeignKey(DogSize, on_delete=models.CASCADE, related_name='size', unique=False)

    def __str__(self):
        return self.name


class WalkerScheduler(models.Model):
    class DaysOfWeek(models.TextChoices):
        SUNDAY = 0, 'sunday'
        MONDAY = 1, 'monday'
        TUESDAY = 2, 'tuesday'
        WEDNESDAY = 3, 'wednesday'
        THURSDAY = 4, 'thursday'
        FRIDAY = 5, 'friday'
        SATURDAY = 6, 'saturday'

    id = models.BigAutoField(primary_key=True)
    walker = models.UUIDField()
    day = models.PositiveIntegerField(choices=DaysOfWeek.choices, validators=[MaxValueValidator(6)])
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    sizes = models.ManyToManyField(DogSize, related_name='sizes', unique=False)

    def __str__(self):
        return '%s %s - %s' % (self.day, self.start, self.end)
