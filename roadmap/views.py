from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class RoadmapView(TemplateView):
    template_name = 'roadmap/roadmap.html'