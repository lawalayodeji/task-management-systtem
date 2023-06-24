from django.contrib import admin
from .models import Tasks,Timer,Notification, DoTask, Comment,Shedule,TimerOff
# Register your models here.

admin.site.register(Tasks)
admin.site.register(Notification)

admin.site.register(Timer)
admin.site.register(DoTask)
admin.site.register(Comment)
admin.site.register(Shedule)
admin.site.register(TimerOff)


