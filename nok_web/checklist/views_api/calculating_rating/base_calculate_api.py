from ...app_models import *
from ...app_serializers.answers_serializer import AnswersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.db import IntegrityError

from ..magic import do_some_magic
from .culture_legacy import culture_legacy_rating
from .culture_standart import culture_standart_rating
from .culture_theatre_legacy import culture_theatre_legacy_rating
from .culture_theatre_standart import culture_theatre_standart_rating
from .healthcare import healthcare_rating
from .school import school_rating
from .addeducation import addeducation_rating
from .kindergarden import kindergarden_rating
from .techcollege import techcollege_rating
from ...app_serializers.ratings_serializer import RatingsSerializer

'''
Данный метод рассчитывает рейтинг с применением коэффициентов, при определении количества положительных 
отзывов респондентов.
Результаты рейтингов, по каждой организации (в разрезе проверок), хранятся в Модели Ratings. 
!!! - CalculatingRatingAPIView только для тестов.
!!! - def calculating_rating - для боевого режима

Применяются коэффициенты установленные законом и рассчитанные рандомно (в соответствии с заданным диапазоном)

Количество респондентов, удовлетворенных качеством услуг, рассчитывается на основе кастомных коэффициентов.
Устанавливается диапазон коэффициента, который рассчитывается рандомно.

В случае необходимости откорректировать рейтинг, нужное количество респондентов устанавливается вручную и применяется метод ChangeRatings
'''


class CalculatingRatingAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['post'],
        tags=['Рейтинг'],
        operation_description="Рассчитать рейтинг",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'checking': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор проверки'),
                'organisations': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор организации'),
                'type_organisations': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                     description='Идентификатор типа организации'),
                'quota': openapi.Schema(type=openapi.TYPE_INTEGER, description='Квота респондентов'),
                'invalid_person': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество инвалидов'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        serializers = AnswersSerializer(data=req_data)
        serializers.is_valid(raise_exception=True)
        try:
            Answers.objects.update_or_create(
                checking_id=req_data['checking'],
                organisations_id=req_data['organisations'],
                type_organisations_id=req_data['type_organisations'],
                defaults={'quota': req_data['quota'], 'invalid_person': req_data['invalid_person']},
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении Квоты респондентов и Инвалидов"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        checking = str(req_data['checking'])
        organisation = str(req_data['organisations'])
        type_organisation = str(req_data['type_organisations'])
        quota = int(req_data['quota'])
        invalid_person = int(req_data['invalid_person'])

        rating = calculating_rating(checking, organisation, type_organisation, quota, invalid_person)
        # return Response(rating)

        serializers = RatingsSerializer(data=rating)
        serializers.is_valid(raise_exception=True)
        try:
            Ratings.objects.update_or_create(
                checking_id=req_data['checking'],
                organisations_id=req_data['organisations'],
                type_organisations_id=req_data['type_organisations'],
                defaults={'ratings_json': rating},
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении рейтингов"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Рейтинг успешно сохранен',
                         'ratings': rating
                         })


def calculating_rating(checking, organisation, type_organisation, quota, invalid_person):

    queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)
    # return queryset['act_json']

    try:
        answer_set = Answers.objects.filter(checking_id=checking, organisations_id=organisation).get(type_organisations_id=type_organisation)
    except:
        return Response({'error': 'Не найдены данные о результатах запрашиваемой проверки.'})

    act_answer = answer_set.answers_json

    form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
    form_json_to_calculate = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json_to_calculate
    query = Question_Values.objects.values()

    comparison = do_some_magic(form_json, act_answer)
    answers = answer_in_the_act(comparison, query)

    match type_organisation:
        case '1':
            return culture_legacy_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '10':
            return culture_standart_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '8':
            return culture_theatre_legacy_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '6':
            return culture_theatre_standart_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '2':
            return healthcare_rating(quota, invalid_person, answers, form_json, form_json_to_calculate, 59, 59)  # Последние два значения - нормативное количество документов на Стенде и Сайте
        case '3':
            return healthcare_rating(quota, invalid_person, answers, form_json, form_json_to_calculate, 60, 60)
        case '4':
            return kindergarden_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '5':
            return school_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '7':
            return techcollege_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
        case '9':
            return addeducation_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)

    return False


'''
Функция формирования текстовых ответов для HTML шаблона из json файла,
который сформирован на основе сопоставления act_json и answer_json.
'''


def answer_in_the_act(comparison, query):
    list_dict = {}

    for answ in comparison:
        answer = []
        answers = []
        if '11' in comparison[answ] or '12' in comparison[answ]:
            for a in comparison[answ]:
                if a == '':
                    answer = {'value': '0', 'text': a}
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = {'value': '1', 'text': a}
                    else:
                        answer = {'value': query.get(pk=int(a))['value_name'], 'text': a}
                answers.append(answer)
        elif len(comparison[answ]) > 2:
            for a in comparison[answ]:
                if a != '':
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = {'value': '1', 'text': a}
                    else:
                        answer = {'value': query.get(pk=int(a))['value_name'], 'text': a}
                    answers.append(answer)
        elif len(comparison[answ]) == 2 and comparison[answ][1] != '' and \
                (not '11' in comparison[answ][1] or not '12' in comparison[answ][1]):
            for a in comparison[answ]:
                if a != '':
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = {'value': '1', 'text': a}
                    else:
                        answer = {'value': query.get(pk=int(a))['value_name'], 'text': a}
                    answers.append(answer)
        else:
            for a in comparison[answ]:
                if a == '':
                    answer = {'value': '0', 'text': a}
                elif a != '':
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = {'value': '1', 'text': a}
                    elif query.get(pk=int(a))['value_name'] == 'Да':
                        answer = {'value': '1', 'text': a}
                    elif query.get(pk=int(a))['value_name'] == 'Нет':
                        answer = {'value': '0', 'text': a}
                    else:
                        answer = {'value': query.get(pk=int(a))['value_name'], 'text': a}
                answers.append(answer)
        list_dict[answ] = answers

    return list_dict