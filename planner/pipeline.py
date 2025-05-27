from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def reject_unknown_user(strategy, details, backend, uid, user=None, *args, **kwargs):
    email = details.get('email')
    try:
        user = User.objects.get(email=email)
        return {'user': user}
    except User.DoesNotExist:
        return redirect('planner:login_error')