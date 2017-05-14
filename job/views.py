from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import DetailView, DeleteView, ListView
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, get_object_or_404, redirect

from .models import JobsInfo
from .mixins import StaffRequiredMixin
from .forms import JobCreateForm
from companys.mixins import CompanyRequiredMixin
# Create your views here.


class JobListView(ListView):
    model = JobsInfo
    queryset = JobsInfo.objects.all()
    context_object_name = "jobs_list"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(name__icontains=query) |
                # Q(company_set__icontains=query) |
                Q(description__icontains=query) |
                Q(experience__icontains=query)
            )
        return qs


class JobDetailView(DetailView):
    model = JobsInfo
    context_object_name = "jobs_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class JobCreateView(LoginRequiredMixin, CompanyRequiredMixin, CreateView):
    form_class = JobCreateForm
    template_name = "job/forms_create.html"
    success_url = "/jobs"
    template_success = "job/jobsinfo_list.html"

    def form_valid(self, form, *args, **kwargs):
        return super().form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["company_login_required"] = True
        return context


class JobDeleteView(StaffRequiredMixin, DeleteView):
    model = JobsInfo

    def get_success_url(self):
        return reverse("jobs")
