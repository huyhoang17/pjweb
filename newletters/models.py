from django.db import models

# Create your models here.


class Newsletters(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
