import os

from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Font, NamedStyle, Side, Border, PatternFill, Alignment, GradientFill
from datetime import date

from ...app_models import *

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponse

'''
Добавление всех рейтингов, по проверке, в сводную таблицу Excel.
'''

class ExportRatingsToExcelAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        method='get',
        tags=['Рейтинг'],
        operation_description="Сводная таблица рейтингов в Excel",
        manual_parameters=[
            openapi.Parameter('checking', openapi.IN_QUERY, description="Идентификатор проверки",
                              type=openapi.TYPE_INTEGER)
        ])
    @action(detail=False, methods=['get'], )
    def get(self, request):
        checking_id = request.query_params.get('checking')

        if checking_id == None:
            return Response({'error': 'Данные о проверке не предоставлены'})

        ratings_set = Ratings.objects.values().filter(checking_id=checking_id)

        type_organisation_id = ratings_set[0]['type_organisations_id']

        result = ''
        match type_organisation_id:
            case (1 | 10):
                result = ratings_culture_to_excel(ratings_set)
            case (2 | 3):
                result = ratings_healthcare_to_excel(checking_id)
            case (4 | 5 | 7 | 9):
                result = ratings_education_to_excel(ratings_set)

        file_pointer = open(result, "rb")
        response = HttpResponse(file_pointer, content_type='application/vnd.openxmlformats-officedocument'
                                                           '.spreadsheetml.sheet;')
        response['Content-Disposition'] = f'attachment; filename=download.xlsx'
        response['Content-Transfer-Encoding'] = 'utf-8'
        os.remove(result)

        return response


