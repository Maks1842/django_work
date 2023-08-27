import re

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from ..app_models import *
from ..app_serializers.checking_serializer import CheckingSerializer

from ..app_serializers.departments_serializer import DepartmentsSerializer
from ..app_serializers.list_checking_serializer import ListCheckingSerializer
from ..app_serializers.organisations_serializer import OrganisationsSerializer
from ..app_serializers.organisation_persons_serializer import Organisation_PersonsSerializer
from ..app_serializers.regions_serializer import RegionsSerializer
from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Concat
import pandas as pd
import json


'''ТЕСТОВЫЕ, ТРЕНИРОВОЧНЫЕ или ВРЕМЕННО НЕ ИСПОЛЬЗУЕМЫЕ ВЬЮХИ'''

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


######## v1 - один класс для всего (). Учебный вариант. Не желательное использование ##########
class RegionsViewSet(
    # mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Regions.objects.all()
    serializer_class = RegionsSerializer

    # Отключаю отображение всех методов из Swagger
    swagger_schema = None

    @swagger_auto_schema(tags=['Регионы'])
    # Отключение метода Destroy
    def _allowed_methods(self):
        return [m for m in super(RegionsViewSet, self)._allowed_methods() if m not in ['DELETE']]

    # Отключаю отображение метода из Swagger
    # @swagger_auto_schema(auto_schema=None)

    # detail=True возвращает только одну запись, detail=False - возвращает несколько записей
    @action(methods=['get'], detail=True)
    def region_id(self, request, pk=None):
        reg_id = Regions.objects.values('id').get(pk=pk)
        return Response({'region_id': reg_id})

    # Извлекаю одну запись из конкретного поля
    # @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def region_name(self, request, pk=None):
        reg_name = Regions.objects.values('region_name').get(pk=pk)
        return Response({'region_name': reg_name})

    # Изменяю одну запись в конкретном поле
    # @swagger_auto_schema(auto_schema=None)
    @action(methods=['put'], detail=True)
    def regions_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Regions.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = RegionsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


"""
Предоставление API для данных из БД.
1. Проверяю, какому типу департамента принадлежит раздел Анкеты:
    - раздел может быть одинаковый для разных департаментов, если type_departments=None, значит подходит ко всем.
2. Передаю два позиционных аргумента, для выбора необходимых вопросов Акта, для конкретных типов оргрнизаций:
    - type_departments=1 ---> 1 - это id модели Type_Departments;
    - type_organisations=2 ---> 2 - это id модели Type_Organisations;
    - number_items=0 ---> 0 - это количество вопросов на странице. Если 0 - то пагинация идет по разделам, 
    если (например) 4 - то на каждой странице по 4 вопроса.
"""

"""
Метод создания формы Анкеты для проверки
"""


class GetActAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        methods=['get'],
        tags=['Админка'],
        operation_description="Создать форму Анкеты для проверки",
        manual_parameters=[
            openapi.Parameter('id_type_departments', openapi.IN_QUERY, description="Идентификатор типа департамента",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        type_departments = request.query_params.get('id_type_departments')
        type_organisations = request.query_params.get('id_type_organisation')
        number_items = 0

        context = []
        count = 0
        count_ex = 0

        form_sections = Form_Sections.objects.values().order_by('order_num').filter(
            type_departments=type_departments) | Form_Sections.objects.values().order_by('order_num').filter(
            type_departments=None)
        form_sections_question = Form_Sections_Question.objects.values().order_by('order_num')
        questions = Questions.objects.values()
        type_answers = Type_Answers.objects.values()
        question_values = Question_Values.objects.values()

        for fs in form_sections:
            if fs['employ_in_act'] == True:
                fs_id = fs['id']
                questions_id = form_sections_question.filter(form_sections=fs_id)
                count_section = 0
                pages = []

                for q in questions_id:
                    choices = []
                    choices_alt = ''
                    special_option = False
                    count_section += 1

                    if q['type_organisations'] == '':
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
                            if qv['special_option'] == True:
                                choices_alt = {'value': ans_var[av], 'text': qv['value_name']}
                            else:
                                choices.append({'value': ans_var[av], 'text': qv['value_name']})

                            if qv['special_option'] == True:
                                special_option = True

                        if special_option == True:
                            pages.append({
                                'name': str(count),
                                'title': question['questions'],
                                'type': type['type'],
                                'showNoneItem': 'true',
                                'noneValue': choices_alt['value'],
                                'noneText': choices_alt['text'],
                                'choices': choices,
                                'isRequired': q['required'],
                            })
                        else:
                            pages.append({
                                'name': str(count),
                                'title': question['questions'],
                                'type': type['type'],
                                'choices': choices,
                                'isRequired': q['required'],
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
                            'isRequired': q['required'],
                        })
                    elif q['type_organisations'] == 'expert':
                        count_ex += 1
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
                            'name': f'expert_{str(count_ex)}',
                            'title': question['questions'],
                            'type': type['type'],
                            'choices': choices,
                            'isRequired': q['required'],
                        })

                if len(pages) == number_items or len(questions_id) == count_section:
                    context.append({
                        'title': fs['name'],
                        'elements': pages,
                        'parent': fs['parent_id']
                    })

        x = list(context)[-1]

        return Response({"pages": context})


"""
Группирую вопросы по соответствующим разделам
"""


class GetActGroupingAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        methods=['get'],
        tags=['Админка'],
        operation_description="Создать форму Акта для расчета рейтинга",
        manual_parameters=[
            openapi.Parameter('id_type_departments', openapi.IN_QUERY, description="Идентификатор типа департамента",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        type_departments = request.query_params.get('id_type_departments')
        type_organisations = request.query_params.get('id_type_organisation')

        count = 0
        count_ex = 0
        count_criterion = 0
        block = []

        block_form_sections = Form_Sections.objects.values().order_by('order_num').filter(parent=6,
                                                                                          type_departments=type_departments) | Form_Sections.objects.values().order_by(
            'order_num').filter(type_departments=None)
        form_sections_question = Form_Sections_Question.objects.values().order_by('order_num')

        for b in block_form_sections:
            count_criterion += 1
            block_id = b['id']
            name = b['name']
            pages = []

            form_sections = Form_Sections.objects.values().order_by('order_num').filter(parent=block_id,
                                                                                        type_departments=type_departments) | Form_Sections.objects.values().order_by(
                'order_num').filter(parent=block_id,
                                    type_departments=None)
            for fs in form_sections:
                fs_id = fs['id']
                questions_id = form_sections_question.filter(form_sections=fs_id)
                count_section = 0

                for q in questions_id:
                    count_section += 1

                    if q['type_organisations'] == '':
                        count += 1
                        pages.append({'name': str(count)})

                    elif str(type_organisations) in q['type_organisations'].split(','):
                        count += 1
                        pages.append({'name': str(count)})

                    elif q['type_organisations'] == 'expert':
                        count_ex += 1
                        pages.append({'name': f'expert_{str(count_ex)}'})

            block.append({'id': count_criterion,
                          'name': name,
                          'criterion': pages})

        return Response({"pages": block})


class GetPositionUserAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить должность пользователя",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Идентификатор пользователя",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        user_id = request.query_params.get('user_id')

        position_id = Profile.objects.get(user_id=user_id).position_id
        position = Profile_Position.objects.get(pk=position_id).position

        return Response({"position": position})


class GetProfileUserAPIView(APIView):
    # permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить профиль пользователя",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Идентификатор пользователя",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        user_id = request.query_params.get('user_id')

        profile_set = Profile.objects.values().get(user_id=user_id)
        user_set = User.objects.values().get(pk=user_id)
        position = Profile_Position.objects.get(pk=profile_set['position_id']).position

        profile = {
            "username": user_set['username'],
            "first_name": user_set['first_name'],
            "last_name": user_set['last_name'],
            "birthday": profile_set['birthday'],
            "phone": profile_set['phone'],
            "email": user_set['email'],
            "address": profile_set['address'],
            "position": position,
        }

        return Response({"profile": profile})


class RegionsAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список регионов", )
    @action(detail=False, methods=['get'])
    def get(self, request):

        regions_set = Regions.objects.values()

        items = []
        try:
            for item in regions_set:
                items.append({
                    "name": item["region_name"],
                    "id": item["id"]
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'items': items})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Админка'],
        operation_description="Добавить/изменить регион",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items_json': openapi.Schema(type=openapi.TYPE_OBJECT, description='Данные региона'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        data = {"id": req_data['items_json']["id"],
                "region_name": req_data['items_json']["region_name"]}

        serializers = RegionsSerializer(data=data)
        serializers.is_valid(raise_exception=True)

        try:
            Regions.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "region_name": req_data["items_json"]["region_name"],
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Регион добавлен'})


class DepartmentsAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список департаментов",
        manual_parameters=[
            openapi.Parameter('department_id', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('department_name', openapi.IN_QUERY, description="Название департамента",
                              type=openapi.TYPE_STRING),
        ]
    )
    @action(detail=False, methods=['get'])
    def get(self, request):
        department_id = request.query_params.get('department_id')
        page = request.query_params.get('page')
        department_name = request.query_params.get('department_name')

        if page is None:
            page = 1

        if department_id:
            departments_set = Departments.objects.values().filter(pk=department_id)
        else:
            departments_set = Departments.objects.values()

        if department_name:
            departments_set = Departments.objects.values().filter(department_name__icontains=department_name)

        paginator = Paginator(departments_set, 20)
        items = []
        try:
            for item in paginator.page(page).object_list:
                items.append({
                    "id": item["id"],
                    "department_name": item["department_name"],
                    "address": item["address"],
                    "phone": item["phone"],
                    "website": item["website"],
                    "email": item["email"],
                    "parent_id": item["parent_id"],
                    "region_id": item["region_id"],
                    "type_departments_id": item["type_departments_id"]
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'totalPages': len(departments_set), 'items': items})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Админка'],
        operation_description="Добавить/изменить департамент",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items_json': openapi.Schema(type=openapi.TYPE_OBJECT, description='Данные департамента'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        data = {"id": req_data['items_json']["id"],
                "department_name": req_data['items_json']["department_name"],
                "type_departments": req_data['items_json']["type_departments_id"],
                "region": req_data['items_json']["region_id"],
                "user": req_data['items_json']["user_id"]}

        serializers = DepartmentsSerializer(data=data, context={'request': request})
        serializers.is_valid(raise_exception=True)

        try:
            Departments.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "department_name": req_data["items_json"]["department_name"],
                    "address": req_data["items_json"]["address"],
                    "phone": req_data["items_json"]["phone"],
                    "website": req_data["items_json"]["website"],
                    "email": req_data["items_json"]["email"],
                    "parent_id": req_data["items_json"]["parent_id"],
                    "region_id": req_data["items_json"]["region_id"],
                    "type_departments_id": req_data["items_json"]["type_departments_id"],
                    "user_id": req_data["items_json"]["user_id"],
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Департамент добавлен'})


class OrganisationsAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список учреждений",
        manual_parameters=[
            openapi.Parameter('organisation_id', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('department_id', openapi.IN_QUERY, description="Идентификатор департамента",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('organization_name', openapi.IN_QUERY, description="Название организации",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        organisation_id = request.query_params.get('organisation_id')
        department_id = request.query_params.get('department_id')
        organization_name = request.query_params.get('organization_name')
        page = request.query_params.get('page')
        if page is None:
            page = 1

        if organisation_id:
            organisations_set = Organisations.objects.values().filter(pk=organisation_id)
        else:
            organisations_set = Organisations.objects.values()

        if department_id:
            organisations_set = Organisations.objects.values().filter(department_id=department_id)

        if organization_name and not department_id:
            organisations_set = Organisations.objects.values().filter(organisation_name__icontains=organization_name)
        elif organization_name and department_id:
            organisations_set = Organisations.objects.values() \
                .filter(organisation_name__icontains=organization_name, department_id=department_id)

        paginator = Paginator(organisations_set, 20)

        items = []
        try:
            for item in paginator.page(page).object_list:
                items.append({
                    "name": item["organisation_name"],
                    "address": item["address"],
                    "phone": item["phone"],
                    "website": item["website"],
                    "email": item["email"],
                    "parent_id": item["parent_id"],
                    "department_id": item["department_id"],
                    "okato": item["okato"],
                    "inn": item["inn"],
                    "kpp": item["kpp"],
                    "ogrn": item["ogrn"],
                    "longitude": item["longitude"],
                    "latitude": item["latitude"],
                    "id": item["id"]
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'totalPages': len(organisations_set), 'items': items})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Админка'],
        operation_description="Добавить/изменить организацию",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items_json': openapi.Schema(type=openapi.TYPE_OBJECT, description='Данные организации'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        data = {"id": req_data['items_json']["id"],
                "organisation_name": req_data['items_json']["organisation_name"],
                "department": req_data['items_json']["department_id"]}

        serializers = OrganisationsSerializer(data=data)
        serializers.is_valid(raise_exception=True)

        try:
            Organisations.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "organisation_name": req_data["items_json"]["organisation_name"],
                    "address": req_data["items_json"]["address"],
                    "phone": req_data["items_json"]["phone"],
                    "website": req_data["items_json"]["website"],
                    "email": req_data["items_json"]["email"],
                    "parent_id": req_data["items_json"]["parent_id"],
                    "department_id": req_data["items_json"]["department_id"],
                    "okato": req_data["items_json"]["okato"],
                    "inn": req_data["items_json"]["inn"],
                    "kpp": req_data["items_json"]["kpp"],
                    "ogrn": req_data["items_json"]["ogrn"],
                    "longitude": req_data["items_json"]["longitude"],
                    "latitude": req_data["items_json"]["latitude"],
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Организация добавлена'})


class CheckingAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список Проверок",
        manual_parameters=[
            openapi.Parameter('check_name', openapi.IN_QUERY, description="Имя проверки",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('department_id', openapi.IN_QUERY, description="Идентификатор департамента",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('check_dates', openapi.IN_QUERY, description="Даты проверки через запятую",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        check_name = request.query_params.get('check_name')
        department_id = request.query_params.get('department_id')
        check_dates = request.query_params.get('check_dates')
        page = request.query_params.get('page')

        if page is None:
            page = 1

        if department_id:
            checking_set = Checking.objects.values().filter(department_id=department_id)
        else:
            checking_set = Checking.objects.values()

        if check_name:
            checking_set = Checking.objects.values().filter(name__icontains=check_name)

        if check_dates:
            range = check_dates.split(',')
            date_from, date_to = None, None
            if len(range):
                date_from = range[0]
                if len(range) > 1:
                    date_to = range[1]
                else:
                    date_to = date_from
            checking_set = Checking.objects.values().filter(
                date_checking__range=(date_from, date_to))

        paginator = Paginator(checking_set, 20)
        items = []
        try:
            for item in paginator.page(page).object_list:
                items.append({
                    "id": item["id"],
                    "checkName": item["name"],
                    "dateChecking": item["date_checking"],
                    "departmentId": item["department_id"],
                    "regionId": item["region_id"]
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'totalPages': len(checking_set), 'items': items})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Админка'],
        operation_description="Добавить/изменить Проверку",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items_json': openapi.Schema(type=openapi.TYPE_OBJECT, description='Данные проверки'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        data = {"id": req_data['items_json']["id"],
                "name": req_data['items_json']["name"],
                "date_checking": req_data['items_json']["date_checking"],
                "region": req_data['items_json']["region_id"],
                "department": req_data['items_json']["department_id"]}

        serializers = CheckingSerializer(data=data)
        serializers.is_valid(raise_exception=True)

        try:
            Checking.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "name": req_data["items_json"]["name"],
                    "date_checking": req_data["items_json"]["date_checking"],
                    "region_id": req_data["items_json"]["region_id"],
                    "department_id": req_data["items_json"]["department_id"],
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Проверка добавлен'})


class ListCheckingAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список проверяемых организаций",
        manual_parameters=[
            openapi.Parameter('checking_id', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('region_id', openapi.IN_QUERY, description="Идентификатор региона",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('checking_name', openapi.IN_QUERY, description="Наименование проверки",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('organization_name', openapi.IN_QUERY, description="Наименование учреждения",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('checking_dates', openapi.IN_QUERY, description="Даты проверки через запятую с и по",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        checking_id = request.query_params.get('checking_id')
        region_id = request.query_params.get('region_id')
        check_name = request.query_params.get('checking_name')
        org_name = request.query_params.get('organization_name')
        dates = request.query_params.get('checking_dates')
        page = request.query_params.get('page')
        if page is None:
            page = 1

        if checking_id is None or checking_id == '':
            list_checking_set = List_Checking.objects.values().all()
        else:
            list_checking_set = List_Checking.objects.values().filter(checking_id=checking_id)

        if region_id:
            list_checking_set = List_Checking.objects.values().filter(checking__region=region_id)

        if check_name:
            list_checking_set = List_Checking.objects.values().filter(checking__name__icontains=check_name)

        if org_name:
            list_checking_set = List_Checking.objects.values().filter(
                organisation__organisation_name__icontains=org_name)
        if dates:
            range = dates.split(',')
            date_from, date_to = None, None
            if len(range):
                date_from = range[0]
                if len(range) > 1:
                    date_to = range[1]
                else:
                    date_to = date_from
            list_checking_set = List_Checking.objects.values().filter(
                date_check_org__range=(date_from, date_to))

        paginator = Paginator(list_checking_set, 20)
        items = []
        try:
            for item in paginator.page(page).object_list:
                person_name = ''
                user_name = ''
                checking = Checking.objects.get(id=item["checking_id"])
                organization = Organisations.objects.get(id=item["organisation_id"])

                if item["person_id"] is not None and item["person_id"] != '':
                    person = Organisation_Persons.objects.values().get(id=item["person_id"])
                    person_name = f"{person['last_name'] or ''} {person['first_name']} {person['second_name'] or ''}"

                if item["user_id"] is not None and item["user_id"] != '':
                    user = User.objects.values().get(id=item["user_id"])
                    user_name = f"{user['last_name'] or ''} {user['first_name']}"

                items.append({"id": item["id"],
                              "checking_id": item["checking_id"],
                              "checking_name": checking.name,
                              "organisation_id": item["organisation_id"],
                              "organisation_name": organization.organisation_name,
                              "person_id": item["person_id"],
                              "person_name": person_name,
                              "user_id": item["user_id"],
                              "user_name": user_name,
                              "date_check_org": item["date_check_org"],
                              "department_id": organization.department_id,
                              "region_id": checking.region_id
                              })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'totalPages': len(list_checking_set), 'items': items})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Админка'],
        operation_description="Добавить/изменить проверяемую организацию",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items_json': openapi.Schema(type=openapi.TYPE_OBJECT, description='Данные проверяемой организации'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        data = {"id": req_data['items_json']["id"],
                "checking": req_data['items_json']["checking_id"],
                "organisation": req_data['items_json']["organisation_id"],
                "date_check_org": req_data['items_json']["date_check_org"], }

        serializers = ListCheckingSerializer(data=data)
        serializers.is_valid(raise_exception=True)

        if "person_id" not in req_data["items_json"]:
            person_id = None
        else:
            person_id = req_data["items_json"]["person_id"]

        try:
            List_Checking.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "checking_id": req_data["items_json"]["checking_id"],
                    "organisation_id": req_data["items_json"]["organisation_id"],
                    "person_id": person_id,
                    "user_id": req_data["items_json"]["user_id"],
                    "date_check_org": req_data["items_json"]["date_check_org"],
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Проверяемая организация добавлен'})


class PersonsAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список представителей",
        manual_parameters=[
            openapi.Parameter('organization_id', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('person_fio', openapi.IN_QUERY, description="Представитель организации",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        organization_id = request.query_params.get('organization_id')
        person_fio = request.query_params.get('person_fio')
        page = request.query_params.get('page')
        if page is None:
            page = 1

        if organization_id and not person_fio:
            persons_set = Organisation_Persons.objects.values().filter(organisation_id=organization_id)
        elif organization_id and person_fio:
            persons_set = Organisation_Persons.objects.values().annotate(
                full_name=Concat('first_name', 'second_name', 'last_name')
            ).filter(organisation_id=organization_id).filter((Q(full_name__icontains=person_fio) |
                                                              Q(first_name__icontains=person_fio) |
                                                              Q(last_name__icontains=person_fio) |
                                                              Q(second_name__icontains=person_fio)))
        else:
            persons_set = Organisation_Persons.objects.values()

        if person_fio and not organization_id:
            persons_set = Organisation_Persons.objects.values().annotate(
                full_name=Concat('first_name', 'second_name', 'last_name')
            ).filter(
                Q(full_name__icontains=person_fio) |
                Q(first_name__icontains=person_fio) |
                Q(last_name__icontains=person_fio) |
                Q(second_name__icontains=person_fio)
            )

        paginator = Paginator(persons_set, 20)

        items = []
        try:
            for item in paginator.page(page).object_list:
                items.append({
                    "id": item["id"],
                    "firstName": item["first_name"],
                    "secondName": item["second_name"],
                    "lastName": item["last_name"],
                    "position": item["position"],
                    "phone": item["phone"],
                    "email": item["email"],
                    "organizationId": item["organisation_id"],
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'totalPages': len(persons_set), 'items': items})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Админка'],
        operation_description="Добавить/изменить представителя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items_json': openapi.Schema(type=openapi.TYPE_OBJECT, description='Данные представителя'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        data = {"id": req_data['items_json']["id"],
                "organisation_id": req_data['items_json']["organization_id"],
                "first_name": req_data['items_json']["first_name"],
                "last_name": req_data['items_json']["last_name"]
                }

        serializers = Organisation_PersonsSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        try:
            Organisation_Persons.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "organisation_id": req_data["items_json"]["organization_id"],
                    "first_name": req_data["items_json"]["first_name"],
                    "second_name": req_data["items_json"]["second_name"],
                    "last_name": req_data["items_json"]["last_name"],
                    "position": req_data["items_json"]["position"],
                    "phone": req_data["items_json"]["phone"],
                    "email": req_data["items_json"]["email"]
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Представитель добавлен'})


class UsersAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список пользователей",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('userName', openapi.IN_QUERY, description="Имя пользователя",
                              type=openapi.TYPE_STRING)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        page = request.query_params.get('page')
        user_name = request.query_params.get('userName')
        if page is None:
            page = 1

        users_set = User.objects.values()

        if user_name:
            users_set = User.objects.values().filter(username=user_name)

        paginator = Paginator(users_set, 20)

        items = []
        try:
            for item in paginator.page(page).object_list:
                user_profile = Profile.objects.filter(user_id=item["id"]).get()
                user_position = Profile_Position.objects.get(pk=user_profile.pk)
                items.append({
                    "id": item["id"],
                    "username": item["username"],
                    "firstName": item["first_name"],
                    "lastName": item["last_name"],
                    "email": item["email"],
                    "phone": user_profile.phone,
                    "address": user_profile.address,
                    "position_id": user_profile.position_id,
                    "positionName": user_position.position,
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'totalPages': len(users_set), 'items': items})


class DepartmentTypesAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список типов департаментов"
    )
    @action(detail=False, methods=['get'])
    def get(self, request):
        department_type_set = Type_Departments.objects.values().filter(is_deleted=False)
        items = []
        try:
            for item in department_type_set:
                items.append({
                    "id": item["id"],
                    "name": item["type"]
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'items': items})


class ImportRegistryExcelAPIView(APIView):
    @swagger_auto_schema(
        method='post',
        tags=['Админка'],
        operation_description="Импортирование реестра организаций в БД",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file_object': openapi.Schema(type=openapi.TYPE_FILE, description='Файл'),
            }))
    @action(methods=['post'], detail=False)
    def post(self, request):
        file_object = request.data

        with open(f'./media/organisations_file.xlsx', 'wb+') as f:
            for chunk in file_object['organisations_file'].chunks():
                f.write(chunk)

        path_file = f'./media/organisations_file.xlsx'

        organisations_json = extract_organisations(path_file)
        count = 0
        for org in organisations_json:
            data = {'organisation_name': org['name'],
                    'address': org['address'],
                    'phone': org['phone'],
                    'website': org['website'],
                    'email': org['email'],
                    'parent_id': None,
                    'department_id': org['department'],
                    'okato': org['okato'],
                    'inn': org['inn'],
                    'kpp': None,
                    'ogrn': org['ogrn'],
                    'latitude': org['geolat'],
                    'longitude': org['geolon'], }
            try:
                serializers = OrganisationsSerializer(data=data)
                serializers.is_valid(raise_exception=True)
                exist_org = Organisations.objects.filter(Q(organisation_name=org['name']) & Q(address=org['address'])).first()
                if not exist_org:
                    org = Organisations(**data)
                    org.save()
                    count += 1
            except Exception as ex:
                return Response(
                    {"error": f'Ошибка при сохранении в модель Organisations, на строке {count}. {ex}', "data": data})

        return Response({'message': f'Успешно загружено {count} организации'})


class DistrictsAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Админка'],
        operation_description="Получить список типов департаментов",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Идентификатор региона",
                              type=openapi.TYPE_STRING)
        ]
    )
    @action(detail=False, methods=['get'])
    def get(self, request):
        name = request.query_params.get('name')
        if name is not None:
            districts_set = Districts.objects.values().filter(Q(name__icontains=name))
        else:
            districts_set = Districts.objects.values()
        items = []
        try:
            for item in districts_set:
                items.append({
                    "code": item["code"],
                    "name": item["name"]
                })
        except Exception as e:
            return Response({'error': f'{e}'})

        return Response({'items': items})


def extract_organisations(path_file):
    excel_data = pd.read_excel(path_file)
    json_str = excel_data.to_json(orient='records', date_format='iso')
    parsed = json.loads(json_str)
    # преобразуем ключи в нижний регистр, дабы избежать разночтений в названиях колонок при импорте
    converted_org = []
    for org in parsed:
        converted_org.append({k.lower(): v for k, v in org.items()})
    return converted_org
