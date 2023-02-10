from ...app_models import *
from ..magic import do_some_magic, answer_in_the_act
from django.template.loader import render_to_string
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser

from weasyprint import HTML, CSS
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer

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


class GetRatingsIntoPdfAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        method='get',
        tags=['Рейтинг'],
        operation_description="Получить рейтинги по результатам проверки в формате pdf. "
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
        inn_org = Organisations.objects.get(pk=organisation).inn
        website_org = Organisations.objects.get(pk=organisation).website


        queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)
        if len(queryset) == 0:
            return Response({'error': 'Не найден указанный тип организации'})

        temp = Templates.objects.filter(type_templates_id=2).get(type_organisations_id=type_organisation).template_file
        if temp == '':
            return Response({'error': 'Не найден шаблон Рейтинга для данного типа организации. '
                                      'Обратитесь к Администратору'})

        try:
            act_answer = Answers.objects.filter(
                checking_id=checking,
                type_organisations=type_organisation
            ).get(organisations_id=organisation).answers_json
        except:
            return Response({'error': 'Не найдены данные о результатах запрашиваемой проверки.'})

        try:
            ratings = Ratings.objects.filter(
                checking_id=checking,
                type_organisations=type_organisation
            ).get(organisations_id=organisation).ratings_json
        except:
            return Response({'error': 'Не найдены данные о Рейтингах запрашиваемой проверки.'})

        date_check = List_Checking.objects.filter(checking_id=checking).get(organisation_id=organisation).date_check_org

        form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
        query = Question_Values.objects.values()

        comparison = do_some_magic(form_json, act_answer)
        answers = answer_in_the_act(comparison, query)

        context = {'name_org': name_org,
                   'address_org': address_org,
                   'inn': inn_org,
                   'website': website_org,
                   'date_check': date_check,
                   'ratings': ratings,
                   'answers': answers}

        content = render_to_string(f'ratings/{temp}', context)

        css = CSS(string='@page { size: A4 !important; '
                         'margin-left: 1cm !important; '
                         'margin-right: 1cm !important; '
                         'margin-top: 1.5cm !important;'
                         'margin-bottom: 1.5cm !important }')
        HTML(string=content).write_pdf(f'./checklist/local_storage/Рейтинг_пр{checking}_{name_org}.pdf', stylesheets=[CSS("nok_web/static/css/style_checkings.css")])
        # отдаем сохраненный pdf в качестве ответа
        file_pointer = open(f'./checklist/local_storage/Рейтинг_пр{checking}_{name_org}.pdf', "rb")
        response = HttpResponse(file_pointer, content_type='application/pdf;')
        response['Content-Disposition'] = f'attachment; filename=download.pdf'
        response['Content-Transfer-Encoding'] = 'utf-8'

        return response

        # return Response(answers)