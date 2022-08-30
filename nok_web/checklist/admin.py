from django.contrib import admin
from .models import *

# Настройка админки
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'region_name', 'is_deleted')                             # Указываю какие поля отображать
    search_fields = ('region_name', 'is_deleted')                                 # Указываю по каким полям можно осуществлять поиск
    list_editable = ('region_name', 'is_deleted')                                 # Возможность редактирования поля
    list_filter = ('region_name', 'is_deleted')                                   # Возможность фильтровать поля


class Type_DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'is_deleted')
    search_fields = ('type', 'is_deleted')
    list_editable = ('type', 'is_deleted')
    list_filter = ('type', 'is_deleted')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'is_deleted')
    search_fields = ('department_name', 'address', 'parent', 'region', 'type_departments', 'is_deleted')
    list_editable = ('department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'is_deleted')
    list_filter = ('department_name', 'address', 'parent', 'region', 'type_departments', 'is_deleted')


class Department_PersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted')
    search_fields = ('last_name', 'position', 'department', 'is_deleted')
    list_editable = ('first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted')
    list_filter = ('department', 'is_deleted')


class Type_OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'is_deleted')
    search_fields = ('type', 'is_deleted')
    list_editable = ('type', 'is_deleted')
    list_filter = ('type', 'is_deleted')


class OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota', 'type_organisations', 'is_deleted')
    search_fields = ('organisation_name', 'address', 'parent', 'department', 'quota', 'type_organisations', 'is_deleted')
    list_editable = ('organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota', 'type_organisations', 'is_deleted')
    list_filter = ('organisation_name', 'address', 'parent', 'department', 'quota', 'type_organisations', 'is_deleted')


class Organisation_PersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'organisation', 'is_deleted')
    search_fields = ('last_name', 'position', 'department', 'is_deleted')
    list_editable = ('first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'organisation', 'is_deleted')
    list_filter = ('organisation', 'is_deleted')


class QuotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'quota')
    search_fields = ('quota',)
    list_editable = ('quota',)
    list_filter = ('quota',)


class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template_file', 'version', 'is_deleted')
    search_fields = ('name', 'template_file', 'version', 'is_deleted')
    list_editable = ('name', 'template_file', 'version', 'is_deleted')
    list_filter = ('name', 'template_file', 'version', 'is_deleted')


class FormsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'created_at', 'type_departments', 'templates', 'is_deleted')
    search_fields = ('name', 'version', 'created_at', 'type_departments', 'templates', 'is_deleted')
    list_editable = ('name', 'version', 'created_at', 'type_departments', 'templates', 'is_deleted')
    list_filter = ('name', 'version', 'created_at', 'type_departments', 'templates', 'is_deleted')


class Form_SectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'order_num', 'parent', 'forms', 'type_departments', 'is_deleted')
    search_fields = ('name', 'version', 'order_num', 'parent', 'forms', 'type_departments', 'is_deleted')
    list_editable = ('name', 'version', 'order_num', 'parent', 'forms', 'type_departments', 'is_deleted')
    list_filter = ('name', 'version', 'order_num', 'parent', 'forms', 'type_departments', 'is_deleted')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'form_sections', 'type_answers', 'is_deleted')
    search_fields = ('name', 'form_sections', 'type_answers', 'is_deleted')
    list_editable = ('name', 'form_sections', 'type_answers', 'is_deleted')
    list_filter = ('name', 'form_sections', 'type_answers', 'is_deleted')


class Question_ValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'value_name', 'questions')
    search_fields = ('value_name', 'questions')
    list_editable = ('value_name', 'questions')
    list_filter = ('value_name', 'questions')


class Form_Sections_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions', 'forms', 'order_num', 'is_deleted')
    search_fields = ('questions', 'forms', 'order_num', 'is_deleted')
    list_editable = ('questions', 'forms', 'order_num', 'is_deleted')
    list_filter = ('questions', 'forms', 'order_num', 'is_deleted')


class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted')
    search_fields = ('name', 'is_deleted')
    list_editable = ('name', 'is_deleted')
    list_filter = ('name', 'is_deleted')


class Forms_RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_value', 'answers', 'forms', 'form_sections', 'recommendations', 'is_deleted')
    search_fields = ('answers', 'forms', 'form_sections', 'recommendations', 'is_deleted')
    list_editable = ('free_value', 'answers', 'forms', 'form_sections', 'recommendations', 'is_deleted')
    list_filter = ('answers', 'forms', 'form_sections', 'recommendations', 'is_deleted')


class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_value', 'organisations', 'quota', 'forms', 'questions', 'question_values', 'is_deleted')
    search_fields = ('organisations', 'quota', 'forms', 'questions', 'question_values', 'is_deleted')
    list_editable = ('free_value', 'organisations', 'quota', 'forms', 'questions', 'question_values', 'is_deleted')
    list_filter = ('organisations', 'quota', 'forms', 'questions', 'question_values', 'is_deleted')


class Signed_DociumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'originat_file_name', 'description', 'created_at', 'forms', 'evaluation', 'is_deleted')
    search_fields = ('file_name', 'originat_file_name', 'created_at', 'forms', 'evaluation', 'is_deleted')
    list_editable = ('file_name', 'originat_file_name', 'description', 'created_at', 'forms', 'evaluation', 'is_deleted')
    list_filter = ('file_name', 'originat_file_name', 'created_at', 'forms', 'evaluation', 'is_deleted')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_value', 'forms', 'is_deleted')
    search_fields = ('free_value', 'forms', 'is_deleted')
    list_editable = ('free_value', 'forms', 'is_deleted')
    list_filter = ('free_value', 'forms', 'is_deleted')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'original_file_name', 'description', 'created_at', 'forms', 'evaluation', 'is_deleted')
    search_fields = ('file_name', 'original_file_name', 'created_at', 'forms', 'evaluation', 'is_deleted')
    list_editable = ('file_name', 'original_file_name', 'description', 'created_at', 'forms', 'evaluation', 'is_deleted')
    list_filter = ('file_name', 'original_file_name', 'created_at', 'forms', 'evaluation', 'is_deleted')


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_evaluation', 'forms', 'organisations', 'organisation_persons', 'is_deleted')
    search_fields = ('date_evaluation', 'forms', 'organisations', 'organisation_persons', 'is_deleted')
    list_editable = ('date_evaluation', 'forms', 'organisations', 'organisation_persons', 'is_deleted')
    list_filter = ('date_evaluation', 'forms', 'organisations', 'organisation_persons', 'is_deleted')


class VersionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_name', 'version', 'active', 'is_deleted')
    search_fields = ('table_name', 'version', 'active', 'is_deleted')
    list_editable = ('table_name', 'version', 'active', 'is_deleted')
    list_filter = ('table_name', 'version', 'active', 'is_deleted')


class Type_AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type',)
    list_editable = ('type',)
    list_filter = ('type',)


admin.site.register(Regions, RegionAdmin)            #!!!Важно соблюдать последовательность регистрации моделей
admin.site.register(Type_Departments, Type_DepartmentsAdmin)
admin.site.register(Departments, DepartmentAdmin)
admin.site.register(Department_Persons, Department_PersonsAdmin)
admin.site.register(Type_Organisations, Type_OrganisationsAdmin)
admin.site.register(Organisations, OrganisationsAdmin)
admin.site.register(Organisation_Persons, Organisation_PersonsAdmin)
admin.site.register(Quota, QuotaAdmin)
admin.site.register(Templates, TemplatesAdmin)
admin.site.register(Forms, FormsAdmin)
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
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Versions, VersionsAdmin)
admin.site.register(Type_Answers, Type_AnswersAdmin)

