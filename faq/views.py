from django.shortcuts import render
from django.views.generic import *

from .models import Faq
# Create your views here.


class FaqListView(ListView):
    model = Faq
    template_name = 'faq/faq_list.html'
    context_object_name = 'faqs'
    paginate_by = 10

