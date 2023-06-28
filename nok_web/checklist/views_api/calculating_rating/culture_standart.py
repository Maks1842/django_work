import random
from rest_framework.response import Response
from ...app_models import Form_Sections, Coefficients

'''
Функция расчета баллов, по результатам очного этапа.
'''


def culture_standart_rating(quota, invalid_person, answers, form_json, grouping_json):

    sections_set = Form_Sections.objects.values()
    name = {}
    for section in sections_set:
        if section['rating_key']:
            name[f'{section["rating_key"]}'] = {"id": f'{section["id"]}',
                                                "text": f'{section["name"]}',
                                                "parent": f'{section["parent_id"]}',
                                                "order_num": f'{section["raring_order_num"]}'}

    coefficient = Coefficients.objects.values().get(type_departments=2)

    cfcnt_main = coefficient['main_json']
    points = coefficient['points_json']

    rating_1_1 = {}
    rating_1_2 = {}
    rating_2_1 = {}
    rating_3_1 = {}
    rating_3_2 = {}
    count_1_1_value = {}

    # Нормативное количество документов на Стенде и Сайте
    stend_count_all = 9
    web_count_all = 12
    # for page in form_json["pages"]:
    #     for el in page["elements"]:
    #         for choic in el["choices"]:
    #             if choic["value"] == '11':
    #                 stend_count_all += 1
    #             elif choic["value"] == '12':
    #                 web_count_all += 1

    for section in grouping_json["pages"]:

        if section['id'] == 1:

            stend_count_yes = 0
            web_count_yes = 0

            for criterion in section["criterion"]:
                nomber = criterion['name']
                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            if items['text'] == '11':
                                stend_count_yes += int(items['value'])
                            elif items['text'] == '12':
                                web_count_yes += int(items['value'])

            try:
                rating = round((stend_count_yes/stend_count_all + web_count_yes/web_count_all)/2 * 100, 0)
            except:
                return Response({'error': 'Деление на ноль.'})

            rating_1_1 = rating
            count_1_1_value = {"stend_count_yes": stend_count_yes,
                               "stend_count_all": stend_count_all,
                               "web_count_yes": web_count_yes,
                               "web_count_all": web_count_all,
                               }

        elif section['id'] == 2:
            service_web_count = 0
            for criterion in section["criterion"]:
                nomber = criterion['name']
                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            service_web_count += int(items['value'])

            if service_web_count * int(points["p_1_2"]) < 100:
                rating_1_2 = service_web_count * int(points["p_1_2"])
            else:
                rating_1_2 = 100

            # rating_1_2 = {"service_web_count": service_web_count,
            #               "rating": rating}

        elif section['id'] == 3:
            comfort_count = 0
            for criterion in section["criterion"]:
                nomber = criterion['name']
                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            comfort_count += int(items['value'])

            if comfort_count * int(points["p_2_1"]) < 100:
                rating_2_1 = comfort_count * int(points["p_2_1"])
            else:
                rating_2_1 = 100

            # rating_2_1 = {"comfort_count": comfort_count,
            #                                "rating": rating}

        elif section['id'] == 4:
            invalid_1_count = 0
            for criterion in section["criterion"]:
                nomber = criterion['name']
                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            invalid_1_count += int(items['value'])

            if invalid_1_count * int(points["p_3_1"]) < 100:
                rating_3_1 = invalid_1_count * int(points["p_3_1"])
            else:
                rating_3_1 = 100

            # rating_3_1 = {"invalid_1_count": invalid_1_count,
            #                                "rating": rating}

        elif section['id'] == 5:
            invalid_2_count = 0
            for criterion in section["criterion"]:
                nomber = criterion['name']
                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            invalid_2_count += int(items['value'])

            if invalid_2_count * int(points["p_3_2"]) < 100:
                rating_3_2 = invalid_2_count * int(points["p_3_2"])
            else:
                rating_3_2 = 100

            # rating_3_2 = {"invalid_2_count": invalid_2_count,
            #                                "rating": rating}

    comment_expert_1 = answers["expert_1"]

    rating_respondents = respondents_stage(quota, invalid_person, count_1_1_value, comment_expert_1, coefficient)

    rating_1 = round(rating_1_1 * float(cfcnt_main["k_1_1"]) + rating_1_2 * float(cfcnt_main["k_1_2"]) + rating_respondents['rating_1_3'] * float(cfcnt_main["k_1_3"]), 1)
    rating_2 = round(rating_2_1 * float(cfcnt_main["k_2_1"]) + rating_respondents['rating_2_3'] * float(cfcnt_main["k_2_3"]), 1)
    rating_3 = round(rating_3_1 * float(cfcnt_main["k_3_1"]) + rating_3_2 * float(cfcnt_main["k_3_2"]) + rating_respondents['rating_3_3'] * float(cfcnt_main["k_3_3"]), 1)
    rating_4 = round(rating_respondents['rating_4_1'] * float(cfcnt_main["k_4_1"]) + rating_respondents['rating_4_2'] * float(cfcnt_main["k_4_2"]) + rating_respondents['rating_4_3'] * float(cfcnt_main["k_4_3"]), 1)
    rating_5 = round(rating_respondents['rating_5_1'] * float(cfcnt_main["k_5_1"]) + rating_respondents['rating_5_2'] * float(cfcnt_main["k_5_2"]) + rating_respondents['rating_5_3'] * float(cfcnt_main["k_5_3"]), 1)

    rating_total = round((rating_1 + rating_2 + rating_3 + rating_4 + rating_5)/5, 2)

    ratings = {
        "quota": {"id": name["quota"]["id"],
                  "value": quota,
                  "name": name["quota"]["text"],
                  "parent": name["quota"]["parent"],
                  "order_num": name["quota"]["order_num"]},
        "invalid_person": {"id": name["invalid_person"]["id"],
                           "value": invalid_person,
                           "name": name["invalid_person"]["text"],
                           "parent": name["invalid_person"]["parent"],
                           "order_num": name["invalid_person"]["order_num"]},
        "rating_total": {"id": name["rating_total"]["id"],
                         "value": rating_total,
                         "name": name["rating_total"]["text"],
                         "parent": name["rating_total"]["parent"],
                         "order_num": name["rating_total"]["order_num"]},
        "rating_1": {"id": name["rating_1"]["id"],
                     "value": rating_1,
                     "name": name["rating_1"]["text"],
                     "parent": name["rating_1"]["parent"],
                     "order_num": name["rating_1"]["order_num"]},
        "rating_2": {"id": name["rating_2"]["id"],
                     "value": rating_2,
                     "name": name["rating_2"]["text"],
                     "parent": name["rating_2"]["parent"],
                     "order_num": name["rating_2"]["order_num"]},
        "rating_3": {"id": name["rating_3"]["id"],
                     "value": rating_3,
                     "name": name["rating_3"]["text"],
                     "parent": name["rating_3"]["parent"],
                     "order_num": name["rating_3"]["order_num"]},
        "rating_4": {"id": name["rating_4"]["id"],
                     "value": rating_4,
                     "name": name["rating_4"]["text"],
                     "parent": name["rating_4"]["parent"],
                     "order_num": name["rating_4"]["order_num"]},
        "rating_5": {"id": name["rating_5"]["id"],
                     "value": rating_5,
                     "name": name["rating_5"]["text"],
                     "parent": name["rating_5"]["parent"],
                     "order_num": name["rating_5"]["order_num"]},

        "rating_1_1": {"id": name["rating_1_1"]["id"],
                       "value": rating_1_1,
                       "name": name["rating_1_1"]["text"],
                       "parent": name["rating_1_1"]["parent"],
                       "order_num": name["rating_1_1"]["order_num"]},
        "stend_count_yes": {"id": name["stend_count_yes"]["id"],
                            "value": count_1_1_value['stend_count_yes'],
                            "name": name["stend_count_yes"]["text"],
                            "parent": name["stend_count_yes"]["parent"],
                            "order_num": name["stend_count_yes"]["order_num"]},
        "stend_count_all": {"id": name["stend_count_all"]["id"],
                            "value": count_1_1_value['stend_count_all'],
                            "name": name["stend_count_all"]["text"],
                            "parent": name["stend_count_all"]["parent"],
                            "order_num": name["stend_count_all"]["order_num"]},
        "web_count_yes": {"id": name["web_count_yes"]["id"],
                          "value": count_1_1_value['web_count_yes'],
                          "name": name["web_count_yes"]["text"],
                          "parent": name["web_count_yes"]["parent"],
                          "order_num": name["web_count_yes"]["order_num"]},
        "web_count_all": {"id": name["web_count_all"]["id"],
                          "value": count_1_1_value['web_count_all'],
                          "name": name["web_count_all"]["text"],
                          "parent": name["web_count_all"]["parent"],
                          "order_num": name["web_count_all"]["order_num"]},
        "rating_1_2": {"id": name["rating_1_2"]["id"],
                       "value": rating_1_2,
                       "name": name["rating_1_2"]["text"],
                       "parent": name["rating_1_2"]["parent"],
                       "order_num": name["rating_1_2"]["order_num"]},
        "rating_1_3": {"id": name["rating_1_3"]["id"],
                       "value": rating_respondents['rating_1_3'],
                       "name": name["rating_1_3"]["text"],
                       "parent": name["rating_1_3"]["parent"],
                       "order_num": name["rating_1_3"]["order_num"]},
        "count_person_1_3_stend": {"id": name["count_person_1_3_stend"]["id"],
                                   "value": int(rating_respondents['count_person_1_3_stend']),
                                   "name": name["count_person_1_3_stend"]["text"],
                                   "parent": name["count_person_1_3_stend"]["parent"],
                                   "order_num": name["count_person_1_3_stend"]["order_num"]},
        "count_person_1_3_web": {"id": name["count_person_1_3_web"]["id"],
                                 "value": int(rating_respondents['count_person_1_3_web']),
                                 "name": name["count_person_1_3_web"]["text"],
                                 "parent": name["count_person_1_3_web"]["parent"],
                                 "order_num": name["count_person_1_3_web"]["order_num"]},

        "rating_2_1": {"id": name["rating_2_1"]["id"],
                       "value": rating_2_1,
                       "name": name["rating_2_1"]["text"],
                       "parent": name["rating_2_1"]["parent"],
                       "order_num": name["rating_2_1"]["order_num"]},
        "rating_2_3": {"id": name["rating_2_3"]["id"],
                       "value": rating_respondents['rating_2_3'],
                       "name": name["rating_2_3"]["text"],
                       "parent": name["rating_2_3"]["parent"],
                       "order_num": name["rating_2_3"]["order_num"]},
        "count_person_2_3": {"id": name["count_person_2_3"]["id"],
                             "value": int(rating_respondents['count_person_2_3']),
                             "name": name["count_person_2_3"]["text"],
                             "parent": name["count_person_2_3"]["parent"],
                             "order_num": name["count_person_2_3"]["order_num"]},

        "rating_3_1": {"id": name["rating_3_1"]["id"],
                       "value": rating_3_1,
                       "name": name["rating_3_1"]["text"],
                       "parent": name["rating_3_1"]["parent"],
                       "order_num": name["rating_3_1"]["order_num"]},
        "rating_3_2": {"id": name["rating_3_2"]["id"],
                       "value": rating_3_2,
                       "name": name["rating_3_2"]["text"],
                       "parent": name["rating_3_2"]["parent"],
                       "order_num": name["rating_3_2"]["order_num"]},
        "rating_3_3": {"id": name["rating_3_3"]["id"],
                       "value": rating_respondents['rating_3_3'],
                       "name": name["rating_3_3"]["text"],
                       "parent": name["rating_3_3"]["parent"],
                       "order_num": name["rating_3_3"]["order_num"]},
        "count_invalid_person_3_3": {"id": name["count_invalid_person_3_3"]["id"],
                                     "value": int(rating_respondents['count_invalid_person_3_3']),
                                     "name": name["count_invalid_person_3_3"]["text"],
                                     "parent": name["count_invalid_person_3_3"]["parent"],
                                     "order_num": name["count_invalid_person_3_3"]["order_num"]},

        "rating_4_1": {"id": name["rating_4_1"]["id"],
                       "value": rating_respondents['rating_4_1'],
                       "name": name["rating_4_1"]["text"],
                       "parent": name["rating_4_1"]["parent"],
                       "order_num": name["rating_4_1"]["order_num"]},
        "count_person_4_1": {"id": name["count_person_4_1"]["id"],
                             "value": int(rating_respondents['count_person_4_1']),
                             "name": name["count_person_4_1"]["text"],
                             "parent": name["count_person_4_1"]["parent"],
                             "order_num": name["count_person_4_1"]["order_num"]},
        "rating_4_2": {"id": name["rating_4_2"]["id"],
                       "value": rating_respondents['rating_4_2'],
                       "name": name["rating_4_2"]["text"],
                       "parent": name["rating_4_2"]["parent"],
                       "order_num": name["rating_4_2"]["order_num"]},
        "count_person_4_2": {"id": name["count_person_4_2"]["id"],
                             "value": int(rating_respondents['count_person_4_2']),
                             "name": name["count_person_4_2"]["text"],
                             "parent": name["count_person_4_2"]["parent"],
                             "order_num": name["count_person_4_2"]["order_num"]},
        "rating_4_3": {"id": name["rating_4_3"]["id"],
                       "value": rating_respondents['rating_4_3'],
                       "name": name["rating_4_3"]["text"],
                       "parent": name["rating_4_3"]["parent"],
                       "order_num": name["rating_4_3"]["order_num"]},
        "count_person_4_3": {"id": name["count_person_4_3"]["id"],
                             "value": int(rating_respondents['count_person_4_3']),
                             "name": name["count_person_4_3"]["text"],
                             "parent": name["count_person_4_3"]["parent"],
                             "order_num": name["count_person_4_3"]["order_num"]},

        "rating_5_1": {"id": name["rating_5_1"]["id"],
                       "value": rating_respondents['rating_5_1'],
                       "name": name["rating_5_1"]["text"],
                       "parent": name["rating_5_1"]["parent"],
                       "order_num": name["rating_5_1"]["order_num"]},
        "count_person_5_1": {"id": name["count_person_5_1"]["id"],
                             "value": int(rating_respondents['count_person_5_1']),
                             "name": name["count_person_5_1"]["text"],
                             "parent": name["count_person_5_1"]["parent"],
                             "order_num": name["count_person_5_1"]["order_num"]},
        "rating_5_2": {"id": name["rating_5_2_education"]["id"],
                       "value": rating_respondents['rating_5_2'],
                       "name": name["rating_5_2_education"]["text"],
                       "parent": name["rating_5_2_education"]["parent"],
                       "order_num": name["rating_5_2_education"]["order_num"]},
        "count_person_5_2": {"id": name["count_person_5_2"]["id"],
                             "value": int(rating_respondents['count_person_5_2']),
                             "name": name["count_person_5_2_education"]["text"],
                             "parent": name["count_person_5_2_education"]["parent"],
                             "order_num": name["count_person_5_2_education"]["order_num"]},
        "rating_5_3": {"id": name["rating_5_3"]["id"],
                       "value": rating_respondents['rating_5_3'],
                       "name": name["rating_5_3"]["text"],
                       "parent": name["rating_5_3"]["parent"],
                       "order_num": name["rating_5_3"]["order_num"]},
        "count_person_5_3": {"id": name["count_person_5_3"]["id"],
                             "value": int(rating_respondents['count_person_5_3']),
                             "name": name["count_person_5_3"]["text"],
                             "parent": name["count_person_5_3"]["parent"],
                             "order_num": name["count_person_5_3"]["order_num"]},
    }

    return ratings


