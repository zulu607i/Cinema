from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User) # used to send the User data to UserProfile.
def update_profile_signal(sender, instance, created, **kwargs): #sender= model, instace= user data that is being saved, created= boolean(if the instace is created)
    if created:
        return UserProfile.objects.create(user=instance)
    instance.userprofile.save() # save the data form the user and updates the UserProfile.
