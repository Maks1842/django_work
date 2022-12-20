from ..app_models import *
from ..app_serializers.answers_serializer import AnswersSerializer
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from drf_yasg2.utils import swagger_auto_schema, unset
from drf_yasg2 import openapi
from django.db import IntegrityError, transaction

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
Представления ApiView. Основной вариант.
'''


class AnswersAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Проверка'],
        operation_description="Получить результаты ответов",
        manual_parameters=[
            openapi.Parameter('id_checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER),

        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        checking = request.query_params.get('id_checking')
        organisation = request.query_params.get('id_organisation')
        type_organisation = request.query_params.get('id_type_organisation')

        queryset = Answers.objects.filter(organisations_id=organisation, checking_id=checking,
                                          type_organisations=type_organisation)
        answer = ''
        if len(queryset) > 0:
            answer = queryset[0].answers_json
        return Response(answer)

    @swagger_auto_schema(
        methods=['post'],
        tags=['Проверка'],
        operation_description="Добавить результаты ответов",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'checking': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор проверки'),
                'organisations': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор организации'),
                'type_organisations': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                     description='Идентификатор типа организации'),
                'answers_json': openapi.Schema(type=openapi.TYPE_STRING, description='Результаты ответов'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        serializers = AnswersSerializer(data=req_data)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
        except IntegrityError:
            return Response({"error": "Ответ, по данной проверке, уже существует"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Ответ успешно добавлен'})


class GetFormActByOrganizationTypeAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Проверка'],
        operation_description="Проверить наличие созданной проверки, в случае отсутствия Получить форму Акта для проверки, в формате JSON",
        manual_parameters=[
            openapi.Parameter('id_checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        checking = request.query_params.get('id_checking')
        organisation = request.query_params.get('id_organisation')
        type_organisation = request.query_params.get('id_type_organisation')


        if Answers.objects.filter(checking_id=checking, organisations_id=organisation, type_organisations=type_organisation).exists():
            return Response({"error": "Такая проверка уже создана"})
        else:
            queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)

            form_json = {}
            if len(queryset) > 0:
                form_json = queryset[0].act_json

        return Response(form_json)


class GetCheckListOrganizationsAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Проверка'],
        operation_description="Получить проверяемую организацию. "
                              "Если эксперт не указан, то получаем все организации находящиеся на проверке.",
        manual_parameters=[
            openapi.Parameter('id_check', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_user', openapi.IN_QUERY, description="Идентификатор эксперта",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        check = request.query_params.get('id_check')
        user = request.query_params.get('id_user')

        if user is None:
            queryset = List_Checking.objects.filter(checking_id=check)
        else:
            queryset = List_Checking.objects.filter(checking_id=check, user_id=user)


        result = []
        if len(queryset) > 0:
            for item in queryset:
                department = Departments.objects.values('type_departments_id').get(pk=item.organisation.department_id)
                result.append({
                    'id': item.organisation_id,
                    'name': item.organisation.organisation_name,
                    # 'type': item.organisation.type_organisations_id,
                    'department': department['type_departments_id']
                })
        return Response({'data': result})


class GetListCheckingAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Проверка'],
        operation_description="Получить список проверок, в которых участвует эксперт",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Идентификатор эксперта",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        user = request.query_params.get('user_id')
        queryset = List_Checking.objects.filter(user_id=user).distinct('checking')

        result = []
        if len(queryset) > 0:
            for item in queryset:
                result.append({
                    'id': item.checking.id,
                    'name': item.checking.name,
                })
        return Response({'data': result})


class GetCheckingCompletedAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Проверка'],
        operation_description="Получить список организаций, по которым завершенны проверки, в которых участвовал эксперт",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Идентификатор эксперта",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        user = request.query_params.get('user_id')
        queryset = List_Checking.objects.filter(user_id=user)
        if len(queryset) == 0:
            return Response({'error': 'У данного эксперта нет проверок'})

        result = []
        for item in queryset:
            queryset_completed = Answers.objects.filter(checking_id=item.checking.id, organisations_id=item.organisation)
            if len(queryset_completed) > 0:
                for item_comp in queryset_completed:
                    result.append({
                        'check_id': item_comp.checking.id,
                        'check_name': item_comp.checking.name,
                        'check_date': item_comp.checking.date_checking,
                        'org_id': item_comp.organisations.id,
                        'org_name': item_comp.organisations.organisation_name,
                        'type_org_id': item_comp.type_organisations.id,
                        'type_org_name': item_comp.type_organisations.type,
                        'org_check_date': item.date_check_org,
                        # 'org_person': item_comp.checking.date_checking,

                    })
            else:
                result.append({
                    'error': f'Проверка организации {item.organisation.organisation_name} не завершена',
                })
        return Response({'data': result})
