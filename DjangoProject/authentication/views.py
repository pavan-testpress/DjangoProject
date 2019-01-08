from django.contrib.auth import authenticate, login as mylogin, logout as mylogout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token, password_reset_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes


from .forms import UserCreationForm, SetPasswordForm
from .models import MyUser
# Create your views here.


def index(request):
    if str(request.user) == 'AnonymousUser':
        return HttpResponseRedirect(reverse('authentication:login'))
    else:
        return render(request, 'authentication/index.html')


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('authentication:index'))
    else:
        if request.method == 'GET':
            template = 'authentication/login.html'
            return render(request, template)
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                mylogin(request, user)
                return HttpResponseRedirect(reverse('authentication:index'))
            else:
                return render(request, "authentication/invalidlogin.html")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        mylogin(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('authentication:index'))
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('authentication/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your account.'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = UserCreationForm()
        return render(request, 'authentication/signup.html', {'form': form})


def logout(request):
    mylogout(request)
    return HttpResponseRedirect(reverse('authentication:login'))


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'authentication/forgot_password.html')
    else:
        try:
            user = MyUser.objects.get(email=request.POST['email'])
            if user:
                current_site = get_current_site(request)
                message = render_to_string('authentication/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': password_reset_token.make_token(user),
                })
                mail_subject = 'Password Reset.'
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please reset your password through the link sent to your mail.')
        except:
            return render(request, 'authentication/forgot_password.html', {'error': 'Given mail does not exist.'})


def password_reset(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = MyUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None
        if user is not None and password_reset_token.check_token(user, token):
            if request.method == "POST":
                form = SetPasswordForm(data=request.POST, user=user)
                if form.is_valid():
                    form.save()
                    mylogin(request, user)
                    return HttpResponseRedirect(reverse('authentication:index'))
                else:
                    print(form.errors)
            else:
                form = SetPasswordForm(user)
            return render(request, 'authentication/forgot_password_form.html', {'form': form})
        else:
            return HttpResponse('Password Reset link is invalid!')
