from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, FormView
from django.shortcuts import redirect, render

from .models import Newsletters
from .forms import NewslettersForm, ContactForm
from companys.models import CompanyProfile
from job.models import JobsInfo


class HomeView(ListView):
    model = JobsInfo
    template_name = "home.html"
    context_object_name = "jobs_list"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            return redirect("/jobs/?q={}".format(query))
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["companys_list"] = CompanyProfile.objects.all()[:10]
        return context


class NewslettersView(FormView):
    form_class = NewslettersForm
    template_name = 'newsletters.html'
    success_url = '/newsletter/'

    def form_valid(self, form, *args, **kwargs):
        fullname = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        if Newsletters.objects.filter(email=email).exists():
            context = {
                "email_subcribed": True
            }
            return render(self.request, self.template_name, context)
        newsletter = Newsletters(full_name=fullname, email=email)
        newsletter.save()
        context = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            self.template_name,
            context
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        form = self.get_form()
        if form.is_valid():
            context["confirm_message"] = "Thank you for your subcribe !"
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context["form"]
        if form.is_valid():
            cd = context['form'].cleaned_data
            subject = cd["subject"]
            from_email = cd['email']
            message = cd['message']

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [settings.EMAIL_HOST_USER]
                )
            except Exception:
                return HttpResponse('Invalid header found.')

            context = {
                "success_message": "Thank you!."
            }
            return render(request, self.template_name, context)
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        form = ContactForm(self.request.POST or None)
        context['form'] = form
        return context
