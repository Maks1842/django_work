from django.urls import path
from .views import *
from . import api

urlpatterns = [
    path('api/regions/', api.RegionsListAPIView.as_view(), name='api_regions'),
    path('api/type_departments/', api.Type_DepartmentsListAPIView.as_view(), name='api_type_departments'),
    path('api/departments/', api.DepartmentsListAPIView.as_view(), name='api_departments'),
    path('api/department_persons/', api.Department_PersonsListAPIView.as_view(), name='api_department_persons'),
    path('api/type_organisations/', api.Type_OrganisationsListAPIView.as_view(), name='api_type_organisations'),
    path('api/organisations/', api.OrganisationsListAPIView.as_view(), name='api_organisations'),
    path('api/organisation_persons/', api.Organisation_PersonsListAPIView.as_view(), name='api_organisation_persons'),
    path('api/quota/', api.QuotaListAPIView.as_view(), name='api_quota'),
    path('api/templates/', api.TemplatesListAPIView.as_view(), name='api_templates'),
    path('api/forms/', api.FormsListAPIView.as_view(), name='api_forms'),
    path('api/form_sections/', api.Form_SectionsListAPIView.as_view(), name='api_form_sections'),
    path('api/questions/', api.QuestionsListAPIView.as_view(), name='api_questions'),
    path('api/question_values/', api.Question_ValuesListAPIView.as_view(), name='question_values'),
    path('api/form_sections_question/', api.Form_Sections_QuestionListAPIView.as_view(), name='api_form_sections_question'),
    path('api/recommendations/', api.RecommendationsListAPIView.as_view(), name='api_recommendations'),
    path('api/forms_recommendations/', api.Forms_RecommendationsListAPIView.as_view(), name='api_forms_recommendations'),
    path('api/answers/', api.AnswersListAPIView.as_view(), name='api_answers'),
    path('api/signed_dociuments/', api.Signed_DociumentsListAPIView.as_view(), name='api_signed_dociuments'),
    path('api/evaluation/', api.EvaluationListAPIView.as_view(), name='api_evaluation'),
    path('api/versions/', api.VersionsListAPIView.as_view(), name='api_versions'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('', region_view, name='home'),
    path('question_view/', question_view, name='question_view'),
    path('departments/', LibDepartments.as_view(), name='departments'),           # пример регистрации маршрута для контроллера классов. В скобках .as_view() можно передавать дополнительные параметры
    path('organisation/', HomeDepartments.as_view(), name='organisation'),
]