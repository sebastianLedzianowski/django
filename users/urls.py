from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.sign_up_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.log_out_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('custom_password_reset/', views.custom_password_reset, name='custom_password_reset'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='custom_password_reset_confirm'),
]

