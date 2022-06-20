from base64 import urlsafe_b64decode

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from cinema.settings import EMAIL_HOST_USER
from .forms import SignUpForm
from .tokens import generate_token
from django.contrib.auth.models import User
from ratelimit.decorators import ratelimit

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
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/partials/activation_invalid.html')


@ratelimit(key="ip", rate="30/m", block=True)
def register_view(request,  uidb64):
    uidb64_padded = uidb64 + "=" * (-len(uidb64) % 4)
    to_email = force_str(urlsafe_b64decode(uidb64_padded))
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.userprofile.first_name = form.cleaned_data.get('first_name')
        user.userprofile.last_name = form.cleaned_data.get('last_name')
        user.is_active = False
        user.save()
        current_domain = get_current_site(request)

        message = render_to_string('users/partials/activate.html', {
            'user': user,
            'domain': current_domain.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),

        })
        # send email
        print(message)
        send_mail('Please Activate Your Account',
                  message,
                  EMAIL_HOST_USER,
                  [to_email]
                  )

        return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'users/sign_up.html', {'form': form,
                                                  'email': to_email})


@ratelimit(key="ip", rate="30/m", block=True)
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=str(username), password=str(password))
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            elif user.is_superuser:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'users/404.html')

    return render(request, 'users/login.html')


@ratelimit(key="ip", rate="30/m", block=True)
def logoutPage(request):
    logout(request)
    return redirect('home')

def pre_register(request):
    if request.method == "POST":
        try:
            validate_email(request.POST["email"])
        except ValidationError:
            messages.error(request, ("Email address is incorrect"))
            return redirect("pre_register")
        else:
            email = request.POST['email']
            encoded_email = urlsafe_base64_encode(force_bytes(email))
            current_domain = get_current_site(request)
            message = render_to_string('users/partials/email_verification.html', {
                'user': email,
                'domain': current_domain.domain,
                'uid': encoded_email,

            })
            print(message)
            send_mail('Please Activate Your Account',
                      message,
                      EMAIL_HOST_USER,
                      [email]
                      )
            messages.success(request, 'Please check your email to continue the registration')
            return redirect('home')

    return render(request, 'users/partials/pre_register.html')
