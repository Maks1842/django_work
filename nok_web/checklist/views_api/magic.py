
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
        answer = ''
        answers = []
        x = str(8)
        if '11' in comparison[answ] or '12' in comparison[answ]:
            for a in comparison[answ]:
                if a == '':
                    answer = "Нет"
                elif int(a) > 0:
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                answers.append(answer)
        elif len(comparison[answ]) > 2:
            for a in comparison[answ]:
                if a != '':
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                    answers.append(answer)
        elif len(comparison[answ]) == 2 and comparison[answ][1] != '' and\
                (not '11' in comparison[answ][1] or not '12' in comparison[answ][1]):
            for a in comparison[answ]:
                if a != '':
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                    answers.append(answer)
        else:
            for a in comparison[answ]:
                if a == '':
                    answer = "Нет"
                elif a != '':
                    if len(query.get(pk=int(a))['name_alternativ']) > 0:
                        answer = query.get(pk=int(a))['name_alternativ']
                    else:
                        answer = query.get(pk=int(a))['value_name']
                answers.append(answer)
        list_dict[answ] = answers

    return list_dict