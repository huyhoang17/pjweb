from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import (
    DetailView,
    DeleteView,
    ListView,
    UpdateView,
)
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

    # def get_object(self):
    #     return UserProfile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        '''
        Check if user is not admin or not authenticated
        '''
        user = self.get_object()  # UserProfile
        if user.user.username != request.user.username and \
                not request.user.is_staff:
            raise Http404
        return super().get(request, *args, **kwargs)


class AccountDeleteView(DeleteView):
    model = UserProfile

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
        username = request.user.username
        user_acc = User.objects.filter(username=username).first()
        user_acc.delete()
        logout(request)
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("jobs")
