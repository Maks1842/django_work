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
    class Meta:
        model = Departments
        fields = ['id', 'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'is_deleted']


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
        fields = ['id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'organisation', 'is_deleted']


class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ['id', 'quota']


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = ['id', 'name', 'template_file', 'version', 'is_deleted']


class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['id', 'name', 'version', 'created_at', 'type_departments', 'templates', 'is_deleted']


class Form_SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Sections
        fields = ['id', 'name', 'version', 'order_num', 'parent', 'forms', 'type_departments', 'is_deleted']


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'name', 'form_sections', 'is_deleted']


class Question_ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_Values
        fields = ['id', 'value_name', 'questions']


class Form_Sections_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Sections_Question
        fields = ['id', 'questions', 'forms', 'order_num', 'is_deleted']


class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ['id', 'name', 'is_deleted']


class Forms_RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms_Recommendations
        fields = ['id', 'free_value', 'answers', 'forms', 'form_sections', 'recommendations', 'is_deleted']


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'free_value', 'organisations', 'quota', 'forms', 'questions', 'question_values', 'is_deleted']


class Signed_DociumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signed_Dociuments
        fields = ['id', 'file_name', 'originat_file_name', 'description', 'created_at', 'forms', 'evaluation', 'is_deleted']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'free_value', 'forms', 'is_deleted']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'file_name', 'original_file_name', 'description', 'created_at', 'forms', 'evaluation', 'is_deleted']


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'date_evaluation', 'forms', 'organisations', 'organisation_persons', 'is_deleted']


class VersionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versions
        fields = ['id', 'table_name', 'version', 'active', 'is_deleted']

