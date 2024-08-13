from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# Create your models here.

class Color(models.Model):

    color_name = models.CharField('Tent color', max_length = 60)

    def __str__(self):
        return self.color_name


class Tent(models.Model):
    TENT_MATERIAL_LIST = (
        ('nylon', 'nylon'),
        ('polyester', 'polyester'),
        ('canvas', 'canvas'),
        ('polyethylene', 'polyethylene'),
    )

    name = models.CharField('Tent name', max_length=60)
    price = models.PositiveIntegerField('Tent price')
    color = models.ManyToManyField(Color, related_name='tent_color')
    material = models.CharField('Tent material', choices=TENT_MATERIAL_LIST, max_length=30)
    capacity = models.PositiveIntegerField('Tent capacity (people)')
    weight = models.FloatField('Tent weight (kg)')
    height = models.FloatField('Tent height (m)')
    image1 = models.ImageField('Tent image1', upload_to='tent_images')
    image2 = models.ImageField('Tent image2', upload_to='tent_images', blank=True)
    image3 = models.ImageField('Tent image3', upload_to='tent_images', blank=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tent = models.ForeignKey(Tent, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)    