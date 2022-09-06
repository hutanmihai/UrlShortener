from django.db import models
from django.contrib.auth.models import User

# Create your models here.
DOMAIN = "localhost:8000/"
DOMAIN_LENGTH = len(DOMAIN)
PATH = "/link/"
PATH_LENGTH = len(PATH)
DOMAIN_PATH = DOMAIN + 'link/'
class Url(models.Model):
    long_url = models.URLField(max_length=200)
    short_url = models.CharField(max_length=PATH_LENGTH+10, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    redirect_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_url