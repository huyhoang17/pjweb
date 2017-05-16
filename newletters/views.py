from django.views.generic import FormView
from django.views.generic import ListView
from django.shortcuts import redirect

from .models import Newsletters
from .forms import NewslettersForm
from job.models import JobsInfo
# Create your views here.

from companys.models import CompanyProfile


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

    def dispatch(self, request, *args, **kwargs):
        # form = self.get_form()
        # print(form.clean)
        # print(form.cleaned_data["email"])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(dir(self))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        fullname = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        newsletter = Newsletters(full_name=fullname, email=email)
        newsletter.save()
        # context = self.get_context_data(*args, **kwargs)
        # return render(
        #     self.request,
        #     self.template_name,
        #     context
        # )
        return super().form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["confirm_message"] = "Thank you for your subcribe !"
        return context


# class ContactView(FormView):
#     form_class = ContactForm
#     template_name = 'contact.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["message"] = "Thank You"
#         return context

#     def form_valid(self, form, *args, **kwargs):
#         full_name = form.cleaned_data.get("full_name")
#         email = form.cleaned_data.get("email")
#         message = form.cleaned_data.get("message")

#         subject = 'Site contact form'
#         from_email = settings.EMAIL_HOST_USER
#         to_email = [email]
#         contact_message = "{}: {} via {}".format(
#             full_name,
#             message,
#             email
#         )
#         html_message = """
#             <h1>Thank You</h1>
#         """
#         send_mail(subject,
#                   contact_message,
#                   from_email,
#                   to_email,
#                   html_message=html_message,
#                   fail_silently=True)

#         return super().form_valid(form, *args, **kwargs)

#     def get_template_names(self):
#         return [self.template_name]

#     def get_success_url(self, *args, **kwargs):
#         return "/contact/"
