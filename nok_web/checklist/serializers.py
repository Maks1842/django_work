from .models import *
from rest_framework import serializers


class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'region_name', 'is_deleted']


class Type_DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Departments
        fields = ['id', 'type', 'is_deleted']


class DepartmentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Departments
        fields = ['id', 'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'is_deleted', 'user']


class Department_PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_Persons
        fields = ['id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted']


class Type_OrganisationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Organisations
        fields = ['id', 'type', 'is_deleted']


class OrganisationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisations
        fields = ['id', 'organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota', 'type_organisations', 'is_deleted']


class Organisation_PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation_Persons
        fields = ['id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'is_deleted']


class Form_Organisation_PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Organisation_Persons
        fields = ['id', 'organisation', 'person']


class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ['id', 'quota']


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = ['id', 'name', 'type_organisations', 'template_file', 'version', 'is_deleted']


class Form_SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Sections
        fields = ['id', 'name', 'version', 'order_num', 'parent', 'type_departments', 'is_deleted']


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'questions']


class Question_ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_Values
        fields = ['id', 'value_name',  'name_alternativ']


class Form_Sections_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Sections_Question
        fields = ['id', 'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'is_deleted']


class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ['id', 'name', 'is_deleted']


class Forms_RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms_Recommendations
        fields = ['id', 'free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted']


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'organisations', 'checking', 'answers_json', 'is_deleted']


class Signed_DociumentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Signed_Dociuments
        fields = ['id', 'file_name', 'originat_file_name', 'description', 'created_at', 'is_deleted', 'user']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'free_value', 'is_deleted']


class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Photo
        fields = ['id', 'file_name', 'original_file_name', 'description', 'created_at', 'is_deleted', 'user']


class VersionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versions
        fields = ['id', 'table_name', 'version', 'active', 'is_deleted']


class Type_AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Answers
        fields = ['id', 'type']


class Transaction_ExchangeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Transaction_Exchange
        fields = ['id', 'model', 'field', 'old_data', 'new_data', 'date_exchange', 'user']


class FormsActSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsAct
        fields = ['id', 'type_departments', 'type_organisations', 'act_json', 'date', 'version']


class CheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checking
        fields = ['id', 'name', 'date_checking', 'region', 'department', 'is_deleted']


class ListCheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Checking
        fields = ['id', 'checking', 'organisation', 'user', 'is_deleted']




