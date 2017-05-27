from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import (
    DetailView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.shortcuts import render

from .models import UserProfile
from .forms import AccountCreateForm


def get_auth_user(request):
    user = request.user._wrapped if hasattr(
        request.user, '_wrapped') else request.user
    if isinstance(user, User):
        return user
    else:
        user = User.objects.get(username=user.username)
        return user


class AccountListView(LoginRequiredMixin, ListView):
    model = UserProfile
    queryset = UserProfile.objects.all()
    context_object_name = "accounts_list"
    paginate_by = 10


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    context_object_name = "accounts_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AccountCreateForm
    model = UserProfile
    template_name = "accounts/userprofile_form_update.html"

    def get(self, request, *args, **kwargs):
        '''
        Check if user is not admin or not authenticated
        '''
        user = self.get_object()  # UserProfile
        if user.user.username != request.user.username and \
                not request.user.is_staff:
            raise Http404
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        email = form.cleaned_data.get("email")
        user_obj = self.get_object()  # UserProfile
        try:
            user = User.objects.get(userprofile=user_obj)
            user.email = email
            user.save()
        except User.DoesNotExist:
            return render(self.request, "404.html")
        messages.info(self.request, 'Your account was updated.')
        return super().form_valid(form, *args, **kwargs)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    success_url = "/"

    def get(self, request, *args, **kwargs):
        '''
        Check if user is not admin or not authenticated
        '''
        user = get_auth_user(request)
        user_acc = self.get_object()  # UserProfile
        if user_acc.user != user and \
                not request.user.is_staff:
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_acc = self.get_object()
        user = user_acc.user
        user.delete()
        # return redirect("home")
        return self.get_success_url()
