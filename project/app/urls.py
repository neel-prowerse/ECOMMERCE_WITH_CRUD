from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index),
    path('mobile',views.mobile),
    path('show',views.show),
    path('edit',views.edit),
    path('update/<int:mid>',views.update),
    path('delete/<int:mid>',views.delete),
    path('register/',views.register),
    path('login/',views.login),
    path('logout/',views.logout), 
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
