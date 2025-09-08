from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from .tokens import account_activation_token

User = get_user_model()

def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    url = request.build_absolute_uri(reverse('activate', args=[uid, token]))
    send_mail(
        'Verify your email',
        f'Click to verify: {url}',
        None,
        [user.email],
        fail_silently=False,
    )

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    return render(request, 'accounts/activate_invalid.html')

def activate_sent(request):
    return render(request, 'accounts/activate_sent.html')
