from ...app_models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from drf_yasg2.utils import swagger_auto_schema, unset
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser
from django.core.paginator import Paginator

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

        ])
    @action(methods=['get'], detail=False)
    def get(self, request):
        checking = request.query_params.get('checking')
        organisation = request.query_params.get('organisation')

        try:
            ratings_set = Ratings.objects.filter(checking_id=checking).get(organisations_id=organisation)
        except:
            return Response({'error': 'Не найдены данные о рейтингах запрашиваемой проверки.'})

        ratings = ratings_set.ratings_json
        return Response(ratings)


class RatingCheckingsListAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        method='get',
        tags=['Рейтинг'],
        operation_description="Получить список проверок. Если страница не указана, то получить первую страницу",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Страница",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'])
    def get(self, request):
        page = request.query_params.get('page')

        if page is None:
            page = 1

        queryset = Checking.objects.all()
        paginator = Paginator(queryset, 20)

        items = []
        try:
            for item in paginator.page(page).object_list:
                items.append({
                    'id': item.id,
                    'nameCheck': item.name,
                    'dateCheck': item.date_checking,
                    'regionCheck': item.region.region_name,
                    'departmentCheck': item.department.department_name,
                    'departmentId': item.department.id,
                })
        except Exception as e:
            return Response({'error': f'{e}'})
        return Response({'totalPages': len(queryset), 'items': items})

