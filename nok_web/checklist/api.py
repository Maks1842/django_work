from .models import *
from . import serializers
from rest_framework.generics import ListAPIView


class RegionsListAPIView(ListAPIView):
    serializer_class = serializers.RegionsSerializer

    def get_queryset(self):
        return Regions.objects.all()


class Type_DepartmentsListAPIView(ListAPIView):
    serializer_class = serializers.Type_DepartmentsSerializer

    def get_queryset(self):
        return Type_Departments.objects.all()


class DepartmentsListAPIView(ListAPIView):
    serializer_class = serializers.DepartmentsSerializer

    def get_queryset(self):
        return Departments.objects.all()


class Department_PersonsListAPIView(ListAPIView):
    serializer_class = serializers.Department_PersonsSerializer

    def get_queryset(self):
        return Department_Persons.objects.all()


class Type_OrganisationsListAPIView(ListAPIView):
    serializer_class = serializers.Type_OrganisationsSerializer

    def get_queryset(self):
        return Type_Organisations.objects.all()


class OrganisationsListAPIView(ListAPIView):
    serializer_class = serializers.OrganisationsSerializer

    def get_queryset(self):
        return Organisations.objects.all()


class Organisation_PersonsListAPIView(ListAPIView):
    serializer_class = serializers.Organisation_PersonsSerializer

    def get_queryset(self):
        return Organisation_Persons.objects.all()


class QuotaListAPIView(ListAPIView):
    serializer_class = serializers.QuotaSerializer

    def get_queryset(self):
        return Quota.objects.all()


class TemplatesListAPIView(ListAPIView):
    serializer_class = serializers.TemplatesSerializer

    def get_queryset(self):
        return Templates.objects.all()


class FormsListAPIView(ListAPIView):
    serializer_class = serializers.FormsSerializer

    def get_queryset(self):
        return Forms.objects.all()


class Form_SectionsListAPIView(ListAPIView):
    serializer_class = serializers.Form_SectionsSerializer

    def get_queryset(self):
        return Form_Sections.objects.all()


class QuestionsListAPIView(ListAPIView):
    serializer_class = serializers.QuestionsSerializer

    def get_queryset(self):
        return Questions.objects.all()


class Question_ValuesListAPIView(ListAPIView):
    serializer_class = serializers.Question_ValuesSerializer

    def get_queryset(self):
        return Question_Values.objects.all()


class Form_Sections_QuestionListAPIView(ListAPIView):
    serializer_class = serializers.Form_Sections_QuestionSerializer

    def get_queryset(self):
        return Form_Sections_Question.objects.all()


class RecommendationsListAPIView(ListAPIView):
    serializer_class = serializers.RecommendationsSerializer

    def get_queryset(self):
        return Recommendations.objects.all()


class Forms_RecommendationsListAPIView(ListAPIView):
    serializer_class = serializers.Forms_RecommendationsSerializer

    def get_queryset(self):
        return Forms_Recommendations.objects.all()


class AnswersListAPIView(ListAPIView):
    serializer_class = serializers.AnswersSerializer

    def get_queryset(self):
        return Answers.objects.all()


class Signed_DociumentsListAPIView(ListAPIView):
    serializer_class = serializers.Signed_DociumentsSerializer

    def get_queryset(self):
        return Signed_Dociuments.objects.all()


class EvaluationListAPIView(ListAPIView):
    serializer_class = serializers.EvaluationSerializer

    def get_queryset(self):
        return Evaluation.objects.all()


class VersionsListAPIView(ListAPIView):
    serializer_class = serializers.VersionsSerializer

    def get_queryset(self):
        return Versions.objects.all()

