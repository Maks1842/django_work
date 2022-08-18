
from django.urls import path, include
from .views import *
from .api_views import *
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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
router.register(r'regions', RegionsViewSet)
router.register(r'departments', DepartmentsViewSet)

urlpatterns = [
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('api/regions/', RegionsAPIView.as_view()),                 # Для v3
    # path('api/regions/<int:pk>/', RegionsAPIView.as_view()),        # Для v3
    # path('api/regions/', RegionsAPIList.as_view()),                   # Для v2
    # path('api/regions/<int:pk>/', RegionsAPIUpdate.as_view()),        # Для v2
    # path('api/regionsdetail/<int:pk>/', RegionsAPIDetailView.as_view()),   # Для v2

    # path('api/regions/', RegionsViewSet.as_view({'get': 'list'})),                   # Для v1 (без использования router)
    # path('api/regions/<int:pk>/', RegionsViewSet.as_view({'put': 'update'})),        # Для v1 (без использования router)
    path('api/', include(router.urls)),                                        # Для v1 (с использованием router)



    # path('api/type_departments/', Type_DepartmentsListAPIView.as_view(), name='api_type_departments'),
    # path('api/departments/', DepartmentsListAPIView.as_view(), name='api_departments'),
    # path('api/department_persons/', Department_PersonsListAPIView.as_view(), name='api_department_persons'),
    # path('api/type_organisations/', Type_OrganisationsListAPIView.as_view(), name='api_type_organisations'),
    # path('api/organisations/', OrganisationsListAPIView.as_view(), name='api_organisations'),
    # path('api/organisation_persons/', Organisation_PersonsListAPIView.as_view(), name='api_organisation_persons'),
    # path('api/quota/', QuotaListAPIView.as_view(), name='api_quota'),
    # path('api/templates/', TemplatesListAPIView.as_view(), name='api_templates'),
    # path('api/forms/', FormsListAPIView.as_view(), name='api_forms'),
    # path('api/form_sections/', Form_SectionsListAPIView.as_view(), name='api_form_sections'),
    # path('api/questions/', QuestionsListAPIView.as_view(), name='api_questions'),
    # path('api/question_values/', Question_ValuesListAPIView.as_view(), name='question_values'),
    # path('api/form_sections_question/', Form_Sections_QuestionListAPIView.as_view(), name='api_form_sections_question'),
    # path('api/recommendations/', RecommendationsListAPIView.as_view(), name='api_recommendations'),
    # path('api/forms_recommendations/', Forms_RecommendationsListAPIView.as_view(), name='api_forms_recommendations'),
    # path('api/answers/', AnswersListAPIView.as_view(), name='api_answers'),
    # path('api/signed_dociuments/', Signed_DociumentsListAPIView.as_view(), name='api_signed_dociuments'),
    # path('api/evaluation/', EvaluationListAPIView.as_view(), name='api_evaluation'),
    # path('api/versions/', VersionsListAPIView.as_view(), name='api_versions'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('', region_view, name='home'),
    path('question_view/', question_view, name='question_view'),
    path('departments/', LibDepartments.as_view(), name='departments'),           # пример регистрации маршрута для контроллера классов. В скобках .as_view() можно передавать дополнительные параметры
    path('organisation/', HomeDepartments.as_view(), name='organisation'),
]