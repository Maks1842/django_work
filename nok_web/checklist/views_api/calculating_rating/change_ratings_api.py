
from ...app_models import *
from ...app_serializers.answers_serializer import AnswersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser

from .changes_to_culture import culture_rating
from .changes_to_healthcare import healthcare_rating
from .changes_to_education import education_rating



class ChangeRatingsAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['get'],
        tags=['Расчет рейтинга'],
        operation_description="Корректировка рейтинга (ввод фактических данных по респондентам)",
        manual_parameters=[
            openapi.Parameter('id_checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_1_3_stend', openapi.IN_QUERY, description="Число удовлетворенных стендом",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_1_3_web', openapi.IN_QUERY, description="Число удовлетворенных сайтом",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_2_2_2', openapi.IN_QUERY, description="Число удовлетворенных своевременностью услуг",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_2_3', openapi.IN_QUERY, description="Число удовлетворенных комфортом",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_invalid_person_3_3', openapi.IN_QUERY, description="Число удовлетворенных инвалидов",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_4_1', openapi.IN_QUERY, description="Число удовлетворенных вежливостью, первичный контакт",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_4_2', openapi.IN_QUERY, description="Число удовлетворенных вежливостью, непоследственное оказание услуги",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_4_3', openapi.IN_QUERY, description="Число удовлетворенных вежливостью, дистанционное взаимодействие",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_5_1', openapi.IN_QUERY, description="Число готовых рекомендовать учреждение",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_5_2', openapi.IN_QUERY, description="Число удовлетворенных графиком/навигацией",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('count_person_5_3', openapi.IN_QUERY, description="Число удовлетворенных условиями оказания услуг",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        rating = {}

        checking = request.query_params.get('id_checking')
        organisation = request.query_params.get('id_organisation')
        type_organisation = request.query_params.get('id_type_organisation')

        count_person = {
            "count_person_1_3_stend": request.query_params.get('count_person_1_3_stend'),
            "count_person_1_3_web": request.query_params.get('count_person_1_3_web'),
            "count_person_2_2_2": request.query_params.get('count_person_2_2_2'),
            "count_person_2_3": request.query_params.get('count_person_2_3'),
            "count_invalid_person_3_3": request.query_params.get('count_invalid_person_3_3'),
            "count_person_4_1": request.query_params.get('count_person_4_1'),
            "count_person_4_2": request.query_params.get('count_person_4_2'),
            "count_person_4_3": request.query_params.get('count_person_4_3'),
            "count_person_5_1": request.query_params.get('count_person_5_1'),
            "count_person_5_2": request.query_params.get('count_person_5_2'),
            "count_person_5_3": request.query_params.get('count_person_5_3')
        }

        try:
            ratings_set = Ratings.objects.filter(checking_id=checking, type_organisations=type_organisation).get(organisations_id=organisation)
        except:
            return Response({'error': 'Не найдены данные о рейтингах запрашиваемой проверки.'})

        ratings = ratings_set.ratings_json

        if type_organisation == '1' or type_organisation == '10':
            rating = culture_rating(ratings, count_person)
        elif type_organisation == '2' or type_organisation == '3':
            rating = healthcare_rating(ratings, count_person)
        elif type_organisation == '4' or type_organisation == '5' or type_organisation == '7' or type_organisation == '9':
            rating = education_rating(ratings, count_person)

        return Response({"ratings": rating})