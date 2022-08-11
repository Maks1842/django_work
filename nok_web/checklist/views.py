from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Departments, Regions
from .forms import UserRegisterForm, UserLoginForm
# from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout


def index(request):
    return render(request, 'checklist/index.html')


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # if form.is_valid():                           ## V1 - после регистарции перенаправляем на страницу авторизации
        #     form.save()
        #     messages.success(request, 'Вы успешно зарегистрировались')   # Сообщение для пользователя из формы
        #     return redirect('login')                                     ## V1 - После успешной регистрации перенаправить на страницу Авторизации

        if form.is_valid():                             ## V2 - после регистрации сразу авторизуем
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')                     # После успешной авторизации можно перенаправить куда-нибудь пользователя (например на главную страницу)

        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'checklist/register.html', {"form": form})


# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':                            # Если данные к нам пришли методом 'POST'
        form = UserLoginForm(data=request.POST)             # Тогда создаем экземпляр формы и связываем его с данными (обязательно указать data=)
        if form.is_valid():                                 # Проверяем, если форма валидна
            user = form.get_user()                          # то можно авторизовать пользователя. Для этого его нужно получить с помощью .get_user()
            login(request, user)                            # далее в метод login передаю объект Юзера
            return redirect('home')                         # После успешной авторизации можно перенаправить куда-нибудь пользователя (например на главную страницу)
    else:
        form = UserLoginForm()                              # Если данные пришли не методом 'POST', то просто создать объект формы не связанный с данными

    return render(request, 'checklist/login.html', {'form': form})     # и далее в шаблон html передаем форму , {'form': form}


# Выход пользователя из учетки
def user_logout(request):
    logout(request)
    return redirect('login')


class HomeDepartments(ListView):
    model = Departments
    template_name = 'checklist/department_list.html'
    context_object_name = 'department'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class LibDepartments(ListView):
    model = Departments
    template_name = 'checklist/department_add_list.html'
    context_object_name = 'department'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Другая страница'
        return context





# class ViewDepartments(DetailView):         # Данный класс заменяет контроллер функции >>> def view_news(request, news_id):
#     model = Departments                    # Указываю из какой Модели буду получать данные
#     # template_name = 'checklist/department_add_list.html'
#     context_object_name = 'department'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Другая страница'
#         return context



# class CreateChecklist(CreateView):         # Данный класс заменяет контроллер функции >>> def add_news(request):
#     form_class = DepartmentsForm                   # Связываю форму с существующей моделью
#     template_name = 'checklist/library.html'
#     success_url = reverse_lazy('library')      # После сохранения данных, перенаправляет пользователя по указанному адресу. По умолчанию (без данного метода) редирект происходит на текущую страницу
#     # login_url = '/admin/'                 # Вариант 1 - перенаправляет на Админку
#     # login_url = reverse_lazy('library')        # Вариант 2 - перенаправляет на указанную страницу


# def view_departments(request, departments_id):
#     departments_id = 1
#     department = Departments.objects.get(pk=departments_id)                           #V1
# #     news_item = get_object_or_404(News, pk=news_id)                     #V2 с обработчиком ошибки некорректного адреса страницы
#     return render(request, 'checklist/department_add_list.html', {"department": department})