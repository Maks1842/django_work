from ..app_models import *
from ..app_serializers.answers_serializer import AnswersSerializer
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from drf_yasg2.utils import swagger_auto_schema, unset
from drf_yasg2 import openapi
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser


'''
Представления ApiView. Основной вариант.
'''


class GetCheckingsListAPIView(APIView):

    permission_classes = [IsAdminUser]
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

    permission_classes = [IsAdminUser]
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


class GetStatisticUserAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        method='get',
        tags=['Статистика'],
        operation_description="Получить список проверок и организаций, по id эксперта.",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Идентификатор эксперта",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        user = request.query_params.get('user_id')

        user_set = User.objects.values().get(pk=user)
        user_name = user_set['first_name']

        queryset = List_Checking.objects.filter(user=user).values()
        checkings = queryset.values('checking_id').distinct()

        result = []
        for item in checkings:
            check_id = item['checking_id']
            checking = Checking.objects.get(pk=check_id)
            org_list = queryset.filter(checking_id=check_id)

            org_data = []
            count_all = 0
            count_end = 0
            for org in org_list:
                count_all += 1
                org_id = org['organisation_id']
                organisation = Organisations.objects.values().get(pk=org_id)


                if Answers.objects.filter(checking_id=check_id, organisations_id=org_id).exists():
                    statusCheck = 'Завершена'
                    count_end += 1
                else:
                    statusCheck = 'Ожидает'

                org_data.append({"nameOrg": organisation['organisation_name'],
                                 "dateCheckOrg": org['date_check_org'],
                                 "statusCheck": statusCheck})

            result.append({
                           "user": user_name,
                           "nameCheck": checking.name,
                           "dateCheck": checking.date_checking,
                           "organisationsNum": {
                               "checkEnd": count_end,
                               "checkAll": count_all
                           },
                           "organisations": org_data})

        return Response(result)