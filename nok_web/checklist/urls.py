
from django.urls import path, include, re_path
from .views import *
from .api_views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi


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


router = routers.DefaultRouter()

router.register(r'regions', RegionsViewSet, basename='regions')
router.register(r'type_departments', Type_DepartmentsViewSet, basename='type_departments')
router.register(r'departments', DepartmentsViewSet, basename='departments')
router.register(r'department_persons', Department_PersonsViewSet, basename='department_persons')
router.register('type_organisations', Type_OrganisationsViewSet, basename='type_organisations')
router.register('organisations', OrganisationsViewSet, basename='organisations')
router.register('organisation_persons', Organisation_PersonsViewSet, basename='organisation_persons')
router.register('quota', QuotaViewSet, basename='quota')
router.register('templates', TemplatesViewSet, basename='templates')
router.register('forms', FormsViewSet, basename='forms')
router.register('form_sections', Form_SectionsViewSet, basename='form_sections')
router.register('questions', QuestionsViewSet, basename='questions')
router.register('question_values', Question_ValuesViewSet, basename='question_values')
router.register('form_sections_question', Form_Sections_QuestionViewSet, basename='form_sections_question')
router.register('recommendations', RecommendationsViewSet, basename='recommendations')
router.register('forms_recommendations', Forms_RecommendationsViewSet, basename='forms_recommendations')
router.register('answers', AnswersViewSet, basename='answers')
router.register('signed_dociuments', Signed_DociumentsViewSet, basename='signed_dociuments')
router.register('evaluation', EvaluationViewSet, basename='evaluation')
router.register('versions', VersionsViewSet, basename='versions')
router.register('type_answers', Type_AnswersViewSet, basename='type_answers')
router.register('transaction_exchange', Transaction_ExchangeViewSet, basename='transaction_exchange')



urlpatterns = [
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),                             # Для v1 (с использованием router)
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),
    # path('api/v1/drf-auth/', include('res_framework.urls')),
    # path(r'^auth/', include('djoser.urls')),


    path('', region_view, name='home'),
    path('question_view/', question_view, name='question_view'),
    path('departments/', LibDepartments.as_view(), name='departments'),           # пример регистрации маршрута для контроллера классов. В скобках .as_view() можно передавать дополнительные параметры
    path('organisation/', HomeDepartments.as_view(), name='organisation'),


    path('api/get_medicine_act/', Get_Medicine_ActAPIView.as_view()),
    path('api/get_education_oo_act/', Get_EducationOO_ActAPIView.as_view()),



    # path('api/regions-put/<int:pk>/', RegionsAPIView.as_view()),        # Для v2
    # path('api/departments-put/<int:pk>/', DepartmentsAPIDetailView.as_view()),        # Для v2

    # path('api/regions/', RegionsViewSet.as_view({'get': 'list'})),                   # Для v1 (без использования router)
    # path('api/regions/<int:pk>/', RegionsViewSet.as_view({'put': 'update'})),        # Для v1 (без использования router)
]