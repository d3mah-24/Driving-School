import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import *


# Create your views here.
def home(req):
    if req.user.is_authenticated:
        return render(req, "index.html", {"name": req.user.first_name})

    else:
        return render(req, "index.html")


quee = {"auto": Auto, "moto": Moto, "car": Car}


def s_email(req):
    if req.method == "POST":
        subject = req.POST.get('name')
        message = req.POST.get('body')
        from_email = req.POST.get('email')
        if subject and message and from_email:
            try:
                send_mail(subject, "Done.....", settings.EMAIL_HOST_USER, [from_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

@login_required
def result(req):
    moto = points.objects.get(user=req.user, type="moto")
    len_moto = quee["moto"].objects.all().count()
    auto = points.objects.get(user=req.user, type="auto")
    len_auto = quee["auto"].objects.all().count()
    car = points.objects.get(user=req.user, type="car")
    len_car = quee["car"].objects.all().count()
    con = {
        "moto": moto.point,
        "auto": auto.point,
        "car": car.point,
        "len_moto": len_moto,
        "len_auto": len_auto,
        "len_car": len_car,
    }
    return render(req, "result.html", con)


@login_required
def check_quiz(req,tyy="car"):
    if req.method=="POST":
        ans = req.POST.get("ans")
        id = req.POST.get("id")
        ty = req.POST.get("ty")
        c_answer = quee[ty].objects.get(id=id)
        len_q = quee[ty].objects.all().count()
        if int(id) == 1:
            points.objects.filter(user=req.user, type=ty).update(point=0)
        if c_answer.answer == ans:
            points.objects.filter(user=req.user, type=ty).update(point=F('point') + 1)
        if int(id) == len_q:
            return HttpResponse(json.dumps({}), content_type="application/json")
        que = list(quee[ty].objects.filter(id=int(id) + 1).values("question", "choose", "id", ))[0]
        que["len"] = len_q
        return HttpResponse(json.dumps(que), content_type="application/json")
    else:
        len_q = quee[tyy].objects.all().count()
        que = list(quee[tyy].objects.filter(id=1).values("question", "choose", "id", ))[0]
        return render(req, "quiz.html",
                      {"question": que["question"], "len": len_q, "typ": tyy, "id": que["id"],
                       "ch": que["choose"].split(",")})

def signup(req):
    if req.method == "POST":
        try:
            uname = req.POST.get("uname")
            email = req.POST.get("email")
            passs = req.POST.get("pswd")
            u = User.objects.create_user(first_name=uname, username=email, password=passs)
            points.objects.create(user=u, type="car", point=0)
            points.objects.create(user=u, type="moto", point=0)
            points.objects.create(user=u, type="auto", point=0)
            return render(req, "login.html", {"done": True, "stat": False})
        except:
            return render(req, "login.html", {"done": False, "stat": True})
    else:
        return redirect("/")
        # return render(req, "index.html")


def signin(req):
    if req.method == "POST":
        email = req.POST.get("email")
        passs = req.POST.get("pswd")
        u = authenticate(username=email, password=passs)
        if u is not None:
            login(req, u)
            return render(req, "index.html", {"name": u.first_name})
        else:
            return render(req, "login.html", {"stat": True, "message": "Wrong Password"})
    else:
        return render(req, "login.html")


def signout(req):
    logout(req)
    return redirect("/")
