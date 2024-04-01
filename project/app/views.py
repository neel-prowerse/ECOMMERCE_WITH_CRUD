from django.shortcuts import render,redirect
from .models import Mobile
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.

def index(request):
  return render(request,'index.html')

def mobile(request):
  mobiles = Mobile.objects.all()
  return render(request,'mobile.html',{'mobiles':mobiles})

def show(request, name):
  mobile = Mobile.objects.get(name=name)
  return render(request,'show.html',{'mobile':mobile})

def edit(request, name):
  mobile = Mobile.objects.get(name=name)
  return render(request,'edit.html',{'mobile':mobile})

def update(request, name):
  mobile = Mobile.objects.get(name=name)
  return render(request,'edit.html',{'mobile':mobile})

def delete(request, name):
  mobile = Mobile.objects.get(name=name)
  mobile.delete()
  return redirect('/mobile')

def register(request):
  if request.method == 'GET':
    return render(request,'register.html',{'form':UserCreateForm})
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
        user.save()
        login(request,user)
        return redirect('index')
      except IntegrityError:
        return render(request,'register.html',
                      {
                        'form':UserCreateForm,
                        'error':'Username already exists.'
                      })
    else:
      return render(request,'register.html',
                    {'form':UserCreateForm,
                     'error':'Passwords do not match'
                    })

def login(request):
  if request.method == 'GET':
            return render(request, 'login.html',{'form':AuthenticationForm})
  else:
      user = authenticate(request, 
                          username = request.POST['username'],
                          password = request.POST['password'])
      if user is None:
          return render(request, 'login.html',
                          {
                            'form':AuthenticationForm(),
                            'error':'username and password do not match'
                          })
      else:
          login(request,user)
          return redirect('index')

def logout(request):
  logout(request)
  return render(request,'index.html')