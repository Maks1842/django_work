from ...app_models import *
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from drf_yasg2.utils import swagger_auto_schema, unset
from drf_yasg2 import openapi
from django.db import IntegrityError, transaction
from rest_framework.permissions import IsAdminUser

from ...app_serializers.ratings_serializer import RatingsSerializer

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



class RatingsAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['get'],
        tags=['Рейтинг'],
        operation_description="Получить результаты рейтингов",
        manual_parameters=[
            openapi.Parameter('checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER),

        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        checking = request.query_params.get('checking')
        organisation = request.query_params.get('organisation')
        type_organisation = request.query_params.get('type_organisation')

        try:
            ratings_set = Ratings.objects.filter(checking_id=checking, type_organisations=type_organisation).get(organisations_id=organisation)
        except:
            return Response({'error': 'Не найдены данные о рейтингах запрашиваемой проверки.'})

        ratings = ratings_set.ratings_json
        return Response(ratings)

    @swagger_auto_schema(
        methods=['post'],
        tags=['Рейтинг'],
        operation_description="Добавить/изменить результаты рейтингов",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'checking': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор проверки'),
                'organisations': openapi.Schema(type=openapi.TYPE_INTEGER, description='Идентификатор организации'),
                'type_organisations': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                     description='Идентификатор типа организации'),
                'ratings_json': openapi.Schema(type=openapi.TYPE_STRING, description='Результаты рейтингов'),
            }
        ))
    @action(methods=['post'], detail=True)
    def post(self, request):
        req_data = request.data

        serializers = RatingsSerializer(data=req_data)
        serializers.is_valid(raise_exception=True)
        try:
            Ratings.objects.update_or_create(
                checking=Checking.objects.get(pk=req_data['checking']),
                organisations=Organisations.objects.get(pk=req_data['organisations']),
                type_organisations=Type_Organisations.objects.get(pk=req_data['type_organisations']),
                defaults={'ratings_json': req_data['ratings_json']},
            )
        except IntegrityError:
            return Response({"error": "Ошибка при добавлении/изменении данных"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        return Response({'message': 'Рейтинг успешно сохранен'})