from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import *
from mydemo.models import *
from functools import wraps
from django.shortcuts import render
import datetime
from django.http import HttpResponse
from myProject import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import os

# Create your views here.

def index(request):
    return HttpResponse("Welcome visit our page")

def login_required():
    def login_decorator(function):
        @wraps(function)
        def wrapped_function(request):

            # if a user is not authorized, redirect to login page
            if 'user' not in request.session or request.session['user'] is None:
                return redirect("/")
            # otherwise, go on the request
            else:
                return function(request)

        return wrapped_function

    return login_decorator


# login view
def login(request):
    error = 'none'
    request.session['user'] = None

    if 'username' in request.POST:

        # get username and password from request.
        username = request.POST['username']
        password = request.POST['password']

        # check whether the user is in database or not
        if username == settings.ADMIN_NAME and password == settings.ADMIN_PASSWORD:
            request.session['user'] = {
                # "id": user[0].id,
                "username": settings.ADMIN_NAME, #user[0].email,
                "password": settings.ADMIN_PASSWORD, #user[0].name.split(" ")[0],
                "role": "admin"
            }

            return redirect("/pricing")

        user = Account.objects.filter(email=username, password=password)
        if len(user) > 0:
            request.session['user'] = {
                # "id": user[0].id,
                "firstname" : user[0].firstname,
                "lastname" : user[0].lastname,
                "username": user[0].username,
                "email": user[0].email,
                "phone" : user[0].phone,
                "address" : user[0].address,
                "password": user[0].password,
                "role" : "client",
            }

            return redirect("/pricing")
        else:
            error = 'block'

    # return render_to_response('login.html', {'error':error}, context_instance=RequestContext(request))
    return render(request, 'login.html', {'error':error})


def logout(request):
    request.session['user'] = None
    return redirect("/")

def main(request):
    # clients = Client.objects.all().order_by("-created_on")
    # return render_to_response('blank.html', locals(), context_instance=RequestContext(request))
    return render(request, 'blank.html', locals())

def pricing(request):
	# stripe_pk = settings.STRIPE_PUBLIC_KEY

	# if "email" not in request.session['user']:
	#     return redirect("/main")

	# client = Client.objects.filter(email=request.session['user']["email"])[0]
	# price = Client.objects.filter(email=request.session['user']["email"])[0].pricing


    # return render_to_response('pricing.html', locals(), context_instance=RequestContext(request))
    return render(request, 'pricing.html', locals())

def signup(request):
    
    if request.POST:
        account = Account()
        account.firstname = request.POST["firstname"]
        account.lastname = request.POST["lastname"]
        account.username = request.POST["username"]
        account.email = request.POST["email"]
        account.phone = request.POST["phone"]
        account.address = request.POST["address"]
        account.password = request.POST["password"]
        request.session['user'] = {
	        # "id": user[0].id,
	        "firstname" : request.POST["firstname"],
	        "lastname" : request.POST["lastname"],
	        "username": request.POST["username"],
	        "email": request.POST["email"],
	        "phone" : request.POST["phone"],
	        "address" : request.POST["address"],
	        "password": request.POST["password"],
	        "role" : "client",
	    }
        account.save()
        return redirect("/pricing")

    # return render_to_response('signup.html', locals(), context_instance=RequestContext(request))
    return render(request, 'signup.html', locals())

def changePwd(request):
    if request.POST:
        if request.POST["opassword"] == request.session['user']['password']:
            if request.POST["password"] == request.POST["rpassword"]:
                account = Account.objects.filter(email=request.session['user']['email']).update(password=request.POST["password"])
                request.session['user']['password'] = request.POST['password']
                return redirect("pricing") 
    # return render_to_response("changePwd.html",locals(),context_instance=RequestContext(request))
    return render(request, 'changePwd.html', locals())

def forgot(request):
    if request.POST:
        if request.POST["password"] == request.POST["rpassword"]:
            account = Account.objects.filter(email=request.POST["email"]).update(password=request.POST["password"])
            return redirect("login") 
    return render(request, 'forgot.html', locals())