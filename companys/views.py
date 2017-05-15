from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    DetailView, DeleteView, ListView
)
from django.views.generic.edit import CreateView
from django.urls import reverse

from .models import CompanyProfile, Membership
from .forms import CompanyCreateForm
from accounts.models import UserProfile
from accounts.mixins import StaffRequiredMixin
# Create your views here.


class CompanyListView(ListView):
    model = CompanyProfile
    queryset = CompanyProfile.objects.all()
    context_object_name = "companys_list"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # query = self.request.GET.get("q")
        # if query:
        #     qs = self.model.objects.filter(
        #         Q(name__icontains=query) |
        #         # Q(company_set__icontains=query) |
        #         Q(description__icontains=query) |
        #         Q(experience__icontains=query)
        #     )

        return qs


class CompanyDetailView(DetailView):
    model = CompanyProfile
    context_object_name = "companys_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = CompanyProfile
    form_class = CompanyCreateForm
    template_name = "companys/forms_create.html"
    success_url = "/companies"

    def get_user(self, request, *args, **kwargs):
        return request.user

    def form_valid(self, form, *args, **kwargs):
        # save first
        super().form_valid(form, *args, **kwargs)
        # then create `Membership` object
        username = self.request.user.username
        user = User.objects.get(username=username)
        user_acc = UserProfile.objects.get(user=user)
        company = form.instance
        member = Membership(account=user_acc, company=company)
        member.save()
        return redirect(self.success_url)


class CompanyDeleteView(StaffRequiredMixin, DeleteView):
    model = CompanyProfile

    def get_success_url(self):
        return reverse("companies")
