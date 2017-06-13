from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .models import Membership


class CompanyRequiredMixin(object):

    def __init__(self):
        self.template_name = "job/forms_create.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request.session['company_info_required'] = True
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            if not Membership.objects.filter(account__user=user).exists():
                return redirect("create_companies")
        except AttributeError:
            return render(self.request, self.template_name)
        return super().dispatch(request, *args, **kwargs)
