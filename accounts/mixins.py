from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import Http404


class StaffRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_authenticated():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
