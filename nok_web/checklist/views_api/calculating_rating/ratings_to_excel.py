from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Font, NamedStyle, Side, Border, PatternFill, Alignment, GradientFill
from datetime import date

import logging

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

        result = ratings_to_excel(ratings_set)
        file_pointer = open(result, "rb")
        response = HttpResponse(file_pointer, content_type='application/vnd.openxmlformats-officedocument'
                                                           '.spreadsheetml.sheet;')
        response['Content-Disposition'] = f'attachment; filename=download.xlsx'
        response['Content-Transfer-Encoding'] = 'utf-8'
        return response


def ratings_to_excel(ratings_set):
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
        sheet.cell(row, column).style = style_main

        row = 2
        sheet.cell(row, column).value = data['ratings_json']['rating_total']['value']
        sheet.cell(row, column).style = style_1

        row = 3
        sheet.cell(row, column).value = data['ratings_json']['rating_1']['value']
        sheet.cell(row, column).style = style_3

        row = 4
        sheet.cell(row, column).value = data['ratings_json']['rating_1_1']['value']
        sheet.cell(row, column).style = style_2

        row = 5
        sheet.cell(row, column).value = data['ratings_json']['rating_1_2']['value']
        sheet.cell(row, column).style = style_2

        row = 6
        sheet.cell(row, column).value = data['ratings_json']['rating_1_3']['value']
        sheet.cell(row, column).style = style_2

        row = 7
        sheet.cell(row, column).value = data['ratings_json']['rating_2']['value']
        sheet.cell(row, column).style = style_3

        row = 8
        sheet.cell(row, column).value = data['ratings_json']['rating_2_1']['value']
        sheet.cell(row, column).style = style_2

        row = 9
        sheet.cell(row, column).value = data['ratings_json']['rating_2_3']['value']
        sheet.cell(row, column).style = style_2

        row = 10
        sheet.cell(row, column).value = data['ratings_json']['rating_3']['value']
        sheet.cell(row, column).style = style_3

        row = 11
        sheet.cell(row, column).value = data['ratings_json']['rating_3_1']['value']
        sheet.cell(row, column).style = style_2

        row = 12
        sheet.cell(row, column).value = rating_3_1_1
        sheet.cell(row, column).style = style_4

        row = 13
        sheet.cell(row, column).value = rating_3_1_2
        sheet.cell(row, column).style = style_4

        row = 14
        sheet.cell(row, column).value = rating_3_1_3
        sheet.cell(row, column).style = style_4

        row = 15
        sheet.cell(row, column).value = data['ratings_json']['rating_3_2']['value']
        sheet.cell(row, column).style = style_2

        row = 16
        sheet.cell(row, column).value = data['ratings_json']['rating_3_3']['value']
        sheet.cell(row, column).style = style_2

        row = 17
        sheet.cell(row, column).value = data['ratings_json']['rating_4']['value']
        sheet.cell(row, column).style = style_3

        row = 18
        sheet.cell(row, column).value = data['ratings_json']['rating_4_1']['value']
        sheet.cell(row, column).style = style_2

        row = 19
        sheet.cell(row, column).value = data['ratings_json']['rating_4_2']['value']
        sheet.cell(row, column).style = style_2

        row = 20
        sheet.cell(row, column).value = data['ratings_json']['rating_4_3']['value']
        sheet.cell(row, column).style = style_2

        row = 21
        sheet.cell(row, column).value = data['ratings_json']['rating_5']['value']
        sheet.cell(row, column).style = style_3

        row = 22
        sheet.cell(row, column).value = data['ratings_json']['rating_5_1']['value']
        sheet.cell(row, column).style = style_2

        row = 23
        sheet.cell(row, column).value = data['ratings_json']['rating_5_2']['value']
        sheet.cell(row, column).style = style_2

        row = 24
        sheet.cell(row, column).value = data['ratings_json']['rating_5_3']['value']
        sheet.cell(row, column).style = style_2

    current_date = date.today()
    file = f'./checklist/local_storage/totalrating_{current_date.strftime("%d.%m.%Y")}.xlsx'
    book_template.save(file)

    return file
