from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import CollaborationRequest
from .forms import CollaborationForm


class CollaborationCreateView(SuccessMessageMixin, CreateView):
    model = CollaborationRequest
    form_class = CollaborationForm
    template_name = 'collaboration/request_form.html'
    success_url = reverse_lazy('collaboration:request')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "درخواست همکاری شما با موفقیت ثبت شد. به زودی با شما تماس خواهیم گرفت.",
        )
        return response