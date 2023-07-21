from django.contrib import admin

from .app_models import Profile_Position
from .app_models.profile import Profile
from .app_models.regions import Regions
from .app_models.type_departments import Type_Departments
from .app_models.answers import Answers
from .app_models.checking import Checking
from .app_models.comments import Comments
from .app_models.department_persons import Department_Persons
from .app_models.departments import Departments
from .app_models.form_sections import Form_Sections
from .app_models.form_sections_question import Form_Sections_Question
from .app_models.form_type_organisation import Form_Type_Organisation
from .app_models.forms_act import FormsAct
from .app_models.forms_recommendations import Forms_Recommendations
from .app_models.list_checking import List_Checking
from .app_models.organisation_persons import Organisation_Persons
from .app_models.organisations import Organisations
from .app_models.photo import Photo
from .app_models.question_values import Question_Values
from .app_models.questions import Questions
from .app_models.ratings import Ratings
from .app_models.signed_dociuments import Signed_Dociuments
from .app_models.templates import Templates
from .app_models.transaction_exchange import Transaction_Exchange
from .app_models.type_answers import Type_Answers
from .app_models.type_templates import Type_Templates
from .app_models.type_organisations import Type_Organisations
from .app_models.versions import Versions
from .app_models.recommendations import Recommendations
from .app_models.coefficients import Coefficients


# Настройка админки

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'address', 'birthday', 'position', 'is_deleted')  # Указываю какие поля отображать
    search_fields = ('user', 'address', 'birthday', 'position')  # Указываю по каким полям можно осуществлять поиск
    list_editable = ('user', 'phone', 'address', 'birthday', 'position', 'is_deleted')  # Возможность редактирования поля
    list_filter = ('user', 'address', 'birthday', 'position')  # Возможность фильтровать поля


class Profile_PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'position')  # Указываю какие поля отображать
    search_fields = ('position',)  # Указываю по каким полям можно осуществлять поиск
    list_editable = ('position',)  # Возможность редактирования поля
    list_filter = ('position',)  # Возможность фильтровать поля


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'region_name', 'area_geojson', 'district_geojson', 'is_deleted')  # Указываю какие поля отображать
    search_fields = ('region_name',)  # Указываю по каким полям можно осуществлять поиск
    list_editable = ('region_name', 'area_geojson', 'district_geojson', 'is_deleted')  # Возможность редактирования поля
    list_filter = ('region_name',)  # Возможность фильтровать поля


class Type_DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'is_deleted')
    search_fields = ('type',)
    list_editable = ('type', 'is_deleted')
    list_filter = ('type',)


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments',
    'is_deleted', 'user')
    search_fields = ('department_name', 'address', 'parent', 'region', 'type_departments', 'user')
    list_editable = (
    'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'user')
    list_filter = ('department_name', 'region', 'type_departments', 'user')


class Department_PersonsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted')
    search_fields = ('last_name', 'position', 'department')
    list_editable = ('last_name', 'position', 'department', 'is_deleted')
    list_filter = ('department',)


class Type_OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'type_departments', 'is_deleted')
    search_fields = ('type', 'type_departments')
    list_editable = ('type', 'type_departments', 'is_deleted')
    list_filter = ('type', 'type_departments')


class OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'inn', 'kpp', 'ogrn', 'longitude', 'latitude', 'is_deleted')
    search_fields = ('organisation_name', 'address', 'parent__organisation_name', 'department__department_name', 'inn', 'kpp', 'ogrn')
    list_editable = ('organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'inn', 'kpp', 'ogrn', 'longitude', 'latitude', 'is_deleted')
    list_filter = ('organisation_name', 'department')


class Form_Type_OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation', 'type_organisation')
    search_fields = ('organisation', 'type_organisation')
    list_editable = ('organisation', 'type_organisation')
    list_filter = ('organisation', 'type_organisation')


class Organisation_PersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'organisation', 'is_deleted')
    search_fields = ('first_name', 'second_name', 'last_name', 'position', 'organisation__organisation_name')
    list_editable = ('first_name', 'second_name', 'last_name', 'position', 'organisation')



class RatingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisations', 'type_organisations', 'checking', 'ratings_json', 'is_deleted')
    search_fields = ('organisations', 'type_organisations', 'checking', 'ratings_json')
    list_editable = ('organisations', 'type_organisations', 'checking', 'ratings_json', 'is_deleted')
    list_filter = ('organisations', 'type_organisations', 'checking')


class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_organisations', 'template_file', 'type_templates', 'version', 'is_deleted')
    search_fields = ('name', 'type_organisations', 'template_file', 'type_templates', 'version')
    list_editable = ('name', 'type_organisations', 'template_file', 'type_templates', 'version', 'is_deleted')
    list_filter = ('name', 'type_organisations', 'type_templates', 'version')


class Form_SectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'order_num', 'parent', 'type_departments', 'employ_in_act', 'rating_key', 'raring_order_num', 'is_deleted')
    search_fields = ('name', 'version', 'order_num', 'parent', 'type_departments',  'employ_in_act', 'rating_key',  'raring_order_num')
    list_editable = ('name', 'version', 'order_num', 'parent', 'type_departments', 'employ_in_act', 'rating_key', 'raring_order_num', 'is_deleted')
    list_filter = ('name', 'version', 'type_departments')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions')
    search_fields = ('questions',)
    list_editable = ('questions',)


class Question_ValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'value_name', 'name_alternativ', 'special_option')
    search_fields = ('value_name', 'name_alternativ', 'special_option')
    list_editable = ('value_name', 'name_alternativ', 'special_option')


