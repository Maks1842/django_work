from django.shortcuts import render, redirect
from .app_forms.forms_act_form import FormsActForm
from .app_models import *


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


def designer_act_view(request):
    type_departments = Type_Departments.objects.order_by('pk')
    type_organisations = Type_Organisations.objects.order_by('pk')
    context = {
        'type_departments': type_departments,
        'type_organisations': type_organisations,

    }
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