def ratings_culture_to_excel(ratings_set):
    style = style_excel()

    book_template = load_workbook(filename='./checklist/templates/template_nok.xlsx')

    # Первый (активный) Лист книги
    sheet = book_template.active

    # Изменить имя Листа книги
    sheet.title = "Сводный рейтинг"

    number_col = 1
    for data in ratings_set:
        organisation = Organisations.objects.get(pk=data['organisations_id']).organisation_name

        number_col += 1

        try:
            rating_3_1_1 = data['rating_3_1_1']['value']
            rating_3_1_2 = data['rating_3_1_2']['value']
            rating_3_1_3 = data['rating_3_1_3']['value']
        except:
            rating_3_1_1 = ''
            rating_3_1_2 = ''
            rating_3_1_3 = ''

        # # Вставить один столбец перед №___
        # sheet.insert_cols(number_col)

        column = number_col

        # Преобразую индекс столбца в его буквенное обозначение: 1 = "А"
        letter = get_column_letter(column)

        # Высота строки
        sheet.row_dimensions[1].height = 60

        # Ширина столбца
        sheet.column_dimensions[letter].width = 35

        # Добавить данные в ячейку
        row = 1
        sheet.cell(row, column).value = organisation
        sheet.cell(row, column).style = style['style_main']

        row = 2
        sheet.cell(row, column).value = data['ratings_json']['rating_total']['value']
        sheet.cell(row, column).style = style['style_1']

        row = 3
        sheet.cell(row, column).value = data['ratings_json']['rating_1']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 4
        sheet.cell(row, column).value = data['ratings_json']['rating_1_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 5
        sheet.cell(row, column).value = data['ratings_json']['rating_1_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 6
        sheet.cell(row, column).value = data['ratings_json']['rating_1_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 7
        sheet.cell(row, column).value = data['ratings_json']['rating_2']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 8
        sheet.cell(row, column).value = data['ratings_json']['rating_2_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 9
        sheet.cell(row, column).value = data['ratings_json']['rating_2_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 10
        sheet.cell(row, column).value = data['ratings_json']['rating_3']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 11
        sheet.cell(row, column).value = data['ratings_json']['rating_3_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 12
        sheet.cell(row, column).value = rating_3_1_1
        sheet.cell(row, column).style = style['style_4']

        row = 13
        sheet.cell(row, column).value = rating_3_1_2
        sheet.cell(row, column).style = style['style_4']

        row = 14
        sheet.cell(row, column).value = rating_3_1_3
        sheet.cell(row, column).style = style['style_4']

        row = 15
        sheet.cell(row, column).value = data['ratings_json']['rating_3_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 16
        sheet.cell(row, column).value = data['ratings_json']['rating_3_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 17
        sheet.cell(row, column).value = data['ratings_json']['rating_4']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 18
        sheet.cell(row, column).value = data['ratings_json']['rating_4_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 19
        sheet.cell(row, column).value = data['ratings_json']['rating_4_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 20
        sheet.cell(row, column).value = data['ratings_json']['rating_4_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 21
        sheet.cell(row, column).value = data['ratings_json']['rating_5']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 22
        sheet.cell(row, column).value = data['ratings_json']['rating_5_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 23
        sheet.cell(row, column).value = data['ratings_json']['rating_5_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 24
        sheet.cell(row, column).value = data['ratings_json']['rating_5_3']['value']
        sheet.cell(row, column).style = style['style_2']

    current_date = date.today()
    file = f'./checklist/local_storage/totalrating_{current_date.strftime("%d.%m.%Y")}.xlsx'
    book_template.save(file)

    return file


def ratings_education_to_excel(ratings_set):
    style = style_excel()

    book_template = load_workbook(filename='./checklist/templates/template_education.xlsx')

    # Первый (активный) Лист книги
    sheet = book_template.active

    # Изменить имя Листа книги
    sheet.title = "Сводный рейтинг"

    number_col = 1
    for data in ratings_set:
        organisation = Organisations.objects.get(pk=data['organisations_id']).organisation_name

        type_organisation_id = Form_Type_Organisation.objects.get(organisation=data['organisations_id']).type_organisation_id
        type_organisation = Type_Organisations.objects.get(pk=type_organisation_id).type

        number_col += 1

        # # Вставить один столбец перед №___
        # sheet.insert_cols(number_col)

        column = number_col

        # Преобразую индекс столбца в его буквенное обозначение: 1 = "А"
        letter = get_column_letter(column)

        # Высота строки
        sheet.row_dimensions[1].height = 60

        # Ширина столбца
        sheet.column_dimensions[letter].width = 35

        # Добавить данные в ячейку
        row = 1
        sheet.cell(row, column).value = type_organisation
        sheet.cell(row, column).style = style['style_main']

        row = 2
        sheet.cell(row, column).value = organisation
        sheet.cell(row, column).style = style['style_main']

        row = 3
        sheet.cell(row, column).value = data['ratings_json']['rating_total']['value']
        sheet.cell(row, column).style = style['style_1']

        row = 4
        sheet.cell(row, column).value = data['ratings_json']['rating_1']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 5
        sheet.cell(row, column).value = data['ratings_json']['rating_1_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 6
        sheet.cell(row, column).value = data['ratings_json']['rating_1_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 7
        sheet.cell(row, column).value = data['ratings_json']['rating_1_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 8
        sheet.cell(row, column).value = data['ratings_json']['rating_2']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 9
        sheet.cell(row, column).value = data['ratings_json']['rating_2_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 10
        sheet.cell(row, column).value = data['ratings_json']['rating_2_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 11
        sheet.cell(row, column).value = data['ratings_json']['rating_3']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 12
        sheet.cell(row, column).value = data['ratings_json']['rating_3_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 13
        sheet.cell(row, column).value = data['ratings_json']['rating_3_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 14
        sheet.cell(row, column).value = data['ratings_json']['rating_3_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 15
        sheet.cell(row, column).value = data['ratings_json']['rating_4']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 16
        sheet.cell(row, column).value = data['ratings_json']['rating_4_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 17
        sheet.cell(row, column).value = data['ratings_json']['rating_4_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 18
        sheet.cell(row, column).value = data['ratings_json']['rating_4_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 19
        sheet.cell(row, column).value = data['ratings_json']['rating_5']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 20
        sheet.cell(row, column).value = data['ratings_json']['rating_5_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 21
        sheet.cell(row, column).value = data['ratings_json']['rating_5_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 22
        sheet.cell(row, column).value = data['ratings_json']['rating_5_3']['value']
        sheet.cell(row, column).style = style['style_2']

    current_date = date.today()
    file = f'./checklist/local_storage/totalrating_{current_date.strftime("%d.%m.%Y")}.xlsx'
    book_template.save(file)

    return file


def ratings_healthcare_to_excel(checking_id):

    ratings_set = Ratings.objects.values().filter(checking_id=checking_id)

    organisation_id_list = []
    for item in ratings_set:
        organisation_id_list.append(item['organisations_id'])

    organisation_unique_id = set(organisation_id_list)

    ratings_list = []
    for org_id in organisation_unique_id:
        ratings_org = Ratings.objects.values().filter(checking_id=checking_id, organisations_id=org_id)

        if len(ratings_org) > 1:
            ratings_consolidat = calculating_ratings_consolidat(ratings_org)
            ratings_list.append(ratings_consolidat)
            for r in ratings_org:
                ratings_list.append(r)
        else:
            ratings_list.append(ratings_org[0])

    style = style_excel()

    book_template = load_workbook(filename='./checklist/templates/template_healthcare.xlsx')

    # Первый (активный) Лист книги
    sheet = book_template.active

    # Изменить имя Листа книги
    sheet.title = "Сводный рейтинг"

    number_col = 1
    for data in ratings_list:
        organisation = Organisations.objects.get(pk=data['organisations_id']).organisation_name

        try:
            # type_organisation_id = Form_Type_Organisation.objects.get(organisation=data['organisations_id']).type_organisation_id
            type_organisation = Type_Organisations.objects.get(pk=data['type_organisations_id']).type
        except:
            type_organisation = 'Консолидированный по организации'

        number_col += 1

        column = number_col

        # Преобразую индекс столбца в его буквенное обозначение: 1 = "А"
        letter = get_column_letter(column)

        # Высота строки
        sheet.row_dimensions[1].height = 60

        # Ширина столбца
        sheet.column_dimensions[letter].width = 35

        # Добавить данные в ячейку
        row = 1
        sheet.cell(row, column).value = type_organisation
        sheet.cell(row, column).style = style['style_main']

        row = 2
        sheet.cell(row, column).value = organisation
        sheet.cell(row, column).style = style['style_main']

        row = 3
        sheet.cell(row, column).value = data['ratings_json']['rating_total']['value']
        sheet.cell(row, column).style = style['style_1']

        row = 4
        sheet.cell(row, column).value = data['ratings_json']['rating_1']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 5
        sheet.cell(row, column).value = data['ratings_json']['rating_1_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 6
        sheet.cell(row, column).value = data['ratings_json']['rating_1_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 7
        sheet.cell(row, column).value = data['ratings_json']['rating_1_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 8
        sheet.cell(row, column).value = data['ratings_json']['rating_2']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 9
        sheet.cell(row, column).value = data['ratings_json']['rating_2_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 10
        sheet.cell(row, column).value = data['ratings_json']['rating_2_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 11
        sheet.cell(row, column).value = data['ratings_json']['rating_2_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 12
        sheet.cell(row, column).value = data['ratings_json']['rating_3']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 13
        sheet.cell(row, column).value = data['ratings_json']['rating_3_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 14
        sheet.cell(row, column).value = data['ratings_json']['rating_3_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 15
        sheet.cell(row, column).value = data['ratings_json']['rating_3_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 16
        sheet.cell(row, column).value = data['ratings_json']['rating_4']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 17
        sheet.cell(row, column).value = data['ratings_json']['rating_4_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 18
        sheet.cell(row, column).value = data['ratings_json']['rating_4_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 19
        sheet.cell(row, column).value = data['ratings_json']['rating_4_3']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 20
        sheet.cell(row, column).value = data['ratings_json']['rating_5']['value']
        sheet.cell(row, column).style = style['style_3']

        row = 21
        sheet.cell(row, column).value = data['ratings_json']['rating_5_1']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 22
        sheet.cell(row, column).value = data['ratings_json']['rating_5_2']['value']
        sheet.cell(row, column).style = style['style_2']

        row = 23
        sheet.cell(row, column).value = data['ratings_json']['rating_5_3']['value']
        sheet.cell(row, column).style = style['style_2']

    current_date = date.today()
    file = f'./checklist/local_storage/totalrating_{current_date.strftime("%d.%m.%Y")}.xlsx'
    book_template.save(file)

    return file


def calculating_ratings_consolidat(ratings_org):

    ratings_0 = ratings_org[0]['ratings_json']
    ratings_1 = ratings_org[1]['ratings_json']

    coefficient = Coefficients.objects.values().get(type_departments=1)

    cfcnt_main = coefficient['main_json']

    quota = ratings_0['quota']['value'] + ratings_1['quota']['value']
    invalid_person = ratings_0['invalid_person']['value'] + ratings_1['invalid_person']['value']

    # Нормативное количество документов на Стенде и Сайте
    stend_count_all = ratings_0['stend_count_all']['value']
    web_count_all = ratings_0['web_count_all']['value']

    stend_count_yes = (ratings_0['stend_count_yes']['value'] + ratings_1['stend_count_yes']['value'])/2
    web_count_yes = (ratings_0['web_count_yes']['value'] + ratings_1['web_count_yes']['value'])/2

    count_person_1_3_stend = ratings_0['count_person_1_3_stend']['value'] + ratings_1['count_person_1_3_stend']['value']
    count_person_1_3_web = ratings_0['count_person_1_3_web']['value'] + ratings_1['count_person_1_3_web']['value']

    rating_1_1 = round((stend_count_yes/stend_count_all + web_count_yes/web_count_all)/2 * 100, 0)

    rating_1_2 = ratings_0['rating_1_2']['value']

    rating_1_3 = round((count_person_1_3_stend + count_person_1_3_web)/(quota * 2) * 100, 0)

    rating_2_1 = (ratings_0['rating_2_1']['value'] + ratings_1['rating_2_1']['value'])/2

    rating_2_2_1 = (ratings_0['rating_2_2_1']['value'] + ratings_1['rating_2_2_1']['value'])/2

    count_person_2_2_2 = ratings_0['count_person_2_2_2']['value'] + ratings_1['count_person_2_2_2']['value']
    rating_2_2_2 = round(count_person_2_2_2/quota * 100, 0)

    count_person_2_3 = ratings_0['count_person_2_3']['value'] + ratings_1['count_person_2_3']['value']
    rating_2_3 = round(count_person_2_3/quota * 100, 0)

    rating_3_1 = (ratings_0['rating_3_1']['value'] + ratings_1['rating_3_1']['value'])/2

    rating_3_2 = (ratings_0['rating_3_2']['value'] + ratings_1['rating_3_2']['value'])/2

    count_invalid_person_3_3 = ratings_0['count_invalid_person_3_3']['value'] + ratings_1['count_invalid_person_3_3']['value']
    rating_3_3 = round(count_invalid_person_3_3/invalid_person * 100, 0)

    count_person_4_1 = ratings_0['count_person_4_1']['value'] + ratings_1['count_person_4_1']['value']
    rating_4_1 = round(count_person_4_1/quota * 100, 0)

    count_person_4_2 = ratings_0['count_person_4_2']['value'] + ratings_1['count_person_4_2']['value']
    rating_4_2 = round(count_person_4_2/quota * 100, 0)

    count_person_4_3 = ratings_0['count_person_4_3']['value'] + ratings_1['count_person_4_3']['value']
    rating_4_3 = round(count_person_4_3/quota * 100, 0)

    count_person_5_1 = ratings_0['count_person_5_1']['value'] + ratings_1['count_person_5_1']['value']
    rating_5_1 = round(count_person_5_1/quota * 100, 0)

    count_person_5_2 = ratings_0['count_person_5_2']['value'] + ratings_1['count_person_5_2']['value']
    rating_5_2 = round(count_person_5_2/quota * 100, 0)

    count_person_5_3 = ratings_0['count_person_5_3']['value'] + ratings_1['count_person_5_3']['value']
    rating_5_3 = round(count_person_5_3/quota * 100, 0)

    rating_1 = round(rating_1_1 * float(cfcnt_main["k_1_1"]) + rating_1_2 * float(cfcnt_main["k_1_2"]) + rating_1_3 * float(cfcnt_main["k_1_3"]), 1)
    rating_2_2 = round(rating_2_2_1 * float(cfcnt_main["k_2_2_1"]) + rating_2_2_2 * float(cfcnt_main["k_2_2_2"]), 0)
    rating_2 = round(rating_2_1 * float(cfcnt_main["k_2_1"]) + rating_2_2 * float(cfcnt_main["k_2_2"]) + rating_2_3 * float(cfcnt_main["k_2_3"]), 1)
    rating_3 = round(rating_3_1 * float(cfcnt_main["k_3_1"]) + rating_3_2 * float(cfcnt_main["k_3_2"]) + rating_3_3 * float(cfcnt_main["k_3_3"]), 1)
    rating_4 = round(rating_4_1 * float(cfcnt_main["k_4_1"]) + rating_4_2 * float(cfcnt_main["k_4_2"]) + rating_4_3 * float(cfcnt_main["k_4_3"]), 1)
    rating_5 = round(rating_5_1 * float(cfcnt_main["k_5_1"]) + rating_5_2 * float(cfcnt_main["k_5_2"]) + rating_5_3 * float(cfcnt_main["k_5_3"]), 1)

    rating_total = round((rating_1 + rating_2 + rating_3 + rating_4 + rating_5)/5, 2)

    ratings_consolidate = {
        "quota": {"value": quota},
        "invalid_person": {"value": invalid_person},
        "rating_total": {"value": rating_total},
        "rating_1": {"value": rating_1},
        "rating_2": {"value": rating_2},
        "rating_3": {"value": rating_3},
        "rating_4": {"value": rating_4},
        "rating_5": {"value": rating_5},

        "rating_1_1": {"value": rating_1_1},
        "stend_count_yes": {"value": stend_count_yes},
        "stend_count_all": {"value": stend_count_all},
        "web_count_yes": {"value": web_count_yes},
        "web_count_all": {"value": web_count_all},
        "rating_1_2": {"value": rating_1_2},
        "rating_1_3": {"value": rating_1_3},
        "count_person_1_3_stend": {"value": count_person_1_3_stend},
        "count_person_1_3_web": {"value": count_person_1_3_web},

        "rating_2_1": {"value": rating_2_1},
        "rating_2_2": {"value": rating_2_2},
        "rating_2_2_1": {"value": rating_2_2_1},
        "rating_2_2_2": {"value": rating_2_2_2},
        "count_person_2_2_2": {"value": count_person_2_2_2},
        "rating_2_3": {"value": rating_2_3},
        "count_person_2_3": {"value": count_person_2_3},

        "rating_3_1": {"value": rating_3_1},
        "rating_3_2": {"value": rating_3_2},
        "rating_3_3": {"value": rating_3_3},
        "count_invalid_person_3_3": {"value": count_invalid_person_3_3},

        "rating_4_1": {"value": rating_4_1},
        "count_person_4_1": {"value": count_person_4_1},
        "rating_4_2": {"value": rating_4_2},
        "count_person_4_2": {"value": count_person_4_2},
        "rating_4_3": {"value": rating_4_3},
        "count_person_4_3": {"value": count_person_4_3},

        "rating_5_1": {"value": rating_5_1},
        "count_person_5_1": {"value": count_person_5_1},
        "rating_5_2": {"value": rating_5_2},
        "count_person_5_2": {"value": count_person_5_2},
        "rating_5_3": {"value": rating_5_3},
        "count_person_5_3": {"value": count_person_5_3},
    }

    return {'organisations_id': ratings_org[0]['organisations_id'], 'ratings_json': ratings_consolidate}


def style_excel():
    # Стиль данных и ячеек
    style_main = NamedStyle(name="style_main")
    style_main.font = Font(bold=False, size=12, color="000000")
    side = Side(style='thin', color="000000")
    style_main.border = Border(left=side, right=side, top=side, bottom=side)
    style_main.fill = PatternFill("solid", fgColor="FFFFFF")
    style_main.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    style_1 = NamedStyle(name="style_1")
    style_1.font = Font(bold=True, size=12, color="FFFFFF")
    side = Side(style='thin', color="000000")
    style_1.border = Border(left=side, right=side, top=side, bottom=side)
    style_1.fill = PatternFill("solid", fgColor="2F5597")
    style_1.alignment = Alignment(horizontal='center', vertical='center')

    style_2 = NamedStyle(name="style_2")
    style_2.font = Font(bold=False, size=12, color="000000")
    side = Side(style='thin', color="000000")
    style_2.border = Border(left=side, right=side, top=side, bottom=side)
    style_2.fill = PatternFill("solid", fgColor="c5e0b4")
    style_2.alignment = Alignment(horizontal='center', vertical='center')

    style_3 = NamedStyle(name="style_3")
    style_3.font = Font(bold=False, size=12, color="000000")
    side = Side(style='thin', color="000000")
    style_3.border = Border(left=side, right=side, top=side, bottom=side)
    style_3.fill = PatternFill("solid", fgColor="b4c7e7")
    style_3.alignment = Alignment(horizontal='center', vertical='center')

    style_4 = NamedStyle(name="style_4")
    style_4.font = Font(bold=False, size=12, color="000000")
    side = Side(style='thin', color="000000")
    style_4.border = Border(left=side, right=side, top=side, bottom=side)
    style_4.fill = PatternFill("solid", fgColor="afd095")
    style_4.alignment = Alignment(horizontal='center', vertical='center')

    return {
        'style_main': style_main,
        'style_1': style_1,
        'style_2': style_2,
        'style_3': style_3,
        'style_4': style_4,
    }



