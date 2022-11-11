
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

router = routers.SimpleRouter()

router.register(r'regions', RegionsViewSet, basename='regions')
router.register(r'type_departments', TypeDepartmentsViewSet, basename='type_departments')
router.register(r'departments', DepartmentsViewSet, basename='departments')
router.register(r'department_persons', DepartmentPersonsViewSet, basename='department_persons')
router.register('type_organisations', TypeOrganisationsViewSet, basename='type_organisations')
router.register('organisations', OrganisationsViewSet, basename='organisations')
router.register('organisation_persons', OrganisationPersonsViewSet, basename='organisation_persons')
router.register('quota', QuotaViewSet, basename='quota')
router.register('templates', TemplatesViewSet, basename='templates')
router.register('forms', FormsViewSet, basename='forms')
router.register('form_sections', FormSectionsViewSet, basename='form_sections')
router.register('questions', QuestionsViewSet, basename='questions')
router.register('question_values', QuestionValuesViewSet, basename='question_values')
router.register('form_sections_question', FormSectionsQuestionViewSet, basename='form_sections_question')
router.register('recommendations', RecommendationsViewSet, basename='recommendations')
router.register('forms_recommendations', FormsRecommendationsViewSet, basename='forms_recommendations')
router.register('answers', AnswersViewSet, basename='answers')
router.register('signed_dociuments', SignedDociumentsViewSet, basename='signed_dociuments')
router.register('evaluation', EvaluationViewSet, basename='evaluation')
router.register('versions', VersionsViewSet, basename='versions')
router.register('type_answers', TypeAnswersViewSet, basename='type_answers')
router.register('transaction_exchange', TransactionExchangeViewSet, basename='transaction_exchange')
router.register('forms_act', FormsActViewSet, basename='forms_act')
router.register('checking', CheckingViewSet, basename='checking')
router.register('list_checking', ListCheckingViewSet, basename='list_checking')


urlpatterns = [
    path('api/v1/get-act/', GetActAPIView.as_view(), name='get_act_drf'),

    path('api/v1/drf-auth/', include('rest_framework.urls')),

    # Маршрутизация с использованием router
    path('api/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),

    re_path(r'^api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', region_view, name='home'),
    path('question_view/', question_view, name='question_view'),
    path('designer-act/', designer_act_view, name='designer-act'),
    path('get-act/', get_act, name='get-act'),
    path('forms-act-add/', forms_act_add, name='forms_act_add'),
    path('forms-test-add/', forms_test_add, name='forms_test_add'),

    # Пример регистрации маршрута для контроллера классов. В скобках .as_view() можно передавать доп. параметры
    path('departments_xxx/', LibDepartments.as_view(), name='departments_xxx'),
    # path('designer-act/', HomeDepartments.as_view(), name='designer-act'),



    # path('api/regions-get/', RegionsAPIList.as_view()),
    # path('api/departments-get/<int:pk>/', DepartmentsAPIRetrieve.as_view()),
    # path('api/departments-get/<int:pk>/region/', DepartmentsAPIRetrieve.as_view()),

    # path('api/regions-put/<int:pk>/', RegionsAPIView.as_view()),        # Для v2
    # path('api/departments-put/<int:pk>/', DepartmentsAPIDetailView.as_view()),        # Для v2

    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),
    # path('api/v1/drf-auth/', include('res_framework.urls')),
    # path(r'^auth/', include('djoser.urls')),
]