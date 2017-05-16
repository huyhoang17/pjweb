from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .models import Membership
from accounts.models import UserProfile


class CompanyRequiredMixin(object):

    def __init__(self):
        self.template_name = "job/forms_create.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        user = User.objects.get(username=username)
        user_acc = UserProfile.objects.get(user=user)
        try:
            member = Membership.objects.filter(account=user_acc)
            if member.count() == 0:
                return redirect('/companies/create/')
        except AttributeError:
            return render(self.request, self.template_name)
        return super().dispatch(request, *args, **kwargs)
