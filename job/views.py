from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.views.generic import (
    DetailView,
    DeleteView,
    ListView,
    UpdateView
)
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render

from .models import JobsInfo
from .forms import JobCreateForm
from accounts.models import UserProfile
from accounts.mixins import StaffRequiredMixin
from accounts.views import get_auth_user
from companys.models import Membership
from companys.mixins import CompanyRequiredMixin


class JobListView(ListView):
    model = JobsInfo
    queryset = JobsInfo.objects.all()
    context_object_name = "jobs_list"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        # iteritem = self.request.GET.lists()
        # for k, v in iteritem:
        #     print(k, v)
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            query = query.strip()
            qs = self.model.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(experience__icontains=query)
            )
        return qs


class JobDetailView(DetailView):
    model = JobsInfo
    context_object_name = "jobs_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_superuser:
            context["job_update_required"] = True
        return context


class JobCreateView(CompanyRequiredMixin, CreateView):
    model = JobsInfo
    form_class = JobCreateForm
    template_name = "job/forms_create.html"
    success_url = "/jobs"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        member = Membership.objects.get(account__user=self.request.user)
        context["membership"] = member
        # use for delete company account
        return context

    def form_valid(self, form, *args, **kwargs):
        super().form_valid(form, *args, **kwargs)
        job_obj = form.instance
        job_obj = form.save(commit=False)
        try:
            user_acc = UserProfile.objects.get(user=self.request.user)
            job_obj.user = user_acc
            membership = Membership.objects.get(account=user_acc)
            job_obj.company = membership.company
            job_obj.save()
        except JobsInfo.DoesNotExist:
            del job_obj
            raise Http404
        return redirect("jobs")


class JobUpdateView(StaffRequiredMixin, UpdateView):
    model = JobsInfo
    form_class = JobCreateForm
    template_name = "job/jobsinfo_form_update.html"
    context_object_name = "job_update"

    def get(self, request, *args, **kwargs):
        user = get_auth_user(request)
        job_obj = self.get_object()
        if job_obj.user != user.userprofile and \
                not request.user.is_staff:
            raise Http404
        messages.info(request, 'Your job was updated.')
        return super().get(request, *args, **kwargs)


class JobDeleteView(StaffRequiredMixin, DeleteView):
    model = JobsInfo

    def get(self, request, *args, **kwargs):
        job_obj = self.get_object()
        user = get_auth_user(request)
        if job_obj.user != user.userprofile and \
                not request.user.is_staff:
            return render(request, '404.html')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("jobs")
