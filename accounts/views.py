from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import (
    DetailView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.shortcuts import render, redirect

from .models import UserProfile
from .forms import AccountCreateForm


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
        return super().form_valid(form, *args, **kwargs)


class AccountDeleteView(DeleteView):
    model = UserProfile
    success_url = "/"

    def get(self, request, *args, **kwargs):
        '''
        Check if user is not admin or not authenticated
        '''
        user = self.get_object()  # UserProfile
        if user.user.username != request.user.username and \
                not request.user.is_staff:
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_acc = self.get_object()
        user = user_acc.user
        user.delete()
        return redirect("home")
