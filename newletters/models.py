from django.db import models

# Create your models here.


class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Detail Sign Up'
        verbose_name_plural = 'SignUps'
