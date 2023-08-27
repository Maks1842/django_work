from django.urls import path, include, re_path

from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from rest_framework import permissions
from drf_yasg2.views import get_schema_view

from .views_api.act_answer_into_pdf import *
from .views_api.map import *
from .views_api.calculating_rating.base_calculate_api import CalculatingRatingAPIView
from .views_api.calculating_rating.change_ratings_api import ChangeRatingsAPIView
from .views_api.calculating_rating.ratings_api import RatingsAPIView, RatingCheckingsListAPIView
from .views_api.calculating_rating.ratings_into_pdf import GetRatingsIntoPdfAPIView
from .views_api.calculating_rating.ratings_to_excel import ExportRatingsToExcelAPIView
from .views_api.checking_organisations import AnswersAPIView, GetFormActByOrganizationTypeAPIView, \
    GetCheckListOrganizationsAPIView, GetListCheckingAPIView, GetCheckingCompletedAPIView, \
    InvalidPersonAPIView, CommentsCheckingAPIView, AddPersonToCheckingAPIView
from .views_api.organisations import OrganisationPersonsAPIView, GetListTypeOrganizationsAPIView
from .views_api.statistics import StatisticUserAPIView, StatisticCheckingsListAPIView, StatisticOrganisationListAPIView
from .views_api.admin_api import RegionsViewSet, GetActAPIView, GetPositionUserAPIView, \
    GetProfileUserAPIView, GetActGroupingAPIView, DepartmentsAPIView, CheckingAPIView, OrganisationsAPIView, \
    ListCheckingAPIView, RegionsAPIView, PersonsAPIView, UsersAPIView, DepartmentTypesAPIView, \
    ImportRegistryExcelAPIView, DistrictsAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()
router.register(r'regions', RegionsViewSet, basename='regions')


urlpatterns = [
    # Маршрутизация с использованием router
    path('api/', include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^api/v1/auth/', include('djoser.urls.authtoken')),

    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Основные API проверки
    path('api/v1/Answers/', AnswersAPIView.as_view(), name='Answers'),
    path('api/v1/OrganisationPersons/', OrganisationPersonsAPIView.as_view(), name='OrganisationPersons'),
    path('api/v1/getListTypeOrganizations/', GetListTypeOrganizationsAPIView.as_view(), name='GetListTypeOrganizations'),
    path('api/v1/getFormActByOrganizationType/', GetFormActByOrganizationTypeAPIView.as_view(), name='GetFormActByOrganizationType'),
    path('api/v1/getCheckListOrganizations/', GetCheckListOrganizationsAPIView.as_view(), name='GetCheckListOrganizations'),
    path('api/v1/getListChecking/', GetListCheckingAPIView.as_view(), name='GetListChecking'),
    # path('api/v1/getFormActByOrganizationId/', GetFormActByOrganizationIdAPIView.as_view(), name='getFormActByOrganizationId'),
    path('api/v1/getResultCheckingIntoPdf/', GetResultCheckingIntoPdfAPIView.as_view(), name='GetResultCheckingIntoPdf'),
    path('api/v1/getCheckingCompleted/', GetCheckingCompletedAPIView.as_view(), name='GetResultCheckingIntoPdf'),
    path('api/v1/CommentsChecking/', CommentsCheckingAPIView.as_view(), name='CommentsChecking'),
    path('api/v1/InvalidPerson/', InvalidPersonAPIView.as_view(), name='InvalidPerson'),
    path('api/v1/AddPersonToChecking/', AddPersonToCheckingAPIView.as_view(), name='AddPersonToChecking'),

    # Для Статистики
    path('api/v1/StatisticCheckingsList/', StatisticCheckingsListAPIView.as_view(), name='StatisticCheckingsList'),
    path('api/v1/StatisticOrganisationList/', StatisticOrganisationListAPIView.as_view(), name='StatisticOrganisationList'),
    path('api/v1/StatisticUser/', StatisticUserAPIView.as_view(), name='StatisticUser'),

    # Для Рейтингов
    path('api/v1/CalculatingRating/', CalculatingRatingAPIView.as_view(), name='CalculatingRating'),
    path('api/v1/ChangeRatings/', ChangeRatingsAPIView.as_view(), name='ChangeRatings'),
    path('api/v1/Ratings/', RatingsAPIView.as_view(), name='Ratings'),
    path('api/v1/RatingCheckingsList/', RatingCheckingsListAPIView.as_view(), name='RatingCheckingsList'),
    path('api/v1/getRatingsIntoPdf/', GetRatingsIntoPdfAPIView.as_view(), name='GetRatingsIntoPdf'),
    path('api/v1/ExportRatingsToExcel/', ExportRatingsToExcelAPIView.as_view(), name='ExportRatingsToExcel'),

    # Для Админа
    path('api/v1/getActGrouping/', GetActGroupingAPIView.as_view(), name='GetActGrouping'),
    path('api/v1/getAct/', GetActAPIView.as_view(), name='GetAct'),
    path('api/v1/getPositionUser/', GetPositionUserAPIView.as_view(), name='GetPositionUser'),
    path('api/v1/getProfileUser/', GetProfileUserAPIView.as_view(), name='GetProfileUser'),
    path('api/v1/Regions/', RegionsAPIView.as_view(), name='Regions'),
    path('api/v1/Departments/', DepartmentsAPIView.as_view(), name='Departments'),
    path('api/v1/Checking/', CheckingAPIView.as_view(), name='Checking'),
    path('api/v1/Organisations/', OrganisationsAPIView.as_view(), name='Organisations'),
    path('api/v1/ListChecking/', ListCheckingAPIView.as_view(), name='ListChecking'),
    path('api/v1/Persons/', PersonsAPIView.as_view(), name='Persons'),
    path('api/v1/Users/', UsersAPIView.as_view(), name='Users'),
    path('api/v1/DepartmentTypes/', DepartmentTypesAPIView.as_view(), name='DepartmentTypes'),
    path('api/v1/ImportRegistryExcel/', ImportRegistryExcelAPIView.as_view(), name='ImportRegistryExcel'),
    path('api/v1/Districts/', DistrictsAPIView.as_view(), name='Districts'),

    # Карта
    path('api/v1/GetMapByCheckId/', GetMapByCheckIdAPIView.as_view(), name='Maps'),
    path('api/v1/GetRegionAreaByCheckId/', GetRegionAreaByCheckIdAPIView.as_view(), name='Maps'),
    path('api/v1/GetDistrictsAreaByCheckId/', GetDistrictsAreaByCheckIdAPIView.as_view(), name='Maps'),
    path('api/v1/GetDistrictArea/', GetDistrictAreaAPIView.as_view(), name='Maps'),

    # Для Авторизации аутентификации
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),




    path('', organisation_view, name='home'),
    path('designer-act/', designer_act_view, name='designer-act'),
    path('forms-act-add/', forms_act_add, name='forms_act_add'),
]
