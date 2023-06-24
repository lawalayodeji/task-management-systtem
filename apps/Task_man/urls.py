from django.urls import path
from .views import TasksMaker,employee_list,count_detect_notifiy,task_list,do_task,sheduleUser,TimeoffView,VerifyTimeoffView,Reject_or_Approve,delete_employee,edit_employee,EditTask,CloseTask,ReadNotify,notifyCheck,Report,EditProfile


urlpatterns = [
    path('tasks/<str:id>/', TasksMaker, name="task"),
    path('employee/', employee_list, name="employeeList"),
    path('notify/', count_detect_notifiy, name="count_notifiy"),
    path('tasks-list/<int:id>/', task_list, name="mytask"),
    path('tasks-do/<int:id>/', do_task, name="task-do"),
    path('shedule/<int:id>/', sheduleUser, name="shedule-user"),
    path('Timeoff/', TimeoffView, name="myTimeoff"),
    path('verifyTimeoff/', VerifyTimeoffView, name="myVerifyTimeoff"),
    path('Reject_or_Approve/', Reject_or_Approve, name="myVerTimeoff"),
    path('Deleteuser/<int:id>/', delete_employee, name="DeleteEmployee"),
    path('Editeuser/<int:id>/', edit_employee, name="EditEmployee"),
    path('EditTask/<int:id>/', EditTask, name="myEditTask"),
    path('CloseTask/<int:id>/', CloseTask, name="myCloseTask"),
    path('Readme/<int:id>/', ReadNotify, name="read"),
    path('CheckNotify/', notifyCheck, name="CheckNotifyid"),
    path('Report/<int:id>/', Report, name="myReport"),
    path('EditProfile/', EditProfile, name="myEditProfile"),




]
