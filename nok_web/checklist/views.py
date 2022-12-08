from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .app_forms.forms_act_form import FormsActForm
# from .app_models import FormsAct, List_Checking, Answers, Regions, Departments, Organisations
from .app_models import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
import re
import json


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


def organisation_view(request):
    organisations = Organisations.objects.order_by('pk')
    type_organisations = Type_Organisations.objects.order_by('pk')
    checking = Checking.objects.order_by('pk')
    context = {
        'organisations': organisations,
        'type_organisations': type_organisations,
        'checking': checking,
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
    return render(request, 'checklist/helper.html', context)


def get_act(request, type_departments=1, type_organisations=3, number_items=0):
    type_departments = request.POST['type_dep']
    type_organisations = request.POST['type_org']
    version_act = request.POST['version']

    form_act = []
    count = 0

    form_sections = Form_Sections.objects.values().order_by('order_num').filter(
        type_departments=type_departments) | Form_Sections.objects.values().order_by('order_num').filter(
        type_departments=None)
    form_sections_question = Form_Sections_Question.objects.values().order_by('order_num')
    questions = Questions.objects.values()
    type_answers = Type_Answers.objects.values()
    question_values = Question_Values.objects.values()

    for fs in form_sections:
        fs_id = fs['id']
        questions_id = form_sections_question.filter(form_sections_id=fs_id)
        count_section = 0
        pages = []

        for q in questions_id:
            choices = []
            count_section += 1

            if q['type_organisations'] is None:
                count += 1
                type = type_answers.get(pk=q['type_answers_id'])
                question = questions.get(pk=q['question_id'])
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
                    "title": question['questions'],
                    "type": type['type'],
                    "choices": choices,
                    "isRequired": 'true',
                })

            elif str(type_organisations) in q['type_organisations'].split(','):
                count += 1
                type = type_answers.get(pk=q['type_answers_id'])
                question = questions.get(pk=q['question_id'])
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
                    'name': str(count),
                    'title': question['questions'],
                    'type': type['type'],
                    'choices': choices,
                    'isRequired': 'true',
                })

        if len(pages) == number_items or len(questions_id) == count_section:
            form_act.append({
                "title": fs['name'],
                "elements": pages,
            })

    xxx = json.dumps({"pages": form_act}, ensure_ascii=False)
    context = {"form_act": xxx}

    # element = FormsAct(type_departments=2, type_organisations=10, act_json=context, version=version_act)
    # element.save()

    return render(request, 'checklist/helper.html', context)


'''
Рендеринг результатов проверки в шаблон HTML.
do_some_magic - предварительно сопоставляет json-структура акта и json-результаты ответов
'''


def get_act_answer(request):
    org_id = request.POST["org_id"]
    type_org_id = request.POST["type_org_id"]
    check_id = request.POST["check_id"]

    # Необходим рефакторинг: записать запрос к FormsAct по id_organisation одной строкой
    # type_organisations = Organisations.objects.get(pk=org_id).type_organisations_id
    name_org = Organisations.objects.get(pk=org_id).organisation_name
    address_org = Organisations.objects.get(pk=org_id).address
    user = List_Checking.objects.filter(organisation_id=org_id).get(checking_id=check_id).user  # Имя проверяющего
    # person = Form_Organisation_Persons.objects.get(organisation_id=org_id).person  # Представитель проверяемой организации
    queryset = FormsAct.objects.filter(type_organisations_id=type_org_id)
    temp = Templates.objects.get(type_organisations_id=type_org_id).template_file

    if len(queryset) > 0:
        form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
        query = Question_Values.objects.values()

        comparison = do_some_magic(form_json, org_id, type_org_id, check_id)
        answers = answer_in_the_act(comparison, query)
    context = {'name_org': name_org,
               'address_org': address_org,
               'user': user,
               # 'person': person,
               'answers': answers}

    return render(request, f'act_checkings/{temp}', context)


'''
Функция сравнения двух json.
Производится сопоставление полученных ответов с имеющимеся вопросами.
На выходе формируется новый json, где:
- если один из ответов совпадает с вопросом, то ячейки без совпадения остаются пустые, в ячейках с совпадением проставляется номер ответа;
- если нет ни одного совпадения, то все ячейки остаются пустые.
В формируемом json количество объектов в списке равно количеству объектов списка с вопросами.
'''


def do_some_magic(form_json, org_id, type_org_id, check_id):

    act = form_json
    act_answer = Answers.objects.filter(checking_id=check_id, type_organisations=type_org_id).get(organisations_id=org_id).answers_json

    questions = {}
    for page in act['pages']:
        for element in page['elements']:
            choices = []
            for choice in element['choices']:
                choices.append(choice['value'])
            questions[element['name']] = choices

    tt = {}

    for question in act_answer:
        sh = []
        for answer in questions[question]:
            if answer in act_answer[question]:
                sh.append(answer)
            else:
                sh.append('')
        tt[question] = sh
    z = questions.copy()
    z.update(tt)
    for question in z:
        if question not in act_answer:
            for i in range(len(z[question])):
                z[question][i] = ''

    return z


'''
Функция формирования текстовых ответов для HTML шаблона из json файла,
который сформирован на основе сопоставления act_json и answer_json.
'''


def answer_in_the_act(comparison, query):
    list = {}

    for answ in comparison:
        answer = ''
        answers = []
        if '11' in comparison[answ] or '12' in comparison[answ]:
            for a in comparison[answ]:
                if a == '':
                    answer = "Нет"
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                answers.append(answer)
        else:
            for a in comparison[answ]:
                if a == '':
                    pass
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                    answers.append(answer)
        list[answ] = answers

    return list


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


def forms_test_add(request):
    type_departments = request.POST['type_dep']
    type_organisations = request.POST['type_org']

    context = {'type_depr': type_departments,
               'type_orgn': type_organisations}
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
