import re

from rest_framework.permissions import IsAdminUser

from ..app_models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from ..app_serializers.regions_serializer import RegionsSerializer
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import GenericViewSet
from drf_yasg2.utils import swagger_auto_schema, unset
from drf_yasg2 import openapi


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


class GetActAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['get'],
        tags=['Для Админа'],
        operation_description="Получить форму Анкеты для проверки",
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
                        choices.append({'value': ans_var[av], 'text': qv['value_name']})

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

            if len(pages) == number_items or len(questions_id) == count_section:
                context.append({
                    'title': fs['name'],
                    'elements': pages,
                })

        return Response({"pages": context})


class GetOrganisationTestAPIView(APIView):

    permission_classes = [IsAdminUser]

    @action(methods=['get'], detail=False)
    def get(self, request):
        organisation = Organisations.objects.values()
        return Response(organisation)

    @action(methods=['post'], detail=True)
    # @transaction.atomic
    def post(self, request):
        organisation = Organisations.objects.values()
        return Response(organisation)
