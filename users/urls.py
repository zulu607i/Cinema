from django.urls import path
from users.views import *

urlpatterns = [
    path('pre_register', pre_register, name='pre_register'),
    path("register/<slug:uidb64>/", register_view, name="register"),
    path('activation_sent', activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', activate_user_profile, name='activate_profile'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
]