from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
import re


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


def get_act(request, type_departments=1, type_organisations='2|3'):

    form_act = []
    count = 0

    form_sections = Form_Sections.objects.values().filter(type_departments=type_departments) | Form_Sections.objects.values().filter(type_departments=None)
    questions = Questions.objects.values()
    type_answers = Type_Answers.objects.values()
    question_values = Question_Values.objects.values()

    for fs in form_sections:
        fs_id = fs['id']
        questions_id = questions.filter(form_sections_id=fs_id)
        count_section = 0
        pages = []

        for q in questions_id:
            choices = []
            count_section += 1

            if re.findall(type_organisations, str(q['type_organisations'])) or q['type_organisations'] is None:
                count += 1
                type = type_answers.get(pk=q['type_answers_id'])
                answer_variant = q['answer_variant']
                ans_var_re = answer_variant
                try:
                    ans_var_re = (re.sub(r'\s', '', answer_variant))
                except:
                    pass

                ans_var = ans_var_re.split(',')

                for av in range(len(ans_var)):
                    qv = question_values.get(pk=ans_var[av])
                    choices.append({'value': ans_var[av], 'text': qv['value_name']})


                pages.append({
                    "name": str(count),
                    "title": q['name'],
                    "type": type['type'],
                    "choices": choices,
                    "isRequired": 'true',
                    # 'test': len(questions_id),
                    # 'test2': count_section
                })

            if len(pages) == 4 or len(questions_id) == count_section:
                form_act.append({
                    "title": fs['name'],
                    "elements": pages,
                })
                pages = []

    context = {"pages": form_act}

    return render(request, 'checklist/helper.html', context)


# Добавление данных в БД
def forms_act_add(request):
    if request.method == 'POST':
        # Данная строка создает Форму связанную с данными Модели
        form = FormsActForm(request.POST)
        # Проверяю прошла ли Форма валидацию
        if form.is_valid():
            # Сохраняются в БД
            form.save()
            return redirect('home')
    else:
        form = FormsActForm()
    return render(request, 'checklist/designer_act.html', {'form': form})


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





