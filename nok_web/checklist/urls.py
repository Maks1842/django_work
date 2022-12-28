from django.urls import path, include, re_path

from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

from .views_api.act_answer_into_pdf import *
from .views_api.checking_organisations import AnswersAPIView, GetFormActByOrganizationTypeAPIView, \
    GetCheckListOrganizationsAPIView, GetListCheckingAPIView, GetCheckingCompletedAPIView
from .views_api.organisations import OrganisationPersonsAPIView, FormOrganisationPersonsAPIView, \
    GetListTypeOrganizationsAPIView
from .views_api.statistics import GetCheckingsListAPIView, GetOrganisationListAPIView
from .views_api.tests import RegionsViewSet, GetOrganisationTestAPIView

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
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    re_path(r'^api/v1/auth/', include('djoser.urls.authtoken')),

    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Маршрутизация без использования router. В скобках .as_view() можно передавать доп. параметры
    path('api/v1/Answers/', AnswersAPIView.as_view(), name='Answers'),
    path('api/v1/OrganisationPersons/', OrganisationPersonsAPIView.as_view(), name='OrganisationPersons'),
    path('api/v1/FormOrganisationPersons/', FormOrganisationPersonsAPIView.as_view(), name='FormOrganisationPersons'),
    path('api/v1/getListTypeOrganizations/', GetListTypeOrganizationsAPIView.as_view(), name='getListTypeOrganizations'),
    path('api/v1/getFormActByOrganizationType/', GetFormActByOrganizationTypeAPIView.as_view(), name='getFormActByOrganizationType'),
    path('api/v1/getCheckListOrganizations/', GetCheckListOrganizationsAPIView.as_view(), name='getCheckListOrganizations'),
    path('api/v1/getListChecking/', GetListCheckingAPIView.as_view(), name='getListChecking'),
    # path('api/v1/getFormActByOrganizationId/', GetFormActByOrganizationIdAPIView.as_view(), name='getFormActByOrganizationId'),
    path('api/v1/getResultCheckingIntoPdf/', GetResultCheckingIntoPdfAPIView.as_view(), name='getResultCheckingIntoPdf'),
    path('api/v1/getCheckingCompleted/', GetCheckingCompletedAPIView.as_view(), name='getResultCheckingIntoPdf'),

    path('api/v1/getCheckingsList/', GetCheckingsListAPIView.as_view(), name='getCheckingsList'),
    path('api/v1/getOrganisationList/', GetOrganisationListAPIView.as_view(), name='getOrganisationList'),

    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', organisation_view, name='home'),
    path('designer-act/', designer_act_view, name='designer-act'),
    path('forms-act-add/', forms_act_add, name='forms_act_add'),
    # path('get-act-answer/', get_act_answer, name='get-act-answer'),

    # path('api/v1/TESTGetOrganisation/', GetOrganisationTestAPIView.as_view(), name='GetOrganisationTest'),





    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),
    # path('api/v1/drf-auth/', include('res_framework.urls')),
    # path(r'^auth/', include('djoser.urls')),
]