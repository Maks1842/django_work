from ..app_models import *
from django.template.loader import render_to_string
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser

from weasyprint import HTML, CSS

"""ОГРАНИЧЕНИЯ ДОСТУПА:
Дефолтные permissions:
AllowAny - полный доступ;
IsAdminUser - только для Администраторов;
IsAuthenticated - только для авторизованных пользователей;
IsAuthenticatedOrReadOnly - только для авторизованных или всем, но для чтения.

Кастомные permissions:
IsAdminOrReadOnly - запись может просматривать любой, а удалять только Администратор;
IsOwnerAndAdminOrReadOnly - запись может менять только пользователь который её создал и Админ, просматривать может любой.
"""


'''
Рендеринг результатов проверки в шаблон HTML с последующим сохранением в pdf.
- do_some_magic - функция предварительно сопоставляет json-структуру акта и json-результаты ответов;
- answer_in_the_act - Функция генерации данных для HTML шаблона.
'''


class GetResultCheckingIntoPdfAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        method='get',
        tags=['Результаты проверки'],
        operation_description="Получить Акт с результатами проверки в формате pdf. "
                              "Предварительно сопоставляется json-структура акта и json-результаты ответов",
        manual_parameters=[
            openapi.Parameter('checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'],)
    def get(self, request):

        checking = request.query_params.get('checking')
        organisation = request.query_params.get('organisation')
        type_organisation = request.query_params.get('type_organisation')

        name_org = Organisations.objects.get(pk=organisation).organisation_name
        address_org = Organisations.objects.get(pk=organisation).address
        # Получаю Имя проверяющего
        try:
            user = List_Checking.objects.filter(organisation_id=organisation).get(checking_id=checking).user
        except:
            return Response({
                'error': 'Данные о проверке или об организации неверны. Проверьте правильность сопоставления проверки и организации'})
        # Получаю Представителя проверяемой организации
        # person = Form_Organisation_Persons.objects.get(organisation_id=organisation).person

        queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)
        if len(queryset) == 0:
            return Response({'error': 'Не найден указанный тип организации'})

        temp = Templates.objects.get(type_organisations_id=type_organisation).template_file
        if temp == '':
            return Response({'error': 'Не найден шаблон Акта для данного типа организации. '
                                      'Обратитесь к Администратору'})

        try:
            act_answer = Answers.objects.filter(
                checking_id=checking,
                type_organisations=type_organisation
            ).get(organisations_id=organisation).answers_json
        except:
            return Response({'error': 'Не найдены данные о результатах запрашиваемой проверки.'})

        form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
        query = Question_Values.objects.values()

        comparison = do_some_magic(form_json, act_answer)
        answers = answer_in_the_act(comparison, query)

        context = {'name_org': name_org,
                   'address_org': address_org,
                   'user': user,
                   # 'person': person,
                   'answers': answers}

        name_org = context['name_org']

        content = render_to_string(f'act_checkings/{temp}', context)
        css = CSS(string='@page { size: A4 !important; '
                         'margin-left: 1cm !important; '
                         'margin-right: 1cm !important; '
                         'margin-top: 1.5cm !important;'
                         'margin-bottom: 1.5cm !important }')
        HTML(string=content).write_pdf(f'./checklist/local_storage/{name_org}.pdf', stylesheets=[css])
        # отдаем сохраненный pdf в качестве ответа
        file_pointer = open(f'./checklist/local_storage/{name_org}.pdf', "rb")
        response = HttpResponse(file_pointer, content_type='application/pdf;')
        response['Content-Disposition'] = f'attachment; filename=download.pdf'
        response['Content-Transfer-Encoding'] = 'utf-8'

        # return response


        return Response(comparison)

'''
Функция сравнения двух json.
Производится сопоставление полученных ответов с имеющимся вопросами.
На выходе формируется новый json, где:
- если один из ответов совпадает с вопросом, то ячейки без совпадения остаются пустые, в ячейках с совпадением проставляется номер ответа;
- если нет ни одного совпадения, то все ячейки остаются пустые.
В формируемом json количество объектов в списке равно количеству объектов списка с вопросами.
'''


def do_some_magic(form_json, act_answer):
    act = form_json
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
    list_dict = {}

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
                    answer = "Нет"
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                answers.append(answer)
        list_dict[answ] = answers

    return list_dict
