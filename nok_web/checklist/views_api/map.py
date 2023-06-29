from ..app_models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi


class GetMapByCheckIdAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Карты'],
        operation_description="Получить координаты организаций по проверке",
        manual_parameters=[
            openapi.Parameter('id_check', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        id_check = request.query_params.get('id_check')
        orgs = List_Checking.objects.filter(checking_id=id_check).values()

        items = []
        if len(orgs) > 0:
            for org in orgs:
                organisation = Organisations.objects.get(id=org["organisation_id"])
                items.append({
                    'id': organisation.id,
                    'name': organisation.organisation_name,
                    'longitude': organisation.longitude,
                    'latitude': organisation.latitude
                })
        return Response({'items': items})
