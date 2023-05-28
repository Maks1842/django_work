from ..app_models import *
from ..app_serializers.organisation_persons_serializer import Organisation_PersonsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
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



class OrganisationPersonsAPIView(APIView):
    # permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['get'],
        tags=['Организация'],
        operation_description="Получить представителя организации",
        manual_parameters=[
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        organisation = request.query_params.get('id_organisation')

        if Organisation_Persons.objects.filter(organisation_id=organisation):
            persons = Organisation_Persons.objects.filter(organisation_id=organisation).values()
        else:
            persons = Organisation_Persons.objects.filter(organisation_id__isnull=True).values()

        result = []
        if len(persons) > 0:
            for item in persons:
                result.append({
                    'id': item['id'],
                    'name': f"{item['last_name']} {item['first_name']} {item['second_name'] or ''}"
                })
        return Response({'data': result})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Организация'],
        operation_description="Добавить представителя организации",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_organisation': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор организации'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя'),
                'second_name': openapi.Schema(type=openapi.TYPE_STRING, description='Отчество'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия'),
                'position': openapi.Schema(type=openapi.TYPE_STRING, description='Должность'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='Эл. почта'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        # .pop()ищет указанный ключ (аналогично .get(), но), возвращает и удаляет его, если он найден, иначе генерируется исключение.
        # id_org = req_data.pop('id_organisation')

        try:
            serializers = Organisation_PersonsSerializer(data=req_data)
            fio = f"{req_data['last_name']} {req_data['first_name']} {req_data['second_name'] or ''}"
            serializers.is_valid(raise_exception=True)
            res = serializers.save()
            return Response({'data': {'id': res.pk, 'name': fio}})
        except IntegrityError as ex:
            return Response({'error': f"Не удалось добавить представителя! {ex}"})
        # error = "Не удалось добавить представителя!"
        # try:
        #     with transaction.atomic():
        #         res = serializers.save()
        #         data = {'organisation': id_org, 'person': res.pk}
        #         serializers_person = Form_Organisation_PersonsSerializer(data=data)
        #         serializers_person.is_valid(raise_exception=True)
        #         serializers_person.save()
        #         return Response({'data': {'id': res.pk, 'name': fio}})
        # except IntegrityError as exception:
        #     if 'violates unique constraint' in exception.args[0]:
        #         error = f"{error} Такой человек уже существует."
        #     return Response({'error': error})


class GetListTypeOrganizationsAPIView(APIView):

    # permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        method='get',
        tags=['Организация'],
        operation_description="Получить список типов организаций",
        manual_parameters=[
            openapi.Parameter('id_type_department', openapi.IN_QUERY, description="Идентификатор типа департамента",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        type_department = request.query_params.get('id_type_department')
        if type_department is None:
            queryset = Type_Organisations.objects.all()
        else:
            queryset = Type_Organisations.objects.filter(type_departments_id=type_department)

        result = []
        if len(queryset) > 0:
            for item in queryset:
                result.append({
                    'id': item.id,
                    'name': item.type,
                })
        return Response({'data': result})
