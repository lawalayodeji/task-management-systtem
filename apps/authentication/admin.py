# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import myUser, Profile

admin.site.register(myUser)
admin.site.register(Profile)


# Register your models here.
