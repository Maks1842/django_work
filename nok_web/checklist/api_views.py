from .models import *
from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action


######## v1 - один класс для всего () ##########
class RegionsViewSet(viewsets.ModelViewSet):                            # Данный класс включает методы GET, POST, PUT, DELETE
    queryset = Regions.objects.all()
    serializer_class = RegionsSerializer

    @action(methods=['get'], detail=True)                              # detail=True возвращает только одну запись, detail=False - возвращает несколько записей
    def region_id(self, request, pk=None):
        reg_id = Regions.objects.values('id').get(pk=pk)
        return Response({'region_id': reg_id})

    @action(methods=['get'], detail=True)                              # Извлекаю одну запись из конкретного поля
    def region_name(self, request, pk=None):
        reg_name = Regions.objects.values('region_name').get(pk=pk)
        return Response({'region_name': reg_name})

    @action(methods=['put'], detail=True)                              # Изменяю одну запись в конкретном поле
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


class Type_DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Type_Departments.objects.all()
    serializer_class = Type_DepartmentsSerializer

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


class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer

    @action(methods=['get'], detail=True)
    def departments_id(self, request, pk=None):
        dep_id = Departments.objects.values('id').get(pk=pk)
        return Response({'departments_id': dep_id})

    @action(methods=['get'], detail=True)
    def department_name(self, request, pk=None):
        dep_name = Departments.objects.values('department_name').get(pk=pk)
        return Response({'department_name': dep_name})

    @action(methods=['get'], detail=True)
    def parent(self, request, pk=None):
        parent_dep = Departments.objects.get(pk=pk)
        return Response({'parent_dep': parent_dep.department_name})

    @action(methods=['get'], detail=False)
    def parents(self, request):
        parents_dep = Departments.objects.all()
        return Response({'parents_dep': [p.department_name for p in parents_dep]})

    @action(methods=['get'], detail=True)
    def region(self, request, pk=None):
        reg = Regions.objects.get(pk=pk)
        return Response({'region': reg.region_name})

    @action(methods=['get'], detail=False)
    def regions(self, request):
        regs = Regions.objects.all()
        return Response({'regions': [r.region_name for r in regs]})

    @action(methods=['get'], detail=True)
    def type_department(self, request, pk=None):
        type_dep = Type_Departments.objects.get(pk=pk)
        return Response({'type_department': type_dep.type})

    @action(methods=['get'], detail=False)
    def types_departments(self, request):
        types_deps = Type_Departments.objects.all()
        return Response({'types_departments': [t.type for t in types_deps]})

    @action(methods=['put'], detail=True)
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


class Department_PersonsViewSet(viewsets.ModelViewSet):
    queryset = Department_Persons.objects.all()
    serializer_class = Department_PersonsSerializer

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


class Type_OrganisationsViewSet(viewsets.ModelViewSet):
    queryset = Type_Organisations.objects.all()
    serializer_class = Type_OrganisationsSerializer

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


class OrganisationsViewSet(viewsets.ModelViewSet):
    queryset = Organisations.objects.all()
    serializer_class = OrganisationsSerializer

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


class Organisation_PersonsViewSet(viewsets.ModelViewSet):
    queryset = Organisation_Persons.objects.all()
    serializer_class = Organisation_PersonsSerializer

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


class QuotaViewSet(viewsets.ModelViewSet):                            # Данный класс включает методы GET, POST, PUT, DELETE
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer

    @action(methods=['get'], detail=True)                              # detail=True возвращает только одну запись, detail=False - возвращает несколько записей
    def quota_id(self, request, pk=None):
        quot_id = Quota.objects.values('id').get(pk=pk)
        return Response({'quota_id': quot_id})

    @action(methods=['get'], detail=True)                              # Извлекаю одну запись из конкретного поля
    def quota(self, request, pk=None):
        quot = Quota.objects.values('quota').get(pk=pk)
        return Response({'quota': quot})

    @action(methods=['put'], detail=True)                              # Изменяю одну запись в конкретном поле
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


class TemplatesViewSet(viewsets.ModelViewSet):
    queryset = Templates.objects.all()
    serializer_class = TemplatesSerializer

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


class FormsViewSet(viewsets.ModelViewSet):
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer

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


class Form_SectionsViewSet(viewsets.ModelViewSet):
    queryset = Form_Sections.objects.all()
    serializer_class = Form_SectionsSerializer

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


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

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
    def form_sections(self, request):
        form_sects = Form_Sections.objects.all()
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


class Question_ValuesViewSet(viewsets.ModelViewSet):
    queryset = Question_Values.objects.all()
    serializer_class = Question_ValuesSerializer

    @action(methods=['get'], detail=True)
    def question_values_id(self, request, pk=None):
        quest_id = Question_Values.objects.values('id').get(pk=pk)
        return Response({'question_values_id': quest_id})

    @action(methods=['get'], detail=True)
    def question_values_name(self, request, pk=None):
        name = Question_Values.objects.values('value_name').get(pk=pk)
        return Response({'value_name': name})

    @action(methods=['get'], detail=True)
    def question(self, request, pk=None):
        quest = Questions.objects.get(pk=pk)
        return Response({'name': quest.name})

    @action(methods=['get'], detail=False)
    def questions(self, request):
        quests = Questions.objects.all()
        return Response({'names': [q.name for q in quests]})

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


class Form_Sections_QuestionViewSet(viewsets.ModelViewSet):
    queryset = Form_Sections_Question.objects.all()
    serializer_class = Form_Sections_QuestionSerializer

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


class RecommendationsViewSet(viewsets.ModelViewSet):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerializer

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


class Forms_RecommendationsViewSet(viewsets.ModelViewSet):
    queryset = Forms_Recommendations.objects.all()
    serializer_class = Forms_RecommendationsSerializer

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


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer

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


class Signed_DociumentsViewSet(viewsets.ModelViewSet):
    queryset = Signed_Dociuments.objects.all()
    serializer_class = Signed_DociumentsSerializer

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


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

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


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

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


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

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


class VersionsViewSet(viewsets.ModelViewSet):
    queryset = Versions.objects.all()
    serializer_class = VersionsSerializer

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




######## v2 - учебный ##########
# class RegionsAPIView(APIView):
#
#     def get(self, request):
#         regions = Regions.objects.all().values()
#         return Response({'regions': regions})
#
#     def post(self, request):                              #Для добавления данных
#         serializers = RegionsSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({'post': serializers.data})
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






