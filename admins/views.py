from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render

from users.models import UserRegistrationModel


def admin_required(view):
    """Only let in admins who logged in through AdminLoginCheck."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.success(request, 'Please log in as admin first')
            return redirect('AdminLogin')
        return view(request, *args, **kwargs)
    return wrapper


def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        # Admins are Django superusers: create one with `python manage.py createsuperuser`.
        user = authenticate(request, username=usrid, password=pswd)
        if user is not None and user.is_superuser:
            request.session.cycle_key()
            request.session['is_admin'] = True
            return render(request, 'admins/AdminHome.html')
        messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


@admin_required
def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/RegisteredUsers.html', {'data': data})


@admin_required
def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        UserRegistrationModel.objects.filter(id=id).update(status=status)
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/RegisteredUsers.html', {'data': data})


@admin_required
def AdminHome(request):
    return render(request, 'admins/AdminHome.html')