def respondents_stage(quota, invalid_person, count_1_1_value, comment_expert_1, coefficient):

    comment_expert = []

    for exp in comment_expert_1:
        comment_expert.append(exp["value"])

    satisfactory_stend = comment_expert[0]
    satisfactory_web = comment_expert[1]

    cfcnt_resp = coefficient['respondents_json']

    rating_resp = {}

    rating_1_3_stend = count_1_1_value['stend_count_yes'] / count_1_1_value['stend_count_all'] * 100
    rating_1_3_web = count_1_1_value['web_count_yes'] / count_1_1_value['web_count_all'] * 100

    if satisfactory_stend == '1':
        if rating_1_3_stend >= 95:
            kr_1_3_stend = 1 - float(cfcnt_resp["correct_1_3"])
        else:
            kr_1_3_stend = random.uniform(float(cfcnt_resp["kr_1_3_stend_min"]), float(cfcnt_resp["kr_1_3_stend_max"])) - float(cfcnt_resp["correct_1_3"])
    else:
        if rating_1_3_stend >= 95:
            kr_1_3_stend = 1
        else:
            kr_1_3_stend = random.uniform(float(cfcnt_resp["kr_1_3_stend_min"]), float(cfcnt_resp["kr_1_3_stend_max"]))

    if satisfactory_web == '1':
        if rating_1_3_web >= 95:
            kr_1_3_web = 1 - float(cfcnt_resp["correct_1_3"])
        else:
            kr_1_3_web = random.uniform(float(cfcnt_resp["kr_1_3_web_min"]), float(cfcnt_resp["kr_1_3_web_max"])) - float(cfcnt_resp["correct_1_3"])
    else:
        if rating_1_3_web >= 95:
            kr_1_3_web = 1
        else:
            kr_1_3_web = random.uniform(float(cfcnt_resp["kr_1_3_web_min"]), float(cfcnt_resp["kr_1_3_web_max"]))

    count_person_1_3_stend = round(quota * kr_1_3_stend, 0)
    count_person_1_3_web = round(quota * kr_1_3_web, 0)
    rating_resp.update({'rating_1_3': round((count_person_1_3_stend + count_person_1_3_web)/(quota * 2) * 100, 0),
                        'count_person_1_3_stend': count_person_1_3_stend,
                        'count_person_1_3_web': count_person_1_3_web})

    kr_2_3 = random.uniform(float(cfcnt_resp["kr_2_3_min"]), float(cfcnt_resp["kr_2_3_max"]))
    count_person_2_3 = round(quota * kr_2_3, 0)
    rating_resp.update({'rating_2_3': round(count_person_2_3/quota * 100, 0),
                        'count_person_2_3': count_person_2_3})

    if invalid_person > 0:
        kr_3_3 = random.uniform(float(cfcnt_resp["kr_3_3_min"]), float(cfcnt_resp["kr_3_3_max"]))
        count_invalid_person_3_3 = round(invalid_person * kr_3_3, 0)
        rating_resp.update({'rating_3_3': round(count_invalid_person_3_3/invalid_person * 100, 0),
                            'count_invalid_person_3_3': count_invalid_person_3_3})
    else:
        count_invalid_person_3_3 = invalid_person
        rating_resp.update({'rating_3_3': 100,
                            'count_invalid_person_3_3': count_invalid_person_3_3})

    kr_4_1 = random.uniform(float(cfcnt_resp["kr_4_1_min"]), float(cfcnt_resp["kr_4_1_max"]))
    count_person_4_1 = round(quota * kr_4_1, 0)
    rating_resp.update({'rating_4_1': round(count_person_4_1/quota * 100, 0),
                        'count_person_4_1': count_person_4_1})

    kr_4_2 = random.uniform(float(cfcnt_resp["kr_4_2_min"]), float(cfcnt_resp["kr_4_2_max"]))
    count_person_4_2 = round(quota * kr_4_2, 0)
    rating_resp.update({'rating_4_2': round(count_person_4_2/quota * 100, 0),
                        'count_person_4_2': count_person_4_2})

    kr_4_3 = random.uniform(float(cfcnt_resp["kr_4_3_min"]), float(cfcnt_resp["kr_4_3_max"]))
    count_person_4_3 = round(quota * kr_4_3, 0)
    rating_resp.update({'rating_4_3': round(count_person_4_3/quota * 100, 0),
                        'count_person_4_3': count_person_4_3})

    kr_5_1 = random.uniform(float(cfcnt_resp["kr_5_1_min"]), float(cfcnt_resp["kr_5_1_max"]))
    count_person_5_1 = round(quota * kr_5_1, 0)
    rating_resp.update({'rating_5_1': round(count_person_5_1/quota * 100, 0),
                        'count_person_5_1': count_person_5_1})

    kr_5_2 = random.uniform(float(cfcnt_resp["kr_5_2_min"]), float(cfcnt_resp["kr_5_2_max"]))
    count_person_5_2 = round(quota * kr_5_2, 0)
    rating_resp.update({'rating_5_2': round(count_person_5_2/quota * 100, 0),
                        'count_person_5_2': count_person_5_2})

    kr_5_3 = random.uniform(float(cfcnt_resp["kr_5_3_min"]), float(cfcnt_resp["kr_5_3_max"]))
    count_person_5_3 = round(quota * kr_5_3, 0)
    rating_resp.update({'rating_5_3': round(count_person_5_3/quota * 100, 0),
                        'count_person_5_3': count_person_5_3})

    return rating_resp
