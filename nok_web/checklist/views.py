from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import *
# from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse


# Регистрация пользователя
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         # if form.is_valid():                           ## V1 - после регистарции перенаправляем на страницу авторизации
#         #     form.save()
#         #     messages.success(request, 'Вы успешно зарегистрировались')   # Сообщение для пользователя из формы
#         #     return redirect('login')                                     ## V1 - После успешной регистрации перенаправить на страницу Авторизации
#
#         if form.is_valid():                             ## V2 - после регистрации сразу авторизуем
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Вы успешно зарегистрировались')
#             return redirect('home')                     # После успешной авторизации можно перенаправить куда-нибудь пользователя (например на главную страницу)
#
#         else:
#             messages.error(request, 'Ошибка регистрации')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'checklist/register.html', {"form": form})
#
#
# # Авторизация пользователя
# def user_login(request):
#     if request.method == 'POST':                            # Если данные к нам пришли методом 'POST'
#         form = UserLoginForm(data=request.POST)             # Тогда создаем экземпляр формы и связываем его с данными (обязательно указать data=)
#         if form.is_valid():                                 # Проверяем, если форма валидна
#             user = form.get_user()                          # то можно авторизовать пользователя. Для этого его нужно получить с помощью .get_user()
#             login(request, user)                            # далее в метод login передаю объект Юзера
#             return redirect('home')                         # После успешной авторизации можно перенаправить куда-нибудь пользователя (например на главную страницу)
#     else:
#         form = UserLoginForm()                              # Если данные пришли не методом 'POST', то просто создать объект формы не связанный с данными
#
#     return render(request, 'checklist/login.html', {'form': form})     # и далее в шаблон html передаем форму , {'form': form}
#
#
# # Выход пользователя из учетки
# def user_logout(request):
#     logout(request)
#     return redirect('login')



# Тренировочная вьюха
def region_view(request):
    regions = Regions.objects.order_by('pk')
    departments = Departments.objects.order_by('pk')
    context = {
        'regions': regions,
        'departments': departments,
    }
    return render(request, 'checklist/select_list.html', context)

# Тренировочная вьюха
def organisation_view(request, organisations_id):                  # Откуда приходит позиционный элемент organisations_id??? Из html ???
    organisations = Organisations.objects.get(pk=organisations_id)
    # organisations = Organisations.objects.order_by('pk')
    context = {
        'organisations': organisations,
    }
    return render(request, 'checklist/select_list.html', context)

# Тренировочная вьюха
def question_view(request):
    form_sections = Form_Sections.objects.order_by('pk')
    questions = Questions.objects.order_by('pk')
    question_values = Question_Values.objects.order_by('pk')
    context = {
        'form_sections': form_sections,
        'questions': questions,
        'question_values': question_values,
    }
    return render(request, 'checklist/check_list.html', context)


def designer_act_view(request):
    type_departments = Type_Departments.objects.order_by('pk')
    type_organisations = Type_Organisations.objects.order_by('pk')
    context = {
        'type_departments': type_departments,
        'type_organisations': type_organisations,
    }
    return render(request, 'checklist/designer_act.html', context)


# Тренировочная вьюха
class HomeDepartments(ListView):
    model = Departments
    template_name = 'checklist/department_list.html'
    context_object_name = 'department'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

# Тренировочная вьюха
class LibDepartments(ListView):
    model = Departments
    template_name = 'checklist/department_add_list.html'
    context_object_name = 'department'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Другая страница'
        return context





