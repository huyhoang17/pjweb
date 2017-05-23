from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import (
    DetailView, DeleteView, ListView
)
from django.views.generic.edit import CreateView
from django.urls import reverse

from .models import CompanyProfile, Membership
from .forms import CompanyCreateForm
from accounts.models import UserProfile
from job.models import JobsInfo


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
        company = self.get_object()
        jobs_company = JobsInfo.objects.filter(company=company)[:5]
        context["jobs_company"] = jobs_company
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
        user_acc = UserProfile.objects.get(user__username=username)
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


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = CompanyProfile

    def get(self, request, *args, **kwargs):
        company_obj = self.get_object()
        user = request.user._wrapped if hasattr(
            request.user, '_wrapped') else request.user  # User
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
