from django.shortcuts import render,redirect
from .models import Mobile,Company
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm,MobileForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request): 
  company = Company.objects.all()
  return render(request,'index.html',{'company':company})

# def mobile(request,id):
#   mobile = Mobile.objects.filter(id=id)
#   if request.method  == 'POST':
#         form = MobileForm(request.POST)
#         try:
#             if form.is_valid():
#                 form.save()
#                 return redirect('show/')
#         except:
#             pass
#   else:
#         form = MobileForm()
    
#   return render(request, 'mobile.html',{'mobiles':mobile})
  
def add(request):
  # mobile = Mobile.objects.all()
  # company = Company.objects.all()
  if request.method  == 'POST':
    form = MobileForm(request.POST or None)
    # form2 = CompanyForm(request.POST)
    if form.is_valid():
            form.save()
            # form2.save()
            return redirect('/show/')
  else:
    form = MobileForm()
    # form2= CompanyForm()
    return render(request, 'add.html',{'form':form})

def show(request):
  searchTerm = request.GET.get('searchTerm')
  if searchTerm:
    mobiles = Mobile.objects.filter(company__name__contains=searchTerm)
  else:
    mobiles = Mobile.objects.all()
  return render(request,'show.html',{'mobiles':mobiles, 'searchTerm':searchTerm})

def showid(request,id):
  company = Company.objects.filter(id=id)
  mobile = Mobile.objects.filter(id=id)
  return render(request,'mobile.html',{'mobile':mobile,'company':company})

def edit(request,id):
  mobile = Mobile.objects.get(id=id)
  return render(request,'edit.html',{'mobile':mobile})

def update(request, id):
  mobile=Mobile.objects.get(id=id)
  form = MobileForm(request.POST or None,instance=mobile)     
  if form.is_valid():
      form.save()
      return redirect('/show/')
  return render(request, 'edit.html',{'mobile':mobile, 'form':form})


def delete(id):
  mobile = Mobile.objects.get(id=id)
  mobile.delete()
  return redirect('show/')

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
        return render(request,'register.html',{'form':UserCreateForm,'error':'Username already exists.'})
    else:
      return render(request,'register.html',{'form':UserCreateForm,'error':'Passwords do not match'})

def loginaccount(request):
  if request.method == 'GET':
            return render(request, 'login.html',{'form':AuthenticationForm})
  else:
      user = authenticate(request, username = request.POST['username'],password = request.POST['password'])
      if user is None:
          return render(request, 'login.html',{'form':AuthenticationForm(),'error':'username and password do not match'})
      else:
          login(request,user)
          return redirect('index')

@login_required
def logoutaccount(request):
  logout(request)
  return render(request,'index.html')