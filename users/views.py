from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from cinema.settings import EMAIL_HOST
from .forms import SignUpForm
from .tokens import generate_token
from django.contrib.auth.models import User
# Create your views here.


def activation_sent(request):
    return render(request, 'users/partials/activation_sent.html')


def activate_user_profile(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and generate_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.userprofile.is_verified = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/partials/activation_invalid.html')


def register_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.userprofile.first_name = form.cleaned_data.get('first_name')
        user.userprofile.last_name = form.cleaned_data.get('last_name')
        user.userprofile.email = form.cleaned_data.get('email')
        user.is_active = False
        user.save()
        current_domain = get_current_site(request)

        message = render_to_string('users/partials/request_activation.html', {
            'user': user,
            'domain': current_domain.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),

        })
        # send email
        print(message)
        send_mail('Please Activate Your Account',
                  message,
                  EMAIL_HOST,
                  [f'{user.userprofile.email}']
                  )

        return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'users/sign_up.html', {'form': form})

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=str(username), password=str(password))
        if user is not None and user.userprofile.is_verified == True or user.is_superuser:
            login(request, user)
            return redirect('home')

    return render(request, 'users/login.html')


def logoutPage(request):
    logout(request)
    return redirect('home')