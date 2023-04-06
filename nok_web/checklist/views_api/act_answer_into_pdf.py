from ..app_models import *
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser
from .magic import do_some_magic, answer_in_the_act

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
            list_check_set = List_Checking.objects.filter(organisation_id=organisation).get(checking_id=checking)
        except:
            return Response({
                'error': 'Данные о проверке или об организации неверны. Проверьте правильность сопоставления проверки и организации'})
        # Получаю Представителя проверяемой организации
        # person = Form_Organisation_Persons.objects.get(organisation_id=organisation).person

        queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)
        if len(queryset) == 0:
            return Response({'error': 'Не найден указанный тип организации'})

        temp = Templates.objects.filter(type_templates_id=1).get(type_organisations_id=type_organisation).template_file
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

        user_set = User.objects.values().get(pk=list_check_set.user_id)
        user_name = f"{user_set['first_name']} {user_set['last_name']}"

        context = {'name_org': name_org,
                   'address_org': address_org,
                   'date': list_check_set.date_check_org,
                   'user': user_name,
                   'person': list_check_set.person,
                   'answers': answers}

        name_org = context['name_org']

        content = render_to_string(f'act_checkings/{temp}', context)
        HTML(string=content).write_pdf(f'./checklist/local_storage/{name_org}.pdf', stylesheets=[CSS("nok_web/static/css/style_checkings.css")])
        # отдаем сохраненный pdf в качестве ответа
        file_pointer = open(f'./checklist/local_storage/{name_org}.pdf', "rb")
        response = HttpResponse(file_pointer, content_type='application/pdf;')
        response['Content-Disposition'] = f'attachment; filename=download.pdf'
        response['Content-Transfer-Encoding'] = 'utf-8'

        return response


        # return Response(answers)