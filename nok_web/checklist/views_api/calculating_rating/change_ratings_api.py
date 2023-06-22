
from ...app_models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser
from django.db import IntegrityError, transaction
from .changes_to_culture_theatre_standart import culture_theatre_standart_rating
from .changes_to_culture_theatre_legacy import culture_theatre_legacy_rating
from .changes_to_culture_standart import culture_standart_rating
from .changes_to_culture_legacy import culture_legacy_rating
from .changes_to_healthcare import healthcare_rating
from .changes_to_education import education_rating
from ...app_serializers.ratings_serializer import RatingsSerializer

'''
Метод корректировки рейтинга, за счет ручного введения количества положительных отзывов респондентов.
Результаты рейтингов, перезаписываются в Модели Ratings. 

Количество респондентов, удовлетворенных качеством услуг, рассчитывается на основе кастомных коэффициентов.
Устанавливается диапазон коэффициента, который рассчитывается рандомно.

В случае необходимости откорректировать рейтинг, нужное количество респондентов устанавливается вручную и применяется метод ChangeRatings
'''


class ChangeRatingsAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['post'],
        tags=['Рейтинг'],
        operation_description="Корректировка рейтинга (ввод фактических данных по респондентам)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            'checking_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Идентификатор проверки"),
            'organisation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Идентификатор организации"),
            'type_organisation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Идентификатор типа организации"),
            'count_person_1_3_stend': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных стендом"),
            'count_person_1_3_web': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных сайтом"),
            'count_person_2_2_2': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных своевременностью услуг (для здравоохранения)"),
            'count_person_2_3': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных комфортом"),
            'count_invalid_person_3_3': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных инвалидов"),
            'count_person_4_1': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных вежливостью, первичный контакт"),
            'count_person_4_2': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных вежливостью, непоследственное оказание услуги"),
            'count_person_4_3': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных вежливостью, дистанционное взаимодействие"),
            'count_person_5_1': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число готовых рекомендовать учреждение"),
            'count_person_5_2': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных графиком/навигацией"),
            'count_person_5_3': openapi.Schema(type=openapi.TYPE_INTEGER, description="Число удовлетворенных условиями оказания услуг"),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        rating = {}

        checking = req_data['checking_id']
        organisation = req_data['organisation_id']
        type_organisation = req_data['type_organisation_id']

        try:
            answer_set = Answers.objects.filter(checking_id=checking, type_organisations_id=type_organisation, organisations_id=organisation).values()
            quota = answer_set[0]['quota']
            invalid_person = answer_set[0]['invalid_person']

            if req_data['count_person_1_3_stend'] > quota or req_data['count_person_1_3_web'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 1.3 не может превышать {quota}"})
            if req_data['count_person_2_3'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 2.3 не может превышать {quota}"})
            if req_data['count_invalid_person_3_3'] > invalid_person:
                return Response({"error": f"Количество респондентов в Критерии 3.3 не может превышать {invalid_person}"})
            if req_data['count_person_4_1'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 4.1 не может превышать {quota}"})
            if req_data['count_person_4_2'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 4.2 не может превышать {quota}"})
            if req_data['count_person_4_3'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 4.3 не может превышать {quota}"})
            if req_data['count_person_5_1'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 5.1 не может превышать {quota}"})
            if req_data['count_person_5_2'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 5.2 не может превышать {quota}"})
            if req_data['count_person_5_3'] > quota:
                return Response({"error": f"Количество респондентов в Критерии 5.3 не может превышать {quota}"})
        except:
            pass

        count_person = {
            "count_person_1_3_stend": req_data['count_person_1_3_stend'],
            "count_person_1_3_web": req_data['count_person_1_3_web'],
            "count_person_2_3": req_data['count_person_2_3'],
            "count_invalid_person_3_3": req_data['count_invalid_person_3_3'],
            "count_person_4_1": req_data['count_person_4_1'],
            "count_person_4_2": req_data['count_person_4_2'],
            "count_person_4_3": req_data['count_person_4_3'],
            "count_person_5_1": req_data['count_person_5_1'],
            "count_person_5_2": req_data['count_person_5_2'],
            "count_person_5_3": req_data['count_person_5_3']
        }

        if 'count_person_2_2_2' in req_data and req_data['count_person_2_2_2'] != '':
            count_person.update({"count_person_2_2_2": req_data['count_person_2_2_2']})

        try:
            ratings_set = Ratings.objects.filter(checking_id=checking).get(organisations_id=organisation)
        except:
            return Response({'error': 'Не найдены данные о рейтингах запрашиваемой проверки.'})

        ratings = ratings_set.ratings_json

        match type_organisation:
            case 1:
                rating = culture_legacy_rating(ratings, count_person)
            case 10:
                rating = culture_standart_rating(ratings, count_person)
            case 8:
                rating = culture_theatre_legacy_rating(ratings, count_person)
            case 6:
                rating = culture_theatre_standart_rating(ratings, count_person)
            case (2 | 3):
                rating = healthcare_rating(ratings, count_person)
            case (4 | 5 | 7 | 9):
                rating = education_rating(ratings, count_person)

        data = {'checking': req_data['checking_id'],
                'organisation': req_data['organisation_id'],
                'type_organisation': req_data['type_organisation_id'],
                'ratings_json': rating
                }

        serializers = RatingsSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        try:
            Ratings.objects.update_or_create(
                checking_id=checking,
                organisations_id=organisation,
                type_organisations_id=type_organisation,
                defaults={'ratings_json': data['ratings_json']},
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response(data['ratings_json'])