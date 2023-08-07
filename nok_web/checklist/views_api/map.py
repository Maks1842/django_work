import json

from ..app_models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from django.http import HttpResponse
from django.db import connection
import re


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

        features = []
        if len(orgs) > 0:
            for org in orgs:
                organisation = Organisations.objects.get(id=org["organisation_id"])
                feature = {
                    "type": "Feature",
                    "properties": {
                        "name": organisation.organisation_name,
                        "id": organisation.id,
                    },
                    "geometry": {
                        "coordinates": [
                            organisation.longitude,
                            organisation.latitude
                        ],
                        "type": "Point"
                    }
                }
                features.append(feature)
        return Response({"type": "FeatureCollection", "features": features})


class GetRegionAreaByCheckIdAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Карты'],
        operation_description="Получить границы региона в формате Feature GeoJson",
        manual_parameters=[
            openapi.Parameter('id_region', openapi.IN_QUERY, description="Идентификатор региона",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        id_region = request.query_params.get('id_region')
        region = Regions.objects.get(id=id_region)
        file_pointer = open(f'./checklist/local_storage/geo/{region.area_geojson}', "rb")
        response = HttpResponse(file_pointer, content_type='application/json;')
        response['Content-Disposition'] = f'attachment; filename={region.area_geojson}'
        response['Content-Transfer-Encoding'] = 'utf-8'
        return response


class GetDistrictsAreaByCheckIdAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Карты'],
        operation_description="Получить границы районов региона в формате Feature GeoJson",
        manual_parameters=[
            openapi.Parameter('id_region', openapi.IN_QUERY, description="Идентификатор региона",
                              type=openapi.TYPE_INTEGER),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        id_region = request.query_params.get('id_region')
        region = Regions.objects.get(id=id_region)
        file_pointer = open(f'./checklist/local_storage/geo/{region.district_geojson}', "rb")
        response = HttpResponse(file_pointer, content_type='application/json;')
        response['Content-Disposition'] = f'attachment; filename={region.district_geojson}'
        response['Content-Transfer-Encoding'] = 'utf-8'
        return response


class GetDistrictAreaAPIView(APIView):
    @swagger_auto_schema(
        methods=['get'],
        tags=['Карты'],
        operation_description="Получить границы районов региона в формате Feature GeoJson",
        manual_parameters=[
            openapi.Parameter('okato', openapi.IN_QUERY, description="Идентификаторы региона через запятую",
                              type=openapi.TYPE_STRING),
        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        okato = request.query_params.get('okato')
        okato = re.sub("[\"\']", "", okato)
        okatos = []
        if "," in okato:
            okatos = okato.split(',')
        else:
            okatos.append(okato)
        codes = ''
        for code in okatos:
            if codes == '':
                codes = f"'{code.strip()}'"
            else:
                codes = codes + f",'{code.strip()}'"
        with connection.cursor() as cursor:
            sql = f"""select obj from checklist_districtarea t, jsonb_array_elements(t.data -> 'features') obj where obj -> 'properties' -> 'OKATO_CODE'  ?| array[{codes}]"""
            cursor.execute(sql)
            rows = cursor.fetchall()
        features = []
        for row in rows:
            features.append(json.loads(''.join(row)))
        return Response({"type": "FeatureCollection", "features": features})
