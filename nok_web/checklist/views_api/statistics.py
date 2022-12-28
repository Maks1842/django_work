from ..app_models import *
from ..app_serializers.answers_serializer import AnswersSerializer
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from drf_yasg2.utils import swagger_auto_schema, unset
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


'''
Представления ApiView. Основной вариант.
'''


class GetCheckingsListAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Статистика'],
        operation_description="Получить список проверок.")
    @action(detail=False, methods=['get'])
    def get(self, request):

        queryset = Checking.objects.all()

        result = []
        for item in queryset:
            count_org_check = List_Checking.objects.filter(checking_id=item.id)
            count_org_complit = Answers.objects.filter(checking_id=item.id)
            result.append({
                'id': item.id,
                'nameCheck': item.name,
                'dateCheck': item.date_checking,
                'regionCheck': item.region.region_name,
                'departmentCheck': item.department.department_name,
                'countOrgAll': len(count_org_check),
                'countOrgComplit': len(count_org_complit),
            })
        return Response(result)


class GetOrganisationListAPIView(APIView):
    @swagger_auto_schema(
        method='get',
        tags=['Статистика'],
        operation_description="Получить список организаций, принадлежащих департаменту, по id проверки.",
        manual_parameters=[
                    openapi.Parameter('checking_id', openapi.IN_QUERY, description="Идентификатор проверки",
                                      type=openapi.TYPE_INTEGER)
                ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        checking = request.query_params.get('checking_id')
        department = Checking.objects.values('department').get(pk=checking)
        queryset = Organisations.objects.filter(department=department['department'])

        result = []
        for item in queryset:
            result.append({
                'id': item.id,
                'name': item.organisation_name,
            })
        return Response(result)


# class GetListCheckingAPIView(APIView):
#     @swagger_auto_schema(
#         method='get',
#         tags=['Проверка'],
#         operation_description="Получить список проверок, в которых участвует эксперт",
#         manual_parameters=[
#             openapi.Parameter('user_id', openapi.IN_QUERY, description="Идентификатор эксперта",
#                               type=openapi.TYPE_INTEGER)
#         ])
#     @action(detail=False, methods=['get'])
#     def get(self, request):
#         user = request.query_params.get('user_id')
#         queryset = List_Checking.objects.filter(user_id=user).distinct('checking')
#
#         result = []
#         if len(queryset) > 0:
#             for item in queryset:
#                 result.append({
#                     'id': item.checking.id,
#                     'name': item.checking.name,
#                 })
#         return Response({'data': result})