from docxtpl import DocxTemplate
from datetime import datetime
import os
import pandas as pd
import json

"""
Метод формирования отчетов по шаблону, с подстановкой тэгов
Заголовки столбцов должны быть на латинице, так как преобразуется в json
"""


def import_registry_organisations():

    excel_data = pd.read_excel('/home/maks/Документы/НОК/2023/Ставрополь образование/Реестр учреждений образования.xlsx')
    json_str = excel_data.to_json(orient='records', date_format='iso')
    parsed = json.loads(json_str)

    context_dict = {}
    for data in parsed:
        name_doc = data["Name"]

        date_check = datetime.strptime(data["date_check"], '%Y-%m-%dT00:00:00.000').strftime("%d.%m.%Y")

        context = { f'Организация': f'{data["NameFull"]}',
                    f'Адрес': f'{data["address"]}',
                    f'Сайт': f'{data["website"]}',
                    f'Дата_проверки': f'{date_check}',
                    }
        context_dict.update(context)
        doc_pattern(context_dict, name_doc)

    return


def doc_pattern(context_dict, name_doc):
    try:
        template_path = '/home/maks/Документы/НОК/2023/Ставрополь образование/Шаблон отчета Минкульт СК.docx'
        doc = DocxTemplate(template_path)
        result_path = '/home/maks/Документы/НОК/2023/Ставрополь образование/result'

        if not os.path.exists(result_path):
            os.mkdir(result_path)

        path_doc = f'{result_path}/{name_doc}.docx'

        doc.render(context_dict)
        doc.save(path_doc)

        # subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', result_path, path_doc])
    except Exception as ex:
        print(ex)

# import_registry_organisations()
