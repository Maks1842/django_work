import re
import json

from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerAndAdminOrReadOnly
from django.http import Http404, HttpResponse
from .serializers import *
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import JSONRenderer
from drf_yasg2.utils import swagger_auto_schema, unset

"""ОГРАНИЧЕНИЯ ДОСТУПА:
Дефолтные permissions:
AllowAny - полный доступ;
IsAdminUser - только для Администраторов;
IsAuthenticated - только для авторизованных пользователей;
IsAuthenticatedOrReadOnly - только для авторизованных или всем, но для чтения.

Кастомные permissions:
IsAdminOrReadOnly - запись может просматривать любой, а удалять только Администратор;
IsOwnerAndAdminOrReadOnly - запись может менять только пользователь который её создал и Админ, просматривать может любой.
"""


######## v1 - один класс для всего () ##########
class RegionsViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    queryset = Regions.objects.all()
    serializer_class = RegionsSerializer

    # Отключаю отображение всех методов из Swagger
    swagger_schema = None

    # Отключение метода Destroy
    def _allowed_methods(self):
        return [m for m in super(RegionsViewSet, self)._allowed_methods() if m not in ['DELETE']]

    # Отключаю отображение метода из Swagger
    # @swagger_auto_schema(auto_schema=None)

    # detail=True возвращает только одну запись, detail=False - возвращает несколько записей
    @action(methods=['get'], detail=True)
    def region_id(self, request, pk=None):
        reg_id = Regions.objects.values('id').get(pk=pk)
        return Response({'region_id': reg_id})

    # Извлекаю одну запись из конкретного поля
    # @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def region_name(self, request, pk=None):
        reg_name = Regions.objects.values('region_name').get(pk=pk)
        return Response({'region_name': reg_name})

    # Изменяю одну запись в конкретном поле
    # @swagger_auto_schema(auto_schema=None)
    @action(methods=['put'], detail=True)
    def regions_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Regions.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = RegionsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class TypeDepartmentsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):

    queryset = Type_Departments.objects.all()
    serializer_class = Type_DepartmentsSerializer

    # swagger_schema = None

    @action(methods=['get'], detail=True)
    def type_departments_id(self, request, pk=None):
        type_dep_id = Type_Departments.objects.values('id').get(pk=pk)
        return Response({'type_dep_id': type_dep_id})

    @action(methods=['get'], detail=True)
    def type_departments_name(self, request, pk=None):
        type_dep_name = Type_Departments.objects.values('type').get(pk=pk)
        return Response({'type_dep_name': type_dep_name})

    @action(methods=['put'], detail=True)
    def type_departments_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Type_Departments.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Type_DepartmentsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class DepartmentsViewSet(
                         # mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         # mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):

    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer
    permission_classes = (IsOwnerAndAdminOrReadOnly,)

    # swagger_schema = None

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def departments_id(self, request, pk=None):
        dep_id = Departments.objects.values('id').get(pk=pk)
        return Response({'departments_id': dep_id})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def department_name(self, request, pk=None):
        dep_name = Departments.objects.values('department_name').get(pk=pk)
        return Response({'department_name': dep_name})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def parent(self, request, pk=None):
        parent_dep = Departments.objects.get(pk=pk)
        return Response({'parent_dep': parent_dep.department_name})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=False)
    def parents(self, request):
        parents_dep = Departments.objects.all()
        return Response({'parents_dep': [p.department_name for p in parents_dep]})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def region(self, request, pk=None):
        reg = Regions.objects.get(pk=pk)
        return Response({'region': reg.region_name})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=False)
    def regions(self, request):
        regs = Regions.objects.all()
        return Response({'regions': [r.region_name for r in regs]})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=True)
    def type_department(self, request, pk=None):
        type_dep = Type_Departments.objects.get(pk=pk)
        return Response({'type_department': type_dep.type})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=False)
    def types_departments(self, request):
        types_deps = Type_Departments.objects.all()
        return Response({'types_departments': [t.type for t in types_deps]})

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['put'], detail=True)
    # @permission_classes([IsAdminUser, IsOwnerOrReadOnly])
    def departments_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Departments.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = DepartmentsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class DepartmentPersonsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):

    queryset = Department_Persons.objects.all()
    serializer_class = Department_PersonsSerializer

    swagger_schema = None

    def _allowed_methods(self):
        return [m for m in super(DepartmentPersonsViewSet, self)._allowed_methods() if m not in ['DELETE']]

    @action(methods=['get'], detail=True)
    def department(self, request, pk=None):
        dep = Departments.objects.get(pk=pk)
        return Response({'department': dep.department_name})

    @action(methods=['get'], detail=False)
    def departments(self, request):
        deps = Departments.objects.all()
        return Response({'departments': [d.department_name for d in deps]})

    @action(methods=['put'], detail=True)
    def department_persons_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Department_Persons.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Department_PersonsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class TypeOrganisationsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Type_Organisations.objects.all()
    serializer_class = Type_OrganisationsSerializer

    swagger_schema = None

    def _allowed_methods(self):
        return [m for m in super(TypeOrganisationsViewSet, self)._allowed_methods() if m not in ['DELETE']]

    @action(methods=['get'], detail=True)
    def type_organisations_id(self, request, pk=None):
        type_orgs_id = Type_Organisations.objects.values('id').get(pk=pk)
        return Response({'type_organisations_id': type_orgs_id})

    @action(methods=['get'], detail=True)
    def type_organisations_name(self, request, pk=None):
        type_orgs_name = Type_Organisations.objects.values('type').get(pk=pk)
        return Response({'type_organisations_name': type_orgs_name})

    @action(methods=['put'], detail=True)
    def type_organisations_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Type_Organisations.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Type_OrganisationsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class OrganisationsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Organisations.objects.all()
    serializer_class = OrganisationsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def organisations_id(self, request, pk=None):
        orgs_id = Organisations.objects.values('id').get(pk=pk)
        return Response({'organisations_id': orgs_id})

    @action(methods=['get'], detail=True)
    def organisation_name(self, request, pk=None):
        org_name = Organisations.objects.values('organisation_name').get(pk=pk)
        return Response({'organisation_name': org_name})

    @action(methods=['get'], detail=True)
    def parent(self, request, pk=None):
        parent_org = Organisations.objects.get(pk=pk)
        return Response({'parent': parent_org.organisation_name})

    @action(methods=['get'], detail=False)
    def parents(self, request):
        parents_org = Organisations.objects.all()
        return Response({'parents': [p.organisation_name for p in parents_org]})

    @action(methods=['get'], detail=True)
    def department(self, request, pk=None):
        dep = Departments.objects.get(pk=pk)
        return Response({'region': dep.region_name})

    @action(methods=['get'], detail=False)
    def departments(self, request):
        deps = Departments.objects.all()
        return Response({'regions': [d.department_name for d in deps]})

    @action(methods=['get'], detail=True)
    def type_organisation(self, request, pk=None):
        type_org = Type_Organisations.objects.get(pk=pk)
        return Response({'type_organisation': type_org.type})

    @action(methods=['get'], detail=False)
    def types_organisations(self, request):
        types_orgs = Type_Organisations.objects.all()
        return Response({'types_organisations': [t.type for t in types_orgs]})

    @action(methods=['get'], detail=True)
    def quota(self, request, pk=None):
        quota_org = Quota.objects.get(pk=pk)
        return Response({'quota': quota_org.quota})

    @action(methods=['put'], detail=True)
    def organisations_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Organisations.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = OrganisationsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class OrganisationPersonsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):

    queryset = Organisation_Persons.objects.all()
    serializer_class = Organisation_PersonsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def organisation(self, request, pk=None):
        org = Organisations.objects.get(pk=pk)
        return Response({'organisation': org.organisation_name})

    @action(methods=['get'], detail=False)
    def organisations(self, request):
        orgs = Organisations.objects.all()
        return Response({'organisations': [o.organisation_name for o in orgs]})

    @action(methods=['put'], detail=True)
    def organisation_persons_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Organisation_Persons.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Organisation_PersonsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class QuotaViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer

    swagger_schema = None

    # swagger_schema = None

    @action(methods=['get'], detail=True)
    def quota_id(self, request, pk=None):
        quot_id = Quota.objects.values('id').get(pk=pk)
        return Response({'quota_id': quot_id})

    @action(methods=['get'], detail=True)
    def quota(self, request, pk=None):
        quot = Quota.objects.values('quota').get(pk=pk)
        return Response({'quota': quot})

    # @swagger_auto_schema(method='delete', swagger_schema=None)
    @action(methods=['put'], detail=True)
    def quota_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Quota.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = QuotaSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class TemplatesViewSet(
                        # mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        # mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Templates.objects.all()
    serializer_class = TemplatesSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def templates_id(self, request, pk=None):
        temp_id = Templates.objects.values('id').get(pk=pk)
        return Response({'templates_id': temp_id})

    @action(methods=['get'], detail=True)
    def name(self, request, pk=None):
        temp_name = Templates.objects.values('name').get(pk=pk)
        return Response({'name': temp_name})

    @action(methods=['put'], detail=True)
    def templates_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Templates.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = TemplatesSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class FormsViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def forms_id(self, request, pk=None):
        form_id = Forms.objects.values('id').get(pk=pk)
        return Response({'forms_id': form_id})

    @action(methods=['get'], detail=True)
    def created_at(self, request, pk=None):
        created = Forms.objects.values('created_at').get(pk=pk)
        return Response({'created': created})

    @action(methods=['get'], detail=True)
    def type_department(self, request, pk=None):
        type_dep = Type_Departments.objects.get(pk=pk)
        return Response({'type_department': type_dep.type})

    @action(methods=['get'], detail=False)
    def types_departments(self, request):
        types_deps = Type_Departments.objects.all()
        return Response({'types_departments': [t.type for t in types_deps]})

    @action(methods=['get'], detail=True)
    def template(self, request, pk=None):
        temp = Templates.objects.get(pk=pk)
        return Response({'template': temp.name})

    @action(methods=['get'], detail=False)
    def templates(self, request):
        temps = Templates.objects.all()
        return Response({'templates': [t.name for t in temps]})

    @action(methods=['put'], detail=True)
    def forms_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Forms.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = FormsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class FormSectionsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Form_Sections.objects.all()
    serializer_class = Form_SectionsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def form_sections_id(self, request, pk=None):
        form_sect_id = Form_Sections.objects.values('id').get(pk=pk)
        return Response({'form_sections_id': form_sect_id})

    @action(methods=['get'], detail=True)
    def form_sections_name(self, request, pk=None):
        name = Form_Sections.objects.values('name').get(pk=pk)
        return Response({'name': name})

    @action(methods=['get'], detail=True)
    def order_num(self, request, pk=None):
        ord_num = Form_Sections.objects.values('order_num').get(pk=pk)
        return Response({'order_num': ord_num})

    @action(methods=['get'], detail=True)
    def parent(self, request, pk=None):
        parent_fs = Form_Sections.objects.get(pk=pk)
        return Response({'parent': parent_fs.name})

    @action(methods=['get'], detail=False)
    def parents(self, request):
        parents_fs = Form_Sections.objects.all()
        return Response({'parents': [p.name for p in parents_fs]})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_fs = Forms.objects.get(pk=pk)
        return Response({'form': form_fs.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_fs = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_fs]})

    @action(methods=['get'], detail=True)
    def type_department(self, request, pk=None):
        type_dep = Type_Departments.objects.get(pk=pk)
        return Response({'type_department': type_dep.type})

    @action(methods=['get'], detail=False)
    def types_departments(self, request):
        types_deps = Type_Departments.objects.all()
        return Response({'types_departments': [t.type for t in types_deps]})

    @action(methods=['put'], detail=True)
    def form_sections_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Form_Sections.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Form_SectionsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class QuestionsViewSet(
                        # mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        # mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def questions_id(self, request, pk=None):
        quest_id = Questions.objects.values('id').get(pk=pk)
        return Response({'questions_id': quest_id})

    @action(methods=['get'], detail=True)
    def questions_name(self, request, pk=None):
        name = Questions.objects.values('name').get(pk=pk)
        return Response({'name': name})

    @action(methods=['get'], detail=True)
    def form_section(self, request, pk=None):
        form_sect = Form_Sections.objects.get(pk=pk)
        return Response({'form_section': form_sect.name})

    @action(methods=['get'], detail=False)
    def type_answers(self, request):
        type_anss = Form_Sections.objects.all()
        return Response({'type_answers': [t.type for t in type_anss]})

    @action(methods=['get'], detail=True)
    def type_answer(self, request, pk=None):
        type_ans = Type_Answers.objects.get(pk=pk)
        return Response({'type_answer': type_ans.type})

    @action(methods=['get'], detail=False)
    def form_sections(self, request):
        form_sects = Type_Answers.objects.all()
        return Response({'form_sections': [f.name for f in form_sects]})

    @action(methods=['put'], detail=True)
    def questions_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Questions.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = QuestionsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class QuestionValuesViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Question_Values.objects.all()
    serializer_class = Question_ValuesSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def question_values_id(self, request, pk=None):
        quest_id = Question_Values.objects.values('id').get(pk=pk)
        return Response({'question_values_id': quest_id})

    @action(methods=['get'], detail=True)
    def question_values_name(self, request, pk=None):
        name = Question_Values.objects.values('value_name').get(pk=pk)
        return Response({'value_name': name})

    @action(methods=['put'], detail=True)
    def question_values_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Question_Values.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Question_ValuesSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class FormSectionsQuestionViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Form_Sections_Question.objects.all()
    serializer_class = Form_Sections_QuestionSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def form_sections_question_id(self, request, pk=None):
        fsq_id = Form_Sections_Question.objects.values('id').get(pk=pk)
        return Response({'fsq_id': fsq_id})

    @action(methods=['get'], detail=True)
    def order_num(self, request, pk=None):
        num = Form_Sections_Question.objects.values('order_num').get(pk=pk)
        return Response({'order_num': num})

    @action(methods=['get'], detail=True)
    def question(self, request, pk=None):
        quest = Questions.objects.get(pk=pk)
        return Response({'name': quest.name})

    @action(methods=['get'], detail=False)
    def questions(self, request):
        quests = Questions.objects.all()
        return Response({'names': [q.name for q in quests]})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_fs = Forms.objects.get(pk=pk)
        return Response({'form': form_fs.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_fs = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_fs]})

    @action(methods=['put'], detail=True)
    def form_sections_question_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Form_Sections_Question.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Form_Sections_QuestionSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class RecommendationsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def recommendations_id(self, request, pk=None):
        rec_id = Recommendations.objects.values('id').get(pk=pk)
        return Response({'recommendations_id': rec_id})

    @action(methods=['get'], detail=True)
    def recommendations_name(self, request, pk=None):
        name = Recommendations.objects.values('name').get(pk=pk)
        return Response({'name': name})

    @action(methods=['put'], detail=True)
    def recommendations_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Recommendations.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = RecommendationsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class FormsRecommendationsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Forms_Recommendations.objects.all()
    serializer_class = Forms_RecommendationsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def forms_recommendations_id(self, request, pk=None):
        fr_id = Forms_Recommendations.objects.values('id').get(pk=pk)
        return Response({'forms_recommendations_id': fr_id})

    @action(methods=['get'], detail=True)
    def free_value(self, request, pk=None):
        fv = Forms_Recommendations.objects.values('free_value').get(pk=pk)
        return Response({'free_value': fv})

    @action(methods=['get'], detail=True)
    def answer(self, request, pk=None):
        ans = Answers.objects.get(pk=pk)
        return Response({'name': ans.id})

    @action(methods=['get'], detail=False)
    def answers(self, request):
        anss = Answers.objects.all()
        return Response({'names': [a.id for a in anss]})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_fs = Forms.objects.get(pk=pk)
        return Response({'form': form_fs.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_fs = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_fs]})

    @action(methods=['get'], detail=True)
    def form_section(self, request, pk=None):
        form_sect = Form_Sections.objects.get(pk=pk)
        return Response({'form_section': form_sect.name})

    @action(methods=['get'], detail=False)
    def form_sections(self, request):
        form_sects = Form_Sections.objects.all()
        return Response({'form_sections': [f.name for f in form_sects]})

    @action(methods=['get'], detail=True)
    def recommendation(self, request, pk=None):
        rec = Recommendations.objects.get(pk=pk)
        return Response({'recommendation': rec.name})

    @action(methods=['get'], detail=False)
    def recommendations(self, request):
        recs = Recommendations.objects.all()
        return Response({'recommendations': [r.name for r in recs]})

    @action(methods=['put'], detail=True)
    def forms_recommendations_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Forms_Recommendations.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Forms_RecommendationsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class AnswersViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def answers_id(self, request, pk=None):
        ans_id = Answers.objects.values('id').get(pk=pk)
        return Response({'answers_id': ans_id})

    @action(methods=['get'], detail=True)
    def free_value(self, request, pk=None):
        fv = Answers.objects.values('free_value').get(pk=pk)
        return Response({'free_value': fv})

    @action(methods=['get'], detail=True)
    def organisation(self, request, pk=None):
        org = Organisations.objects.get(pk=pk)
        return Response({'organisation': org.organisation_name})

    @action(methods=['get'], detail=False)
    def organisations(self, request):
        orgs = Organisations.objects.all()
        return Response({'organisations': [o.organisation_name for o in orgs]})

    @action(methods=['get'], detail=True)
    def quota(self, request, pk=None):
        quot = Quota.objects.get(pk=pk)
        return Response({'quota': quot.quota})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_fs = Forms.objects.get(pk=pk)
        return Response({'form': form_fs.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_fs = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_fs]})

    @action(methods=['get'], detail=True)
    def question(self, request, pk=None):
        quest = Questions.objects.get(pk=pk)
        return Response({'name': quest.name})

    @action(methods=['get'], detail=False)
    def questions(self, request):
        quests = Questions.objects.all()
        return Response({'names': [q.name for q in quests]})

    @action(methods=['get'], detail=True)
    def question_value(self, request, pk=None):
        qv = Question_Values.objects.get(pk=pk)
        return Response({'question_value': qv.value_name})

    @action(methods=['get'], detail=False)
    def question_values(self, request):
        qvs = Question_Values.objects.all()
        return Response({'question_values': [f.value_name for f in qvs]})

    @action(methods=['put'], detail=True)
    def answers_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Answers.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = AnswersSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class SignedDociumentsViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):

    queryset = Signed_Dociuments.objects.all()
    serializer_class = Signed_DociumentsSerializer
    # permission_classes = (IsOwnerAndAdminOrReadOnly,)

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def signed_dociuments_id(self, request, pk=None):
        sd_id = Signed_Dociuments.objects.values('id').get(pk=pk)
        return Response({'signed_dociuments_id': sd_id})

    @action(methods=['get'], detail=True)
    def file_name(self, request, pk=None):
        fn = Signed_Dociuments.objects.values('file_name').get(pk=pk)
        return Response({'file_name': fn})

    @action(methods=['get'], detail=True)
    def originat_file_name(self, request, pk=None):
        ofn = Signed_Dociuments.objects.values('originat_file_name').get(pk=pk)
        return Response({'originat_file_name': ofn})

    @action(methods=['get'], detail=True)
    def description(self, request, pk=None):
        descr = Signed_Dociuments.objects.values('description').get(pk=pk)
        return Response({'description': descr})

    @action(methods=['get'], detail=True)
    def created_at(self, request, pk=None):
        created = Signed_Dociuments.objects.values('created_at').get(pk=pk)
        return Response({'created': created})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_sd = Forms.objects.get(pk=pk)
        return Response({'form': form_sd.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_sd = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_sd]})

    @action(methods=['get'], detail=True)
    def evaluation(self, request, pk=None):
        evaluat = Evaluation.objects.get(pk=pk)
        return Response({'name': evaluat.date_evaluation})

    @action(methods=['get'], detail=False)
    def evaluations(self, request):
        evaluats = Evaluation.objects.all()
        return Response({'names': [e.date_evaluation for e in evaluats]})

    @action(methods=['put'], detail=True)
    def signed_dociuments_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Signed_Dociuments.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Signed_DociumentsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class CommentsViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def comments_id(self, request, pk=None):
        comment_id = Comments.objects.values('id').get(pk=pk)
        return Response({'comments_id': comment_id})

    @action(methods=['get'], detail=True)
    def free_value(self, request, pk=None):
        fv = Comments.objects.values('free_value').get(pk=pk)
        return Response({'free_value': fv})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_fs = Forms.objects.get(pk=pk)
        return Response({'form': form_fs.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_fs = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_fs]})

    @action(methods=['put'], detail=True)
    def comments_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Comments.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = CommentsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class PhotoViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # permission_classes = (IsOwnerAndAdminOrReadOnly,)

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def photo_id(self, request, pk=None):
        pht_id = Photo.objects.values('id').get(pk=pk)
        return Response({'photo_id': pht_id})

    @action(methods=['get'], detail=True)
    def file_name(self, request, pk=None):
        fn = Photo.objects.values('file_name').get(pk=pk)
        return Response({'file_name': fn})

    @action(methods=['get'], detail=True)
    def original_file_name(self, request, pk=None):
        ofn = Photo.objects.values('original_file_name').get(pk=pk)
        return Response({'original_file_name': ofn})

    @action(methods=['get'], detail=True)
    def description(self, request, pk=None):
        descr = Photo.objects.values('description').get(pk=pk)
        return Response({'description': descr})

    @action(methods=['get'], detail=True)
    def created_at(self, request, pk=None):
        created = Photo.objects.values('created_at').get(pk=pk)
        return Response({'created': created})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_sd = Forms.objects.get(pk=pk)
        return Response({'form': form_sd.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_sd = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_sd]})

    @action(methods=['get'], detail=True)
    def evaluation(self, request, pk=None):
        evaluat = Evaluation.objects.get(pk=pk)
        return Response({'name': evaluat.date_evaluation})

    @action(methods=['get'], detail=False)
    def evaluations(self, request):
        evaluats = Evaluation.objects.all()
        return Response({'names': [e.date_evaluation for e in evaluats]})

    @action(methods=['put'], detail=True)
    def photo_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Photo.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = PhotoSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class EvaluationViewSet(
                        # mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        # mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def evaluation_id(self, request, pk=None):
        evaluat_id = Evaluation.objects.values('id').get(pk=pk)
        return Response({'evaluation_id': evaluat_id})

    @action(methods=['get'], detail=True)
    def date_evaluation(self, request, pk=None):
        date = Evaluation.objects.values('date_evaluation').get(pk=pk)
        return Response({'date_evaluation': date})

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        form_sd = Forms.objects.get(pk=pk)
        return Response({'form': form_sd.name})

    @action(methods=['get'], detail=False)
    def forms(self, request):
        forms_sd = Forms.objects.all()
        return Response({'forms': [f.name for f in forms_sd]})

    @action(methods=['get'], detail=True)
    def organisation(self, request, pk=None):
        org = Organisations.objects.get(pk=pk)
        return Response({'organisation': org.organisation_name})

    @action(methods=['get'], detail=False)
    def organisations(self, request):
        orgs = Organisations.objects.all()
        return Response({'organisations': [o.organisation_name for o in orgs]})

    @action(methods=['get'], detail=True)
    def organisation_person(self, request, pk=None):
        org_pers = Organisation_Persons.objects.get(pk=pk)
        return Response({'organisation_person': org_pers.id})

    @action(methods=['get'], detail=False)
    def organisation_persons(self, request):
        orgs_pers = Organisation_Persons.objects.all()
        return Response({'organisation_persons': [o.id for o in orgs_pers]})

    @action(methods=['put'], detail=True)
    def evaluation_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Evaluation.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = EvaluationSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class VersionsViewSet(
                        # mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        # mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Versions.objects.all()
    serializer_class = VersionsSerializer

    swagger_schema = None

    @action(methods=['get'], detail=True)
    def versions_id(self, request, pk=None):
        vers_id = Versions.objects.values('id').get(pk=pk)
        return Response({'versions_id': vers_id})

    @action(methods=['get'], detail=True)
    def table_name(self, request, pk=None):
        name = Versions.objects.values('table_name').get(pk=pk)
        return Response({'table_name': name})

    @action(methods=['get'], detail=True)
    def version(self, request, pk=None):
        vers = Versions.objects.values('version').get(pk=pk)
        return Response({'version': vers})

    @action(methods=['put'], detail=True)
    def versions_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Versions.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = VersionsSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class TypeAnswersViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):  # Данный класс включает методы GET, POST, PUT, DELETE
    queryset = Type_Answers.objects.all()
    serializer_class = Type_AnswersSerializer

    swagger_schema = None

    # def _allowed_methods(self):
    #     return [m for m in super(TypeAnswersViewSet, self)._allowed_methods() if m not in ['DELETE']]

    @action(methods=['get'],
            detail=True)  # detail=True возвращает только одну запись, detail=False - возвращает несколько записей
    def type_answers_id(self, request, pk=None):
        type_ans_id = Type_Answers.objects.values('id').get(pk=pk)
        return Response({'type_id': type_ans_id})

    @action(methods=['get'], detail=True)  # Извлекаю одну запись из конкретного поля
    def type_answers(self, request, pk=None):
        type = Type_Answers.objects.values('type').get(pk=pk)
        return Response({'type': type})

    @action(methods=['put'], detail=True)  # Изменяю одну запись в конкретном поле
    def type_answers_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Type_Answers.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Type_AnswersSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class TransactionExchangeViewSet(
                            # mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Transaction_Exchange.objects.all()
    serializer_class = Transaction_ExchangeSerializer

    swagger_schema = None

    @action(methods=['put'], detail=True)
    def transaction_exchange_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Метод PUT не определен'})
        try:
            instance = Transaction_Exchange.objects.get(pk=pk)
        except:
            return Response({'error': 'Объект не существует'})
        serializers = Transaction_ExchangeSerializer(data=request.data, instance=instance, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'post': serializers.data})


class ListForCheckViewSet(
                    # mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = ListForCheck.objects.all()
    serializer_class = ListForCheckSerializer

    # swagger_schema = None

    # def _allowed_methods(self):
    #     return [m for m in super(TypeAnswersViewSet, self)._allowed_methods() if m not in ['DELETE']]


class FormsActViewSet(
                # mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                # mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = FormsAct.objects.all()
    serializer_class = FormsActSerializer

    # swagger_schema = None

    # def _allowed_methods(self):
    #     return [m for m in super(TypeAnswersViewSet, self)._allowed_methods() if m not in ['DELETE']]


"""
Предоставление API для данных из БД.
1. Проверяю, какому типу департамента принадлежит раздел Анкеты:
    - раздел может быть одинаковый для разных департаментов, если type_departments=None, значит подходит ко всем.
2. Передаю два позиционных аргумента, для выбора необходимых вопросов Акта, для конкретных типов оргрнизаций:
    - type_departments=1 ---> 1 - это id модели Type_Departments;
    - type_organisations='2|3' ---> '2|3' - это id модели Type_Organisations.
"""


class GetActAPIView(APIView):

    def get(self, request, type_departments=3, type_organisations='9'):

        context = []
        count = 0

        form_sections = Form_Sections.objects.values().filter(type_departments=type_departments) | Form_Sections.objects.values().filter(type_departments=None)
        questions = Questions.objects.values()
        type_answers = Type_Answers.objects.values()
        question_values = Question_Values.objects.values()

        for fs in form_sections:
            fs_id = fs['id']
            questions_id = questions.filter(form_sections_id=fs_id)
            count_section = 0
            pages = []

            for q in questions_id:
                choices = []
                count_section += 1

                if re.findall(type_organisations, str(q['type_organisations'])) or q['type_organisations'] is None:
                    count += 1
                    type = type_answers.get(pk=q['type_answers_id'])
                    answer_variant = q['answer_variant']
                    ans_var_re = answer_variant
                    try:
                        ans_var_re = (re.sub(r'\s', '', answer_variant))
                    except:
                        pass

                    ans_var = ans_var_re.split(',')

                    for av in range(len(ans_var)):
                        qv = question_values.get(pk=ans_var[av])
                        choices.append({'value': ans_var[av], 'text': qv['value_name']})


                    pages.append({
                        'name': str(count),
                        'title': q['name'],
                        'type': type['type'],
                        'choices': choices,
                        'isRequired': 'true',
                        # 'test': len(questions_id),
                        # 'test2': count_section
                    })

                if len(pages) == 4 or len(questions_id) == count_section:
                    context.append({
                        'title': fs['name'],
                        'elements': pages,
                    })
                    pages = []
        return Response({'pages': context})
