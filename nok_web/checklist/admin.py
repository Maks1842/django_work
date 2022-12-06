from django.contrib import admin

from .app_models.regions import Regions
from .app_models.type_departments import Type_Departments
from .app_models.answers import Answers
from .app_models.checking import Checking
from .app_models.comments import Comments
from .app_models.department_persons import Department_Persons
from .app_models.departments import Departments
from .app_models.form_organisation_persons import Form_Organisation_Persons
from .app_models.form_sections import Form_Sections
from .app_models.form_sections_question import Form_Sections_Question
from .app_models.forms_act import FormsAct
from .app_models.forms_recommendations import Forms_Recommendations
from .app_models.list_checking import List_Checking
from .app_models.organisation_persons import Organisation_Persons
from .app_models.organisations import Organisations
from .app_models.photo import Photo
from .app_models.question_values import Question_Values
from .app_models.questions import Questions
from .app_models.quota import Quota

from .app_models.signed_dociuments import Signed_Dociuments
from .app_models.templates import Templates
from .app_models.transaction_exchange import Transaction_Exchange
from .app_models.type_answers import Type_Answers

from .app_models.type_organisations import Type_Organisations
from .app_models.versions import Versions
from .app_models.recommendations import Recommendations


# Настройка админки
class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'region_name', 'is_deleted')  # Указываю какие поля отображать
    search_fields = ('region_name', 'is_deleted')  # Указываю по каким полям можно осуществлять поиск
    list_editable = ('region_name', 'is_deleted')  # Возможность редактирования поля
    list_filter = ('region_name', 'is_deleted')  # Возможность фильтровать поля


class Type_DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'is_deleted')
    search_fields = ('type', 'is_deleted')
    list_editable = ('type', 'is_deleted')
    list_filter = ('type', 'is_deleted')


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments',
    'is_deleted', 'user')
    search_fields = ('department_name', 'address', 'parent', 'region', 'type_departments', 'is_deleted', 'user')
    list_editable = (
    'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'is_deleted',
    'user')
    list_filter = ('department_name', 'region', 'type_departments', 'is_deleted', 'user')


class Department_PersonsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted')
    search_fields = ('last_name', 'position', 'department', 'is_deleted')
    list_editable = ('last_name', 'position', 'department', 'is_deleted')
    list_filter = ('department', 'is_deleted')


class Type_OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'is_deleted')
    search_fields = ('type', 'is_deleted')
    list_editable = ('type', 'is_deleted')
    list_filter = ('type', 'is_deleted')


class OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota',
                    'type_organisations', 'is_deleted')
    search_fields = (
    'organisation_name', 'address', 'parent', 'department', 'quota', 'type_organisations', 'is_deleted')
    list_editable = (
    'organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota', 'type_organisations',
    'is_deleted')
    list_filter = ('organisation_name', 'department', 'quota', 'type_organisations', 'is_deleted')


class Organisation_PersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'is_deleted')
    search_fields = ('first_name', 'second_name', 'last_name', 'position', 'department', 'is_deleted')
    list_editable = ('first_name', 'second_name', 'last_name', 'position', 'is_deleted')


class Form_Organisation_PersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation', 'person')
    search_fields = ('organisation', 'person')
    list_editable = ('organisation', 'person')
    list_filter = ('organisation', 'person')


class QuotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'quota')
    search_fields = ('quota',)
    list_editable = ('quota',)
    list_filter = ('quota',)


class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_organisations', 'template_file', 'version', 'is_deleted')
    search_fields = ('name', 'type_organisations', 'template_file', 'version', 'is_deleted')
    list_editable = ('name', 'type_organisations', 'template_file', 'version', 'is_deleted')
    list_filter = ('name', 'type_organisations', 'version', 'is_deleted')


class Form_SectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'order_num', 'parent', 'type_departments', 'is_deleted')
    search_fields = ('name', 'version', 'order_num', 'parent', 'type_departments', 'is_deleted')
    list_editable = ('name', 'version', 'order_num', 'parent', 'type_departments', 'is_deleted')
    list_filter = ('name', 'version', 'type_departments', 'is_deleted')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions')
    search_fields = ('questions',)
    list_editable = ('questions',)


class Question_ValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'value_name', 'name_alternativ')
    search_fields = ('value_name', 'name_alternativ')
    list_editable = ('value_name', 'name_alternativ')


class Form_Sections_QuestionAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations',
    'is_deleted')
    search_fields = (
    'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'is_deleted')
    list_editable = (
    'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'is_deleted')


class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted')
    search_fields = ('name', 'is_deleted')
    list_editable = ('name', 'is_deleted')


class Forms_RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted')
    search_fields = ('answers', 'form_sections', 'recommendations', 'is_deleted')
    list_editable = ('free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted')


class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisations', 'checking', 'answers_json', 'is_deleted')
    search_fields = ('organisations', 'checking', 'answers_json', 'is_deleted')
    list_editable = ('organisations', 'checking', 'answers_json', 'is_deleted')
    list_filter = ('organisations', 'checking', 'is_deleted')


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


class Transaction_ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'field', 'old_data', 'new_data', 'date_exchange', 'user')
    search_fields = ('model', 'field', 'old_data', 'new_data', 'user')
    list_editable = ('model', 'field', 'old_data', 'new_data', 'user')


class FormsActAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_departments', 'type_organisations', 'act_json', 'date', 'version')
    search_fields = ('type_departments', 'type_organisations', 'act_json', 'date', 'version')
    list_editable = ('type_departments', 'type_organisations', 'act_json', 'date', 'version')
    list_filter = ('type_departments', 'type_organisations', 'date', 'version')


class CheckingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_checking', 'region', 'department', 'is_deleted')
    search_fields = ('name', 'date_checking', 'region', 'department', 'is_deleted')
    list_editable = ('name', 'date_checking', 'region', 'department', 'is_deleted')
    list_filter = ('name', 'date_checking', 'region', 'department', 'is_deleted')


class ListCheckingAdmin(admin.ModelAdmin):
    list_display = ('id', 'checking', 'organisation', 'user', 'is_deleted')
    search_fields = ('checking', 'organisation', 'user', 'is_deleted')
    list_editable = ('checking', 'organisation', 'user', 'is_deleted')
    list_filter = ('checking', 'organisation', 'user', 'is_deleted')


# !!!Важно соблюдать последовательность регистрации моделей
admin.site.register(Regions, RegionsAdmin)
admin.site.register(Type_Departments, Type_DepartmentsAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(Department_Persons, Department_PersonsAdmin)
admin.site.register(Type_Organisations, Type_OrganisationsAdmin)
admin.site.register(Organisations, OrganisationsAdmin)
admin.site.register(Organisation_Persons, Organisation_PersonsAdmin)
admin.site.register(Form_Organisation_Persons, Form_Organisation_PersonsAdmin)
admin.site.register(Quota, QuotaAdmin)
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
admin.site.register(Transaction_Exchange, Transaction_ExchangeAdmin)
admin.site.register(FormsAct, FormsActAdmin)
admin.site.register(Checking, CheckingAdmin)
admin.site.register(List_Checking, ListCheckingAdmin)
