import re
import json

from .permissions import IsAdminOrReadOnly, IsOwnerAndAdminOrReadOnly
from django.http import Http404, HttpResponse
from .serializers import *
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import JSONRenderer
from drf_yasg2.utils import swagger_auto_schema, unset
from drf_yasg2 import openapi
from django.db import IntegrityError

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


'''
Представления ApiView. Основной вариант.
'''


class AnswersAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Получить результаты ответов'],
        manual_parameters=[
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_checking', openapi.IN_QUERY, description="Идентификатор проверка",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        id_organisation = request.query_params.get('id_organisation')
        id_checking = request.query_params.get('id_checking')

        queryset = Answers.objects.filter(organisations_id=id_organisation, checking_id=id_checking)
        answer = ''
        if len(queryset) > 0:
            answer = queryset[0].answers_json
        return Response(answer)

    @swagger_auto_schema(
        methods=['post'],
        tags=['Добавить результаты ответов'],
        manual_parameters=[
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_checking', openapi.IN_QUERY, description="Идентификатор проверка",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('answers', openapi.IN_QUERY, description="Результаты ответов",
                              type=openapi.TYPE_STRING),
        ])
    @action(methods=['post'], detail=True)
    def post(self, request):
        id_organisation = request.query_params.get('id_organisation')
        id_checking = request.query_params.get('id_checking')
        answers = request.query_params.get('answers')

        data = {'organisations': id_organisation, 'checking': id_checking, 'answers_json': answers}
        serializers = AnswersSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class OrganisationPersonsAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Получить представителя организации'],
        manual_parameters=[
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        organisation = request.query_params.get('id_organisation')
        persons = Form_Organisation_Persons.objects.filter(organisation_id=organisation)
        result = []
        if len(persons) > 0:
            for item in persons:
                result.append({
                    'id': item.person_id,
                    'name': f"{item.person.last_name} {item.person.first_name} {item.person.second_name or ''}"
                })
        return Response({'data': result})

    @swagger_auto_schema(
        methods=['post'],
        tags=['Добавить представителя организации'],
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
        id_org = req_data.pop('id_organisation')
        serializers = Organisation_PersonsSerializer(data=req_data)
        serializers.is_valid(raise_exception=True)
        try:
            res = serializers.save()
        except IntegrityError:
            return Response({"error": "Такой человек уже существует"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )
        data = {
            'organisation': id_org,
            'person': res.pk
        }
        serializers_person = Form_Organisation_PersonsSerializer(data=data)
        serializers_person.is_valid(raise_exception=True)
        try:
            serializers_person.save()
        except IntegrityError:
            return Response({"error": "Пользователь добавлен, но не связан с организацией. Обратитесь к администратору!"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Представитель успешно добавлен'})


class GetListTypeOrganizationsAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Типы организаций'],
        operation_description="Получить список типов оргнизаций",
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


class GetFormActByOrganizationTypeAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Получить формы Актов по типу организации'],
        operation_description="Получить формы Актов для проверки, в формате JSON",
        manual_parameters=[
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        type_organisation = request.query_params.get('id_type_organisation')
        queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)

        form_json = {}
        if len(queryset) > 0:
            form_json = queryset[0].act_json

        return Response(form_json)


class GetFormActByOrganizationIdAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Получить формы Актов по Id организации'],
        operation_description="Получить формы Актов для проверки, в формате JSON",
        manual_parameters=[
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        organisation = request.query_params.get('id_organisation')
        queryset = Organisations.objects.filter(id=organisation)

        form_json = {}
        if len(queryset) > 0:
            form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json

        return Response(form_json)


class GetCheckListOrganizationsAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Список организаций на проверке'],
        operation_description="Получить: user --> организации, проверка --> организации",
        manual_parameters=[
            openapi.Parameter('id_check', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_user', openapi.IN_QUERY, description="Идентификатор эксперта",
                              type=openapi.TYPE_INTEGER)
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
                    'type': item.organisation.type_organisations_id,
                    'department': department['type_departments_id']
                })
        return Response({'data': result})


class GetListCheckingAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Список проверок у эксперта'],
        operation_description="Получить список проверок в которых участвует эксперт",
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


class GetActAPIView(APIView):

    def get(self, request, type_departments=3, type_organisations=9, number_items=0):

        context = []
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
                        'name': str(count),
                        'title': question['questions'],
                        'type': type['type'],
                        'choices': choices,
                        'isRequired': 'true',
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
                context.append({
                    'title': fs['name'],
                    'elements': pages,
                })
                pages = []
        return Response({"pages": context})


class GetActAnswerAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Получить Акта проверки по организации'],
        operation_description="Получить Акт с результатами проверки, в формате JSON",
        manual_parameters=[
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):

        organisation = request.query_params.get('id_organisation')

        # Необходим рефакторинг: записать запрос к FormsAct по id_organisation одной строкой
        try:
            type_organisations = Organisations.objects.get(pk=organisation).type_organisations_id
        except Exception:
            type_organisations = 0
        queryset = FormsAct.objects.filter(type_organisations_id=type_organisations)

        answers = {}
        if len(queryset) > 0:
            form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
            query = Question_Values.objects.values()

            comparison = do_some_magic(form_json)
            answers = answer_in_the_act(comparison, query)

        return Response(answers)


'''
Функция сравнения двух json.
Производится сопоставление полученных ответов с имеющимеся вопросами.
На выходе формируется новый json, где:
- если один из ответов совпадает с вопросом, то ячейки без совпадения остаются пустые, в ячейках с совпадением проставляется номер ответа;
- если нет ни одного совпадения, то все ячейки остаются пустые.
В формируемом json количество объектов в списке равно количеству объектов списка с вопросами.
'''


def do_some_magic(form_json):
    # f = open("checklist/modules/abm.json")       # Акт амбулатория
    # f = open("checklist/modules/cult_legacy.json")    # Акт культурное наследие
    f = open("checklist/modules/cult_standart.json")  # Акт культура стандарт
    # f = open("checklist/modules/kindergarten.json")    # Акт Детсад
    # f = open("checklist/modules/school.json")    # Акт школа
    act_answer = json.load(f)
    f.close()
    # f = open("answ.json")
    # answ = json.load(f)
    # f.close()

    act = form_json
    answ = act_answer

    questions = {}
    for page in act['pages']:
        for element in page['elements']:
            choices = []
            for choice in element['choices']:
                choices.append(choice['value'])
            questions[element['name']] = choices

    tt = {}

    for question in answ:
        sh = []
        for answer in questions[question]:
            if answer in answ[question]:
                sh.append(answer)
            else:
                sh.append('')
        tt[question] = sh
    z = questions.copy()
    z.update(tt)
    for question in z:
        if question not in answ:
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
