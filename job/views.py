from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, DeleteView, ListView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render

from .models import JobsInfo
from .forms import JobCreateForm
from accounts.models import UserProfile
from accounts.mixins import StaffRequiredMixin
from companys.models import Membership
from companys.mixins import CompanyRequiredMixin


class JobListView(ListView):
    model = JobsInfo
    queryset = JobsInfo.objects.all()
    context_object_name = "jobs_list"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

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

    def get_object(self, *args, **kwargs):
        return super().get_object(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class JobCreateView(CompanyRequiredMixin, CreateView):
    model = JobsInfo
    form_class = JobCreateForm
    template_name = "job/forms_create.html"
    success_url = "/jobs"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)

    # def get_form_kwargs(self):
    #     '''
    #     Use to send request(user) in ModelForm
    #     '''
    #     kwargs = super().get_form_kwargs()
    #     username = self.request.user.username
    #     membership = Membership.objects.get(account__user__username=username)
    #     kwargs["instance"] = membership.company
    #     return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        member = Membership.objects.get(account__user=user)
        # use for delete company account
        context["membership"] = member
        return context

    def form_valid(self, form, *args, **kwargs):
        super().form_valid(form, *args, **kwargs)
        job_obj = form.instance
        job_obj = form.save(commit=False)
        username = self.request.user.username
        try:
            user = UserProfile.objects.get(user__username=username)
            job_obj.user = user
            membership = Membership.objects.get(account=user)
            job_obj.company = membership.company
            job_obj.save()
        except JobsInfo.DoesNotExist:
            del job_obj
            raise Http404
        return redirect("jobs")


class JobDeleteView(StaffRequiredMixin, DeleteView):
    model = JobsInfo

    def get(self, request, *args, **kwargs):
        job_obj = self.get_object()
        user = request.user._wrapped if hasattr(
            request.user, '_wrapped') else request.user  # User
        if job_obj.user != user.userprofile:
            return render(request, '404.html')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("jobs")
