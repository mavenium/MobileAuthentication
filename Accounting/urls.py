from django.urls import path

from . import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='index'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
]
