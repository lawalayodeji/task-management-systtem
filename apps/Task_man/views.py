from django.shortcuts import render, redirect
from .forms import TaskForm,DoTaskForm,EmployeeCommentForm,EmployeeSheduleForm,TimeOffForm
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.authentication.models import myUser, Profile
from .models import Tasks,Notification,DoTask,Comment,Timer,Shedule,TimerOff
from apps.authentication.forms import EditSignUp,EditProfileForm
from datetime import datetime
import pytz


@login_required
def EditProfile(request):
    usertext = myUser.objects.get(id=request.user.id)
    err = ' '
    if request.method == "POST":
         form = EditSignUp(request.POST, instance=request.user)
         form_sec = EditProfileForm(request.POST,request.FILES, instance=request.user.profile)
         if form.is_valid() and form_sec.is_valid():
            form.save()
            form_sec.save()
         else:
            err+="please check and try again!"
    else:
        form = EditSignUp(instance=usertext)
        form_sec = EditProfileForm(instance=request.user.profile)


    context = {
        "form": form,
        'form_sec': form_sec,
        'err': err
    }    

    return render(request, "./home/editProfile.html", context)





@user_passes_test(lambda u: u.is_admin)
def TasksMaker(request, id):
    employee = myUser.objects.get(username=id)
    msg = []
    if request.method == "POST":
        form = TaskForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['Name']
            description = form.cleaned_data['description']
            priority = form.cleaned_data['priority']
            deadline = form.cleaned_data['deadline']
            status = form.cleaned_data['status']
            submitConfirm = form.cleaned_data['submitConfirm']
            employee_task = Tasks.objects.create(Name=name, description=description,priority=priority,deadline=deadline,
            status=status, user=employee,submitConfirm=submitConfirm
            )
            DoTask.objects.create(task_main=employee_task)            
            Notification.objects.create(task=employee_task,user=employee)


            msg.append("Task Added SuccessFully!")
        else:
            msg.append("Error check the Input!")
    
    form = TaskForm()

    context = {
        "form": form,
        "msg": msg
    }

    return render(request, "./tasks/myTask.html", context)

@user_passes_test(lambda u: u.is_admin)
def EditTask(request, id):
    task_obj = Tasks.objects.get(id=id)
    err = ' '
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task_obj)

        if form.is_valid():

            form.save()
        else:
            err += 'Wrong input! please try again'
    else:
        form = TaskForm(instance=task_obj)


    context = {
    'form': form,
    'err': err,
    }

    return render(request, './tasks/edit-task.html', context)


@user_passes_test(lambda u: u.is_admin)
def CloseTask(request, id):
    task_obj = Tasks.objects.get(id=id)
    myId = task_obj.user.id
    task_obj.status= 0
    task_obj.save()
    tasks =  Tasks.objects.filter(user__id=myId).order_by('-priority')
    context = {
        "tasks": tasks,
        'length': len(tasks)
    }

    return render(request, './tasks/task-list.html', context)


@login_required
def count_detect_notifiy(request):
    if request.method == "POST":
        notify = Notification.objects.filter(user=request.user, read=False)
        if len(notify) > 0:
            my_count = notify.count()
        else:
            notify = 'empty'
            my_count = "0"
    else:
        notify = 'empty'
        my_count = "0"

    context = {
        'my_count': my_count
        }

    return JsonResponse(context, safe=False)

@login_required
def notifyCheck(request):
    notifys = Notification.objects.filter(user=request.user, read=False)
    mlength = len(notifys)
    print(notifys)
    context = {
        'notifys':notifys,
        "lengths": mlength,
    }

    return render(request, 'tasks/notifications.html',context)


def ReadNotify(request, id):
    notify = Notification.objects.get(id=id)
    notify.read= True
    notify.save()


    return redirect('CheckNotifyid')


@user_passes_test(lambda u: u.is_admin)
def employee_list(request):
    user = myUser.objects.all()
    context = {
        "employees": user
    }

    return render(request, './tasks/employee.html', context)


@user_passes_test(lambda u: u.is_admin)
def delete_employee(request,id):
    user = myUser.objects.get(id=id)
    user.delete()
    return render(request, './tasks/employee.html', context)
    

@user_passes_test(lambda u: u.is_admin)
def edit_employee(request,id):
    user = myUser.objects.get(id=id)
    err = ' '
    if request.method == "POST":
        form = EditSignUp(request.POST, instance=user)
        if form.is_valid() :
            form.save()
        else:
            err+="please check and try again!"
    else:
      form = EditSignUp(instance=user)


    context = {
        "form": form,
        'err': err,
        "myuser": user,
    }    

    return render(request, './tasks/editUser.html', context)
    



@user_passes_test(lambda u: u.is_admin)
def sheduleUser(request, id):
    userc = myUser.objects.get(id = id)
    myshe = Shedule.objects.filter(user=userc)
    if request.method == "POST":
        try:
            my_she = Shedule.objects.get(user=userc)
            form = EmployeeSheduleForm(request.POST, instance=my_she)
        except:
            form = EmployeeSheduleForm(request.POST)

        

        if form.is_valid():
            monday = form.cleaned_data['monday_1']
            tuesday = form.cleaned_data['tuesday_1'] 
            wesnesday = form.cleaned_data['wesnesday_1'] 
            thursday = form.cleaned_data['thursday_1'] 
            friday = form.cleaned_data['friday_1'] 
            
            my_shedule = Shedule.objects.filter(user=userc)

            if len(my_shedule) > 0:
                my_shedule_obj = Shedule.objects.get(user=userc)
                my_shedule_obj.monday_1=monday
                my_shedule_obj.tuesday_1 = tuesday
                my_shedule_obj.wesnesday_1=wesnesday
                my_shedule_obj.thursday_1=thursday
                my_shedule_obj.friday_1=friday
                my_shedule_obj.user=userc         
                my_shedule_obj.save()
            else:
                Shedule.objects.create(monday_1=monday,
                tuesday_1=tuesday,
                wesnesday_1=wesnesday,
                thursday_1=thursday,
                friday_1=friday,
                user=userc,         
                )
    try:
        my_she = Shedule.objects.get(user=userc)
        form = EmployeeSheduleForm(instance=my_she)
    except:
        form = EmployeeSheduleForm()

    
    context ={"form": form}
    return render(request, 'tasks/shedule.html',context)






