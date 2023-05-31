import re

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from ..app_models import *
from ..app_serializers.checking_serializer import CheckingSerializer

from ..app_serializers.departments_serializer import DepartmentsSerializer
from ..app_serializers.list_checking_serializer import ListCheckingSerializer
from ..app_serializers.organisations_serializer import OrganisationsSerializer
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

        result = []
        for item in regions_set:
            result.append({
                "name": item["region_name"],
                "id": item["id"]
            })

        return Response(result)

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
        operation_description="Получить список департаментов", )
    @action(detail=False, methods=['get'])
    def get(self, request):

        departments_set = Departments.objects.values()

        result = []
        for item in departments_set:
            result.append({
                "name": item["department_name"],
                "value": {"id": item["id"],
                          "type_departments_id": item["type_departments_id"]}
            })

        return Response(result)

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

        serializers = DepartmentsSerializer(data=data)
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
            openapi.Parameter('department_id', openapi.IN_QUERY, description="Идентификатор департамента",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        department_id = request.query_params.get('department_id')

        if department_id:
            organisations_set = Organisations.objects.values().filter(department_id=department_id)
        else:
            organisations_set = Organisations.objects.values()

        result = []
        for item in organisations_set:
            result.append({
                "name": item["organisation_name"],
                "id": item["id"]
            })

        return Response(result)

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
                    "inn": req_data["items_json"]["inn"],
                    "kpp": req_data["items_json"]["kpp"],
                    "ogrn": req_data["items_json"]["ogrn"],
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
            openapi.Parameter('department_id', openapi.IN_QUERY, description="Идентификатор департамента",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        department_id = request.query_params.get('department_id')

        if department_id:
            checking_set = Checking.objects.values().filter(department_id=department_id)
        else:
            checking_set = Checking.objects.values()

        result = []
        for item in checking_set:
            result.append({
                "name": item["name"],
                "value": {"id": item["id"],
                          "date_checking": item["date_checking"]}
            })

        return Response(result)

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
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        checking_id = request.query_params.get('checking_id')
        page = request.query_params.get('page')
        if page is None:
            page = 1
        if checking_id is None or checking_id == '':
            list_checking_set = List_Checking.objects.values().all()
        else:
            list_checking_set = List_Checking.objects.values().filter(checking_id=checking_id)
        paginator = Paginator(list_checking_set, 20)
        items = []
        try:
            for item in paginator.page(page).object_list:
                person_name = ''
                user_name = ''
                checking_name = Checking.objects.get(id=item["checking_id"]).name
                organisation_name = Organisations.objects.get(id=item["organisation_id"]).organisation_name

                if item["person_id"] is not None and item["person_id"] != '':
                    person = Organisation_Persons.objects.values().get(id=item["person_id"])
                    person_name = f"{person['last_name'] or ''} {person['first_name']} {person['second_name'] or ''}"

                if item["user_id"] is not None and item["user_id"] != '':
                    user = User.objects.values().get(id=item["user_id"])
                    user_name = f"{user['last_name'] or ''} {user['first_name']}"

                items.append({"id": item["id"],
                               "checking_id": item["checking_id"],
                               "checking_name": checking_name,
                               "organisation_id": item["organisation_id"],
                               "organisation_name": organisation_name,
                               "person_id": item["person_id"],
                               "person_name": person_name,
                               "user_id": item["user_id"],
                               "user_name": user_name,
                               "date_check_org": item["date_check_org"],
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

        try:
            List_Checking.objects.update_or_create(
                pk=req_data["items_json"]["id"],
                defaults={
                    "checking_id": req_data["items_json"]["checking_id"],
                    "organisation_id": req_data["items_json"]["organisation_id"],
                    "person_id": req_data["items_json"]["person_id"],
                    "user_id": req_data["items_json"]["user_id"],
                    "date_check_org": req_data["items_json"]["date_check_org"],
                },
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Проверяемая организация добавлен'})
