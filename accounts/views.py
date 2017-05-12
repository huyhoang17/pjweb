from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import (
    DetailView,
    DeleteView,
    ListView,
    UpdateView
)

from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render

from .models import UserProfile
from .forms import AccountCreateForm
# Create your views here.


class AccountListView(ListView):
    model = UserProfile
    queryset = UserProfile.objects.all()
    context_object_name = "accounts_list"
    paginate_by = 10


class AccountDetailView(DetailView):
    model = UserProfile
    context_object_name = "accounts_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class AccountUpdateView(UpdateView):
    form_class = AccountCreateForm
    model = UserProfile
    template_name = "accounts/userprofile_form_update.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class AccountDeleteView(DeleteView):
    model = UserProfile

    def post(self, request, *args, **kwargs):
        username = request.user.username
        user_acc = User.objects.filter(username=username).first()
        user_acc.delete()
        logout(request)
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("jobs")
