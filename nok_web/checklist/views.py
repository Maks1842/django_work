from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

# from .models import News, Category
# from .forms import NewsForm
# from .utils import MyMixin


def index(request):
    # print(dir(request))
    return HttpResponse('Hello world')