from django.db import models
from froala_editor.fields import FroalaField

CHOICES = (
    ("ACCEPT","ACCEPT"),
    ("REJECT","REJECT"),
    ("UNTICK","UNTICK"),
)

TASK_CHOICES = (
    (0, "OPEN"),
    (1, "CLOSE"),
)

TASK_PRIORITY = (
    (0, "LOW"),
    (1, "MEDIUM"),
    (2, "HIGH"),

)

TASK_Submit = (
    (1, "YES"),
    (0, "NO"),
)

class Tasks(models.Model):
    Name = models.CharField(max_length=40)
    description = FroalaField()
    priority = models.IntegerField(choices=TASK_PRIORITY,null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    startdate = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=TASK_CHOICES, default=TASK_CHOICES[0][0], null=True)
    user = models.ForeignKey("authentication.myUser",on_delete=models.CASCADE,related_name="taskuser")
    submitConfirm = models.IntegerField(choices=TASK_Submit,default=TASK_Submit[1][0], null=True)


    def __str__(self):
        return self.Name
    

class Timer(models.Model):
    clock_in = models.DateTimeField(null=True)
    clock_out = models.DateTimeField(null=True)
    status = models.IntegerField()
    user = models.ForeignKey("authentication.myUser",on_delete=models.CASCADE,related_name="timeruser")

class Shedule(models.Model):
    monday_1 = models.BooleanField(default=False)
    tuesday_1 = models.BooleanField(default=False) 
    wesnesday_1 = models.BooleanField(default=False) 
    thursday_1 = models.BooleanField(default=False) 
    friday_1 = models.BooleanField(default=False) 
    user = models.ForeignKey("authentication.myUser", on_delete=models.CASCADE,related_name="usershe", null=True)

    def __str__(self):
        return "shedule"


class TimerOff(models.Model):
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=CHOICES, null=True)
    user = models.ForeignKey("authentication.myUser",on_delete=models.CASCADE,related_name="leaveuser", null=True)
    
    def __str__(self):
        return "User-Timeoff"




class Notification(models.Model):
    task = models.ForeignKey("Tasks",on_delete=models.CASCADE,related_name="notifytask")
    read = models.BooleanField(default=False)
    user = models.ForeignKey("authentication.myUser",on_delete=models.CASCADE,related_name="notifyuser")


class DoTask(models.Model):
    task_text = FroalaField()
    comment = models.ManyToManyField('Comment',related_name="doComment")
    task_main = models.ForeignKey("Tasks",on_delete=models.CASCADE,)

    class Meta:
        ordering = ['id',]


class Comment(models.Model):
    text = models.CharField(max_length=300)
    c_task = models.ForeignKey("DoTask",on_delete=models.CASCADE,related_name="mainComment")
    user = models.ForeignKey("authentication.myUser",on_delete=models.CASCADE,related_name="userComment")



