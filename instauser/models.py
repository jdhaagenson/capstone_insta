from django.db import models
from django.contrib.auth.models import AbstractUser

THEME_CHOICES = [
    ('default', (
        ('theme_vanilla.jpg', 'theme_vanilla'),
        ('theme_vanilla2.jpeg', '2')
    )),
    ('Feb', (
        ('theme_feb1.jpg', '1'),
        ('theme_feb2.jpg', '2'),
        ('theme_feb3.jpg', '3'),
        ('theme_feb4.jpg', '4'),
        ('theme_feb5.jpg', '5'),
    )),
    ('Mar', (('theme_mar1.jpg', '1'),)),
    ('Apr', (
        ('theme_apr1.jpg', '1'),
        ('theme_apr2.jpg', '2'),
    )),
    ('Jul', (
        ('theme_jul1.jpg', '1'),
        ('theme_jul2.jpg', '2'),
        ('theme_jul3.png', '3'),
        ('theme_jul4.png', '4'),
        ('theme_jul5.png', '5'),
        ('theme_jul6.jpg', '6'),
    )),
    ('Oct', (
        ('theme_oct1.png', '1'),
        ('theme_oct2.jpg', '2'),
        ('theme_oct3.png', '3'),
        ('theme_oct4.jpg', '4'),
        ('theme_oct5.png', '5'),
        ('theme_oct6.png', '6'),
        ('theme_oct7.png', '7'),
        ('theme_oct8.png', '8'),
        ('theme_oct9.jpg', '9'),
    )),
    ('Nov', (
        ('theme_nov1.jpg', '1'),
    )),
    ('Dec', (
        ('theme_dec1.jpg', '1'),
        ('theme_dec2.jpg', '2'),
        ('theme_dec3.jpg', '3'),
        ('theme_dec4.jpg', '4'),
        ('theme_dec5.jpg', '5'),
        ('theme_dec6.png', '6'),
        ('theme_dec7.jpg', '7'),
        ('theme_dec8.jpg', '8'),
    )),
]


class InstaUser(AbstractUser):
    display_name = models.CharField(max_length=40, unique=False)
    bio = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, default='self')
    profile_pic = models.ImageField(upload_to='image', default='/media/image/default.jpg')
    email = models.EmailField(blank=True, null=True)
    theme = models.CharField(max_length=30, default=THEME_CHOICES[0][0], null=True, blank=True, choices=THEME_CHOICES)

    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return f"@{self.username}"
