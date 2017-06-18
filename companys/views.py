from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import (
    DetailView,
    DeleteView,
    ListView,
    UpdateView
)
from django.views.generic.edit import CreateView
from django.urls import reverse

from .models import CompanyProfile, Membership
from .forms import CompanyCreateForm
from accounts.models import UserProfile
from accounts.views import get_auth_user
from job.models import JobsInfo


class CompanyListView(LoginRequiredMixin, ListView):
    model = CompanyProfile
    queryset = CompanyProfile.objects.all()
    context_object_name = "companys_list"
    paginate_by = 10


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = CompanyProfile
    context_object_name = "companys_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_acc = self.request.user.userprofile
        company_obj = self.get_object()
        try:
            Membership.objects.get(
                company=company_obj,
                account=user_acc
            )
            context["company_update_required"] = True
        except Membership.DoesNotExist:
            if user_acc.user.is_staff:
                context["company_update_required"] = True
            pass
        company = self.get_object()
        jobs_company = JobsInfo.objects.filter(
            company=company).filter(active=True)
        context["jobs_company"] = jobs_company
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = CompanyProfile
    form_class = CompanyCreateForm
    template_name = "companys/forms_create.html"
    success_url = "/companies"

    def form_valid(self, form, *args, **kwargs):
        # save first
        super().form_valid(form, *args, **kwargs)
        # then create `Membership` object
        user_acc = UserProfile.objects.get(user=self.request.user)
        company = form.instance
        member = Membership(account=user_acc, company=company)
        member.save()

        company_info_required = self.request.session.get(
            "company_info_required", None
        )
        if company_info_required:
            del self.request.session["company_info_required"]
            return redirect("create_jobs")
        return redirect(self.success_url)


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyProfile
    form_class = CompanyCreateForm
    template_name = "companys/companyprofile_form_update.html"
    context_object_name = "company_update"

    def get(self, request, *args, **kwargs):
        user = get_auth_user(request)
        company_obj = self.get_object()
        try:
            membership = Membership.objects.get(account=user.userprofile)
            company_pk = membership.company.pk
            if not request.user.is_staff:
                if company_pk != company_obj.pk:
                    raise Http404
        except Membership.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = CompanyProfile

    def get(self, request, *args, **kwargs):
        company_obj = self.get_object()
        user = get_auth_user(request)
        try:
            membership = Membership.objects.get(account=user.userprofile)
            company_pk = membership.company.pk
            if not request.user.is_staff:
                if company_pk != company_obj.pk:
                    raise Http404
        except Membership.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("companies")
