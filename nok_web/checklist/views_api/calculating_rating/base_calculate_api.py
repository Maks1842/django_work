from ...app_models import *
from ...app_serializers.answers_serializer import AnswersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser

from ..magic import do_some_magic
from .culture_legacy import culture_legacy_rating
from .culture_standart import culture_standart_rating
from .healthcare import healthcare_rating
from .school import school_rating
from .addeducation import addeducation_rating
from .kindergarden import kindergarden_rating
from .techcollege import techcollege_rating


'''
Данный метод рассчитывает рейтинг с применением коэффициентов, при определении количества положительных 
отзывов респондентов.
Результаты рейтингов, по каждой организации (в разрезе проверок), хранятся в Модели Ratings. 
!!! - CalculatingRatingAPIView только для тестов.
!!! - def calculating_rating - для боевого режима
'''


# CalculatingRatingAPIView только для тестов. def calculating_rating - для боевого режима
class CalculatingRatingAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Рейтинг'],
        operation_description="Расчет рейтинга, с применением коэффициентов к респондентам",
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

        rating = calculating_rating(checking, organisation, type_organisation)

        return Response(rating)
# Чтобы верхний блок не попадал в API, необходимо его отключить в urls.py


def calculating_rating(checking, organisation, type_organisation):

    rating = {}

    queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)

    try:
        answer_set = Answers.objects.filter(checking_id=checking).get(organisations_id=organisation)
    except:
        return Response({'error': 'Не найдены данные о результатах запрашиваемой проверки.'})

    act_answer = answer_set.answers_json
    quota = answer_set.quota
    invalid_person = answer_set.invalid_person

    form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
    form_json_to_calculate = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json_to_calculate
    query = Question_Values.objects.values()

    comparison = do_some_magic(form_json, act_answer)
    answers = answer_in_the_act(comparison, query)

    if type_organisation == '1':
        rating = culture_legacy_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
    elif type_organisation == '10':
        rating = culture_standart_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
    elif type_organisation == '2' or type_organisation == '3':
        rating = healthcare_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
    elif type_organisation == '4':
        rating = kindergarden_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
    elif type_organisation == '5':
        rating = school_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
    elif type_organisation == '7':
        rating = techcollege_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)
    elif type_organisation == '9':
        rating = addeducation_rating(quota, invalid_person, answers, form_json, form_json_to_calculate)

    return rating


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