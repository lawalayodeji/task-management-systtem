# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import  JsonResponse
from apps.authentication.models import myUser
from apps.Task_man.models import Timer
from datetime import datetime

@login_required
def index(request):
    # checking if the check_out and checkin is valid using ajax
    #  using status 0,1,2 to know their status

    error = []
    if request.method == "POST":
        check = int(request.POST["check"])
        
        if check:
            user1 = myUser.objects.get(username=request.user.username)
            
            timer = Timer.objects.filter(user=user1)
            if len(timer) == 0:
                Timer.objects.create(user = user1, status=0)


            timer_neu = Timer.objects.filter(user=request.user).last()
            if check == 1:
                if int(timer_neu.status) == 2:
                    Timer.objects.create(user = user1, status=1, clock_in=datetime.now())
                    return JsonResponse({"data":"You have clock-in!"}, safe=False)

                elif int(timer_neu.status) == 0:
                    timer_neu.status = 1
                    timer_neu.clock_in = datetime.now()
                    timer_neu.save()
                    return JsonResponse({"data":"You have clock-in!"}, safe=False)

                elif int(timer_neu.status) == 1:
                    return JsonResponse({"data":"You have already Clock-in"}, safe=False)

                    error.append("You have already Clock-in")
            elif check == 2:
                if int(timer_neu.status) == 1:
                    timer_neu.status=2
                    timer_neu.clock_out = datetime.now()
                    timer_neu.save()
                    return JsonResponse({"data":"You have clock-out!"}, safe=False)

                elif int(timer_neu.status) == 2:
                    return JsonResponse({"data":"You need to clock in before you clock out"}, safe=False)

                    error.append("You need to clock in before you clock out")
                elif int(timer_neu.status) == 0:
                    return JsonResponse({"data":"You need to clock in before you clock out"}, safe=False)
                    error.append("You need to clock in before you clock out")
        else:
            render(request, "home/index.html")
    else:
        return render(request, "home/index.html")


@login_required
def profileView(request):
    return render(request,'home/profile.html')



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