@login_required
def task_list(request,id):
    tasks =  Tasks.objects.filter(user__id=id).order_by('-priority')
    context = {
        "tasks": tasks,
        'length': len(tasks)
    }

    return render(request, './tasks/task-list.html', context)



@login_required
def do_task(request,id):
    user_task = Tasks.objects.get(id=id)
    tasks = DoTask.objects.get(task_main__id=id)
    user_t = myUser.objects.get(username=request.user.username)

    if user_task.startdate == None:
        user_task.startdate= datetime.now()
        user_task.save()
    if user_task.deadline <= datetime.now().replace(tzinfo=pytz.utc):
        print("yes")
        print(user_task.status)
        user_task.status = 1
        user_task.save()




    if request.method == "POST":
        form = DoTaskForm(request.POST, instance=tasks)
        comment_form = EmployeeCommentForm(request.POST)

        if form.is_valid():
            form.save()


        c_text = request.POST.get("commentData")
        if c_text != ' ' and c_text != None:

            userComment = Comment.objects.create(
                text=str(c_text),
                c_task = tasks,
                user=user_t
            )
            tasks.comment.add(userComment)
            tasks.save()
    else:
        form = DoTaskForm(instance=tasks)
        comment_form = EmployeeCommentForm()
        

    context = {
        'form': form,
        'comment_form':comment_form,
        'task_id': id,
        'task_com': tasks.comment.order_by('id'),
        'task_user':user_task.user.username,
    }

    return render(request, 'tasks/do_task.html', context)



@login_required
def TimeoffView(request):
    user_t = myUser.objects.get(username=request.user.username)
    msg = ' '
    if request.method == "POST":
        form = TimeOffForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['startdate']
            end_date = form.cleaned_data['enddate'] 
            TimerOff.objects.create(
                startdate=start_date,
                enddate = end_date,
                user = user_t,
                status ='UNTICK',
            )
            msg+="Request sent!"

    form = TimeOffForm()
    context = {
        'form':form,
        "msg": msg,
    }
    return render(request, 'tasks/requestTimeOff.html', context)


@user_passes_test(lambda u: u.is_admin)
def VerifyTimeoffView(request):
    leaveRequest = TimerOff.objects.filter(status='UNTICK')
    context = {
        'leaveRequest':leaveRequest,
    }
    return render(request, 'tasks/verifyLeave.html', context)



@user_passes_test(lambda u: u.is_admin)
def Reject_or_Approve(request):
    if request.method == "POST":
        myidq = request.POST['myId']
        leaveRequestobj = TimerOff.objects.get(status='UNTICK', id=myidq)
        key = request.POST.get("mykey")

        if key == 'approve':
            leaveRequestobj.status = 'ACCEPT'
            leaveRequestobj.save()
            return JsonResponse({"data":"You Have accept the request"}, safe=False)

        elif key == 'reject':
            leaveRequestobj.status = 'REJECT'
            leaveRequestobj.save()
            return JsonResponse({"data":"You Have reject the request"}, safe=False)
        else:
            return JsonResponse({"data":"oops! try again"}, safe=False)
    return JsonResponse({"data":"oops! try again"}, safe=False)


@user_passes_test(lambda u: u.is_admin)
def Report(request, id):
    # first report list is the lenght of the task  - total_task
    #  second report is the done task - Done_task
    # third is the close task or undone - unDone_task
    j= 0
    k= 0
    m=0
    myuserData = myUser.objects.get(id=id)
    Attendance_logic = Timer.objects.filter(user__id=id)
    if len(Attendance_logic) > 0:
        Attendance   = Attendance_logic
    else:  
        Attendance = None

    Mytask = Tasks.objects.filter(user__id=id)
    for task_report in Mytask:
        if task_report.submitConfirm == 1:
            j+=1

        if task_report.status == 1 and task_report.submitConfirm == 0:
            k+=1
        
        if task_report.status == 0 and task_report.submitConfirm == 0:
            m+=1
        
    total_task = len(Mytask)
    Done_task = j
    unDone_task = k
    openUnDone_task = m

    if total_task > 0:
        percentage_done = (Done_task/total_task) * 100
        percentage_closeUndone = (unDone_task/total_task) * 100
        percentage_openUndone = (openUnDone_task/total_task) * 100
    else:
        percentage_done = 0                                                                          
        percentage_closeUndone = 0
        percentage_openUndone = 0



    context = {
        'percentage_done':percentage_done,
        'percentage_closeUndone':percentage_closeUndone,
        'percentage_openUndone':percentage_openUndone,
        'Attendance':Attendance,
        'total_task':total_task,
        'Done_task':Done_task,
        'unDone_task':unDone_task,
        'openUnDone_task':openUnDone_task,
        "myUser":myuserData,


    }


    return render(request, './tasks/report.html', context)









    