class Form_Sections_QuestionAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations',
    'required', 'is_deleted')
    search_fields = (
    'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'required')
    list_editable = (
    'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'required', 'is_deleted')


class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted')
    search_fields = ('name',)
    list_editable = ('name', 'is_deleted')


class Forms_RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted')
    search_fields = ('answers', 'form_sections', 'recommendations')
    list_editable = ('free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted')


class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisations', 'type_organisations', 'checking', 'answers_json', 'quota', 'invalid_person', 'comments', 'is_deleted')
    search_fields = ('organisations', 'type_organisations', 'checking', 'answers_json' 'quota', 'invalid_person',)
    list_editable = ('organisations', 'type_organisations', 'checking', 'answers_json', 'quota', 'invalid_person', 'comments', 'is_deleted')
    list_filter = ('organisations', 'type_organisations', 'checking')


class Signed_DociumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'originat_file_name', 'description', 'created_at', 'is_deleted', 'user')
    search_fields = ('file_name', 'originat_file_name', 'created_at', 'is_deleted', 'user')
    list_editable = ('file_name', 'originat_file_name', 'description', 'created_at', 'is_deleted', 'user')
    list_filter = ('file_name', 'created_at', 'is_deleted', 'user')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_value', 'is_deleted')
    search_fields = ('free_value', 'is_deleted')
    list_editable = ('free_value', 'is_deleted')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'original_file_name', 'description', 'created_at', 'is_deleted', 'user')
    search_fields = ('file_name', 'original_file_name', 'created_at', 'is_deleted', 'user')
    list_editable = ('file_name', 'original_file_name', 'description', 'created_at', 'is_deleted', 'user')
    list_filter = ('file_name', 'created_at', 'is_deleted', 'user')


class VersionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_name', 'version', 'active', 'is_deleted')
    search_fields = ('table_name', 'version', 'active', 'is_deleted')
    list_editable = ('table_name', 'version', 'active', 'is_deleted')
    list_filter = ('table_name', 'version', 'active', 'is_deleted')

class Type_AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type',)
    list_editable = ('type',)


class Type_TemplatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type',)
    list_editable = ('type',)


class Transaction_ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'field', 'old_data', 'new_data', 'date_exchange', 'user')
    search_fields = ('model', 'field', 'old_data', 'new_data', 'user')
    list_editable = ('model', 'field', 'old_data', 'new_data', 'user')


class FormsActAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_departments', 'type_organisations', 'act_json', 'act_json_to_calculate', 'date', 'version')
    search_fields = ('type_departments', 'type_organisations', 'act_json', 'act_json_to_calculate', 'date', 'version')
    list_editable = ('type_departments', 'type_organisations', 'act_json', 'act_json_to_calculate', 'date', 'version')
    list_filter = ('type_departments', 'type_organisations', 'date', 'version')


class CheckingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_checking', 'region', 'department', 'finished', 'is_deleted')
    search_fields = ('name', 'date_checking', 'region', 'department', 'finished', 'is_deleted')
    list_editable = ('name', 'date_checking', 'region', 'department', 'finished', 'is_deleted')
    list_filter = ('name', 'date_checking', 'region', 'department', 'finished', 'is_deleted')


class ListCheckingAdmin(admin.ModelAdmin):
    list_display = ('id', 'checking', 'organisation', 'person', 'user', 'date_check_org', 'is_deleted')
    search_fields = ('checking', 'organisation', 'person', 'user', 'date_check_org', 'is_deleted')
    list_editable = ('checking', 'organisation', 'person', 'user', 'date_check_org', 'is_deleted')
    list_filter = ('checking', 'organisation', 'person', 'user', 'date_check_org', 'is_deleted')


class CoefficientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_departments', 'type_organisations', 'main_json', 'respondents_json', 'points_json', 'date', 'version')
    search_fields = ('type_departments', 'type_organisations', 'main_json', 'respondents_json', 'points_json', 'date', 'version')
    list_editable = ('type_departments', 'type_organisations', 'main_json', 'respondents_json', 'points_json', 'date', 'version')
    list_filter = ('type_departments', 'type_organisations', 'date', 'version')


# !!!Важно соблюдать последовательность регистрации моделей
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Profile_Position, Profile_PositionAdmin)
admin.site.register(Regions, RegionsAdmin)
admin.site.register(Type_Departments, Type_DepartmentsAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(Department_Persons, Department_PersonsAdmin)
admin.site.register(Type_Organisations, Type_OrganisationsAdmin)
admin.site.register(Organisations, OrganisationsAdmin)
admin.site.register(Form_Type_Organisation, Form_Type_OrganisationAdmin)
admin.site.register(Organisation_Persons, Organisation_PersonsAdmin)
admin.site.register(Ratings, RatingsAdmin)
admin.site.register(Templates, TemplatesAdmin)
admin.site.register(Form_Sections, Form_SectionsAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Question_Values, Question_ValuesAdmin)
admin.site.register(Form_Sections_Question, Form_Sections_QuestionAdmin)
admin.site.register(Recommendations, RecommendationsAdmin)
admin.site.register(Forms_Recommendations, Forms_RecommendationsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Signed_Dociuments, Signed_DociumentsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Versions, VersionsAdmin)
admin.site.register(Type_Answers, Type_AnswersAdmin)
admin.site.register(Type_Templates, Type_TemplatesAdmin)
admin.site.register(Transaction_Exchange, Transaction_ExchangeAdmin)
admin.site.register(FormsAct, FormsActAdmin)
admin.site.register(Checking, CheckingAdmin)
admin.site.register(List_Checking, ListCheckingAdmin)
admin.site.register(Coefficients, CoefficientsAdmin)
