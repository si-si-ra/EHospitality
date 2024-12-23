from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.userRegistration,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('',views.home,name='home'),

]
