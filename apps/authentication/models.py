from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save

from django.dispatch import receiver



class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class myUser(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)


    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email","first_name","last_name"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin 

class Profile(models.Model):
    user = models.OneToOneField("myUser",on_delete=models.CASCADE,)
    image = models.ImageField(default="./default_faculty.png", upload_to='profile_pics')

    
    @receiver(post_save, sender=myUser)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=myUser)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()


    def __str__(self):
        return self.user.username
        


   


    


    

