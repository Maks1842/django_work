from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Departments, Regions
from .forms import DepartmentsForm
# from .utils import MyMixin


class HomeDepartments(ListView):           # Данный класс заменяет контроллер функции >>> def index(request):
    model = Departments                    # Указываю из какой Модели буду получать данныу
    template_name = 'checklist/department_list.html'
    context_object_name = 'department'
    # queryset = Departments.objects.select_related('department_name')          # Данный атрибут указывается здесь, если отсутствует метод def get_queryset(self):. Если этот метод есть в классе, то атрибут указывать там
    # mixin_prop = 'hello world'
    #
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    # def get_queryset(self):
    #     return News.objects.filter(is_published=True).select_related('category')


# class ViewDepartments(DetailView):         # Данный класс заменяет контроллер функции >>> def view_news(request, news_id):
#     model = Departments                    # Указываю из какой Модели буду получать данные
#     context_object_name = 'department'



# class CreateChecklist(CreateView):         # Данный класс заменяет контроллер функции >>> def add_news(request):
#     form_class = DepartmentsForm                   # Связываю форму с существующей моделью
#     template_name = 'checklist/library.html'
#     success_url = reverse_lazy('library')      # После сохранения данных, перенаправляет пользователя по указанному адресу. По умолчанию (без данного метода) редирект происходит на текущую страницу
#     # login_url = '/admin/'                 # Вариант 1 - перенаправляет на Админку
#     # login_url = reverse_lazy('library')        # Вариант 2 - перенаправляет на указанную страницу