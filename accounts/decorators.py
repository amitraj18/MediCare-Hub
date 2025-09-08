from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login

def role_required(*allowed_roles):
    def wrapper(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('You do not have permission to access this page.')
        return _wrapped
    return wrapper

patient_required = role_required('PATIENT')
doctor_required  = role_required('DOCTOR')
admin_required   = role_required('ADMIN')
