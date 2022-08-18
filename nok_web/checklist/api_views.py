from .models import *
from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


######## v1 - один класс для всего () ##########
class RegionsViewSet(viewsets.ModelViewSet):
    queryset = Regions.objects.all()
    serializer_class = RegionsSerializer


class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer



# ######## v2 - для каждой задачи отдельный класс ##########
# class RegionsAPIList(generics.ListCreateAPIView):           # Для GET и POST запросов
#     queryset = Regions.objects.all()
#     serializer_class = RegionsSerializer
#
#
# class RegionsAPIUpdate(generics.UpdateAPIView):             # Для изменения данных
#     queryset = Regions.objects.all()
#     serializer_class = RegionsSerializer
#
#
# class RegionsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):       # Чтение, удаление, добавление отдельной записи
#     queryset = Regions.objects.all()
#     serializer_class = RegionsSerializer
#
# ######## v3 - учебный ##########
# class RegionsAPIView(APIView):
#
#     # def get(self, request):
#     #     regions = Regions.objects.all().values()
#     #     return Response({'regions': regions})
#     #
#     # def post(self, request):                              #Для добавления данных
#     #     serializers = RegionsSerializer(data=request.data)
#     #     serializers.is_valid(raise_exception=True)
#     #     serializers.save()
#     #     return Response({'post': serializers.data})
#
#     def put(self, request, *args, **kwargs):              #Для изменения данных
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Метод PUT не определен'})
#
#         try:
#             instance = Regions.objects.get(pk=pk)
#         except:
#             return Response({'error': 'Объект не существует'})
#
#         serializers = RegionsSerializer(data=request.data, instance=instance)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({'post': serializers.data})
# ######## END v3 - учебный ##########







# class Type_DepartmentsAPIView(APIView):
#     serializer_class = serializers.Type_DepartmentsSerializer
#
#     def get_queryset(self):
#         return Type_Departments.objects.all()
#
#
# class DepartmentsAPIView(APIView):
#     serializer_class = serializers.DepartmentsSerializer
#
#     def get_queryset(self):
#         return Departments.objects.all()
#
#
#
# class Department_PersonsAPIView(APIView):
#     serializer_class = serializers.Department_PersonsSerializer
#
#     def get_queryset(self):
#         return Department_Persons.objects.all()
#
#
# class Type_OrganisationsAPIView(APIView):
#     serializer_class = serializers.Type_OrganisationsSerializer
#
#     def get_queryset(self):
#         return Type_Organisations.objects.all()
#
#
# class OrganisationsAPIView(APIView):
#     serializer_class = serializers.OrganisationsSerializer
#
#     def get_queryset(self):
#         return Organisations.objects.all()
#
#
# class Organisation_PersonsAPIView(APIView):
#     serializer_class = serializers.Organisation_PersonsSerializer
#
#     def get_queryset(self):
#         return Organisation_Persons.objects.all()
#
#
# class QuotaAPIView(APIView):
#     serializer_class = serializers.QuotaSerializer
#
#     def get_queryset(self):
#         return Quota.objects.all()
#
#
# class TemplatesAPIView(APIView):
#     serializer_class = serializers.TemplatesSerializer
#
#     def get_queryset(self):
#         return Templates.objects.all()
#
#
# class FormsAPIView(APIView):
#     serializer_class = serializers.FormsSerializer
#
#     def get_queryset(self):
#         return Forms.objects.all()
#
#
# class Form_SectionsAPIView(APIView):
#     serializer_class = serializers.Form_SectionsSerializer
#
#     def get_queryset(self):
#         return Form_Sections.objects.all()
#
#
# class QuestionsAPIView(APIView):
#     serializer_class = serializers.QuestionsSerializer
#
#     def get_queryset(self):
#         return Questions.objects.all()
#
#
# class Question_ValuesAPIView(APIView):
#     serializer_class = serializers.Question_ValuesSerializer
#
#     def get_queryset(self):
#         return Question_Values.objects.all()
#
#
# class Form_Sections_QuestionAPIView(APIView):
#     serializer_class = serializers.Form_Sections_QuestionSerializer
#
#     def get_queryset(self):
#         return Form_Sections_Question.objects.all()
#
#
# class RecommendationsAPIView(APIView):
#     serializer_class = serializers.RecommendationsSerializer
#
#     def get_queryset(self):
#         return Recommendations.objects.all()
#
#
# class Forms_RecommendationsAPIView(APIView):
#     serializer_class = serializers.Forms_RecommendationsSerializer
#
#     def get_queryset(self):
#         return Forms_Recommendations.objects.all()
#
#
# class AnswersAPIView(APIView):
#     serializer_class = serializers.AnswersSerializer
#
#     def get_queryset(self):
#         return Answers.objects.all()
#
#
# class Signed_DociumentsAPIView(APIView):
#     serializer_class = serializers.Signed_DociumentsSerializer
#
#     def get_queryset(self):
#         return Signed_Dociuments.objects.all()
#
#
# class EvaluationAPIView(APIView):
#     serializer_class = serializers.EvaluationSerializer
#
#     def get_queryset(self):
#         return Evaluation.objects.all()
#
#
# class VersionsAPIView(APIView):
#     serializer_class = serializers.VersionsSerializer
#
#     def get_queryset(self):
#         return Versions.objects.all()

