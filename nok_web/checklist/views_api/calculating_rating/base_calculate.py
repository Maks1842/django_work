from ...app_models import *
from ...app_serializers.answers_serializer import AnswersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser

from .school import school_rating



class CalculatingRatingAPIView(APIView):

    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        methods=['get'],
        tags=['Расчет баллов'],
        operation_description="Образование, баллы по результатам очного этапа",
        manual_parameters=[
            openapi.Parameter('id_checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_organisation', openapi.IN_QUERY, description="Идентификатор организации",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('id_type_organisation', openapi.IN_QUERY, description="Идентификатор типа организации",
                              type=openapi.TYPE_INTEGER),

        ])
    @action(methods=['get'], detail=False)
    def get(self, request):

        checking = request.query_params.get('id_checking')
        organisation = request.query_params.get('id_organisation')
        type_organisation = request.query_params.get('id_type_organisation')

        queryset = FormsAct.objects.filter(type_organisations_id=type_organisation)

        try:
            answer_set = Answers.objects.filter(checking_id=checking, type_organisations=type_organisation).get(organisations_id=organisation)
        except:
            return Response({'error': 'Не найдены данные о результатах запрашиваемой проверки.'})

        act_answer = answer_set.answers_json
        quota = answer_set.quota
        invalid_person = answer_set.invalid_person

        form_json = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json
        form_json_to_calculate = FormsAct.objects.get(type_organisations_id=queryset[0].type_organisations_id).act_json_to_calculate
        query = Question_Values.objects.values()

        comparison = do_some_magic(form_json, act_answer)
        answers = answer_in_the_act(comparison, query)

        if type_organisation == '1':
            rating = 100
        elif type_organisation == '2':
            rating = 100
        elif type_organisation == '3':
            rating = 100
        elif type_organisation == '4':
            rating = 100
        elif type_organisation == '5':
            rating = school_rating(quota, invalid_person, answers, form_json_to_calculate)
        elif type_organisation == '7':
            rating = 100
        elif type_organisation == '9':
            rating = 100
        elif type_organisation == '10':
            rating = 100

        return Response(rating)



'''
Функция сравнения двух json.
Производится сопоставление полученных ответов с имеющимся вопросами.
На выходе формируется новый json, где:
- если один из ответов совпадает с вопросом, то ячейки без совпадения остаются пустые, в ячейках с совпадением проставляется номер ответа;
- если нет ни одного совпадения, то все ячейки остаются пустые.
В формируемом json количество объектов в списке равно количеству объектов списка с вопросами.
'''

def do_some_magic(form_json, act_answer):
    act = form_json
    questions = {}
    for page in act['pages']:
        for element in page['elements']:
            choices = []
            for choice in element['choices']:
                choices.append(choice['value'])
            questions[element['name']] = choices

    tt = {}

    for question in act_answer:
        sh = []

        for answer in questions[question]:
            if answer in act_answer[question]:
                sh.append(answer)
            else:
                sh.append('')
        tt[question] = sh

    z = questions.copy()
    z.update(tt)
    for question in z:
        if question not in act_answer:
            for i in range(len(z[question])):
                z[question][i] = ''

    return z


'''
Функция формирования текстовых ответов для HTML шаблона из json файла,
который сформирован на основе сопоставления act_json и answer_json.
'''

def answer_in_the_act(comparison, query):
    list_dict = {}

    for answ in comparison:
        answer = []
        answers = []
        if '11' in comparison[answ] or '12' in comparison[answ]:
            for a in comparison[answ]:
                if a == '':
                    # answer = "0"
                    answer = {'value': '0', 'text': a}
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        # answer = "1"
                        answer = {'value': '1', 'text': a}
                    else:
                        # answer = query.get(pk=int(a))['value_name']
                        answer = {'value': query.get(pk=int(a))['value_name'], 'text': a}
                answers.append(answer)
        else:
            for a in comparison[answ]:
                if a == '':
                    # answer = "0"
                    answer = {'value': '0', 'text': a}
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        # answer = query.get(pk=int(a))['name_alternativ']
                        answer = {'value': query.get(pk=int(a))['name_alternativ'], 'text': a}
                    elif query.get(pk=int(a))['value_name'] == 'Да':
                        # answer = "1"
                        answer = {'value': '1', 'text': a}
                    elif query.get(pk=int(a))['value_name'] == 'Нет':
                        # answer = "0"
                        answer = {'value': '0', 'text': a}
                    else:
                        # answer = query.get(pk=int(a))['value_name']
                        answer = {'value': query.get(pk=int(a))['value_name'], 'text': a}
                answers.append(answer)
        list_dict[answ] = answers

    return list_dict