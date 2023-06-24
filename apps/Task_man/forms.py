from .models import Tasks,DoTask,Comment,Shedule,TimerOff
from django.forms import ModelForm
from django import forms
from froala_editor.widgets import FroalaEditor
from apps.authentication.models import myUser



class TaskForm(ModelForm):
    user=forms.ModelChoiceField(queryset=myUser.objects.all()),
    class Meta:
        model = Tasks
        fields = ("Name","description","deadline","priority","status","submitConfirm")
        
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'deadline':forms.DateField(widget=forms.widgets.DateInput(
        #         attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'})
        # )
            'description': FroalaEditor(),

        'deadline':forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}),
                
        'priority': forms.Select(attrs={ 'class': 'form-control'}),
        'status':  forms.Select(attrs={ 'class': 'form-control'}),
        'submitConfirm': forms.Select(attrs={'class': 'form-control'}),

        }


class DoTaskForm(ModelForm):
    class Meta:
        model = DoTask
        fields = ('task_text',)
        
        widgets = {
            'task_text': FroalaEditor(),
        }


class EmployeeCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control commentChat'}),
        }


class EmployeeSheduleForm(ModelForm):
    class Meta:
        model = Shedule
        fields = ('monday_1','tuesday_1','wesnesday_1','thursday_1','friday_1')
        
        widgets = {
            'monday_1': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'tuesday_1': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'wesnesday_1': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'thursday_1': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'friday_1': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
        }

class TimeOffForm(ModelForm):
    class Meta:
        model = TimerOff
        fields = ('startdate','enddate')
        
        widgets = {
            'startdate': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'enddate': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        }
