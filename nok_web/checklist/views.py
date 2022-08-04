from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Department, Region
from .forms import ChecklistForm
# from .utils import MyMixin


def index(request):
    department = Department.objects.all()   #Если необходимо отображать объекты в порядке как в ДБ
    context = {
        'department': department,
        'title': 'Департаменты',
    }
    return render(request, 'checklist/index.html', context)


class CreateChecklist(CreateView):         # Данный класс заменяет контроллер функции >>> def add_news(request):
    form_class = ChecklistForm                   # Связываю форму с существующей моделью
    template_name = 'checklist/library.html'
    success_url = reverse_lazy('library')      # После сохранения данных, перенаправляет пользователя по указанному адресу. По умолчанию (без данного метода) редирект происходит на текущую страницу
    # login_url = '/admin/'                 # Вариант 1 - перенаправляет на Админку
    # login_url = reverse_lazy('library')        # Вариант 2 - перенаправляет на указанную страницу