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

    excel_data = pd.read_csv('/home/maks/Документы/НОК/2024/Культура Шпаковский рн/Рейтинг для шаблонов.csv')
    json_str = excel_data.to_json(orient='records', date_format='iso')
    parsed = json.loads(json_str)

    context_dict = {}
    count = 0
    for data in parsed:
        print(f'{data=}')
        count += 1

        date_check = datetime.strptime(str(data["date_check"]), '%Y-%m-%d').strftime("%d.%m.%Y")

        context = { f'Организация': data["NameFull"],
                    f'Адрес': data["address"],
                    f'Дата_проверки': date_check,
                    f'Квота': data["quota"],
                    f'Балл': data["ball"],
                    }
        context_dict.update(context)
        doc_pattern(context_dict, count)

    return


def doc_pattern(context_dict, name_doc):
    try:
        template_path = '/home/maks/Документы/НОК/2024/Культура Шпаковский рн/Шаблон отчета Шпаковский МР культ.docx'
        doc = DocxTemplate(template_path)
        result_path = '/home/maks/Документы/НОК/2024/Культура Шпаковский рн/Отчеты Шпаковский культура'

        if not os.path.exists(result_path):
            os.mkdir(result_path)

        path_doc = f'{result_path}/{name_doc}.docx'

        doc.render(context_dict)
        doc.save(path_doc)

        # subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', result_path, path_doc])
    except Exception as ex:
        print(ex)

# import_registry_organisations()
