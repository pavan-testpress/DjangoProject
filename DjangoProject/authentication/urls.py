from django.urls import path

from . import views

app_name = "authentication"
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout, name="logout"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password-reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
]
