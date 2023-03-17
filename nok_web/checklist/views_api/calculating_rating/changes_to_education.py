from ...app_models import Form_Sections, Coefficients

'''
Функция расчета баллов, по результатам корректировки количества респондентов.
'''


def education_rating(ratings_json, count_person):

    cfcnt_main = None

    sections_set = Form_Sections.objects.values()
    name = {}
    for section in sections_set:
        if section['rating_key']:
            name[f'{section["rating_key"]}'] = {"id": f'{section["id"]}',
                                                "text": f'{section["name"]}',
                                                "parent": f'{section["parent_id"]}',
                                                "order_num": f'{section["raring_order_num"]}'}

    coefficient = Coefficients.objects.values().get(type_departments=3)
    cfcnt_main = coefficient['main_json']

    quota = ratings_json["quota"]['value']
    invalid_person = ratings_json["invalid_person"]['value']

    rating_1_3 = round((int(count_person["count_person_1_3_stend"]) + int(count_person["count_person_1_3_web"]))/(quota * 2) * 100, 0)
    rating_2_3 = round(int(count_person["count_person_2_3"])/quota * 100, 0)
    if invalid_person > 0:
        rating_3_3 = round(int(count_person["count_invalid_person_3_3"])/invalid_person * 100, 0)
    else:
        rating_3_3 = 100
    rating_4_1 = round(int(count_person["count_person_4_1"])/quota * 100, 0)
    rating_4_2 = round(int(count_person["count_person_4_2"])/quota * 100, 0)
    rating_4_3 = round(int(count_person["count_person_4_3"])/quota * 100, 0)
    rating_5_1 = round(int(count_person["count_person_5_1"])/quota * 100, 0)
    rating_5_2 = round(int(count_person["count_person_5_2"])/quota * 100, 0)
    rating_5_3 = round(int(count_person["count_person_5_3"])/quota * 100, 0)

    rating_1 = round(ratings_json["rating_1_1"]['value'] * float(cfcnt_main["k_1_1"]) + ratings_json["rating_1_2"]['value'] * float(cfcnt_main["k_1_1"]) + rating_1_3 * float(cfcnt_main["k_1_3"]), 1)
    rating_2 = round((ratings_json["rating_2_1"]['value'] + rating_2_3)/2, 1)
    rating_3 = round(ratings_json["rating_3_1"]['value'] * float(cfcnt_main["k_3_1"]) + ratings_json["rating_3_2"]['value'] * float(cfcnt_main["k_3_2"]) + rating_3_3 * float(cfcnt_main["k_3_3"]), 1)
    rating_4 = round(rating_4_1 * float(cfcnt_main["k_4_1"]) + rating_4_2 * float(cfcnt_main["k_4_2"]) + rating_4_3 * float(cfcnt_main["k_4_3"]), 1)
    rating_5 = round(rating_5_1 * float(cfcnt_main["k_5_1"]) + rating_5_2 * float(cfcnt_main["k_5_2"]) + rating_5_3 * float(cfcnt_main["k_5_3"]), 1)

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
                       "value": ratings_json["rating_1_1"]['value'],
                       "name": name["rating_1_1"]["text"],
                       "parent": name["rating_1_1"]["parent"],
                       "order_num": name["rating_1_1"]["order_num"]},
        "stend_count_yes": {"id": name["stend_count_yes"]["id"],
                            "value": ratings_json['stend_count_yes']['value'],
                            "name": name["stend_count_yes"]["text"],
                            "parent": name["stend_count_yes"]["parent"],
                            "order_num": name["stend_count_yes"]["order_num"]},
        "stend_count_all": {"id": name["stend_count_all"]["id"],
                            "value": ratings_json['stend_count_all']['value'],
                            "name": name["stend_count_all"]["text"],
                            "parent": name["stend_count_all"]["parent"],
                            "order_num": name["stend_count_all"]["order_num"]},
        "web_count_yes": {"id": name["web_count_yes"]["id"],
                          "value": ratings_json['web_count_yes']['value'],
                          "name": name["web_count_yes"]["text"],
                          "parent": name["web_count_yes"]["parent"],
                          "order_num": name["web_count_yes"]["order_num"]},
        "web_count_all": {"id": name["web_count_all"]["id"],
                          "value": ratings_json['web_count_all']['value'],
                          "name": name["web_count_all"]["text"],
                          "parent": name["web_count_all"]["parent"],
                          "order_num": name["web_count_all"]["order_num"]},
        "rating_1_2": {"id": name["rating_1_2"]["id"],
                       "value": ratings_json["rating_1_2"]['value'],
                       "name": name["rating_1_2"]["text"],
                       "parent": name["rating_1_2"]["parent"],
                       "order_num": name["rating_1_2"]["order_num"]},
        "rating_1_3": {"id": name["rating_1_3"]["id"],
                       "value": rating_1_3,
                       "name": name["rating_1_3"]["text"],
                       "parent": name["rating_1_3"]["parent"],
                       "order_num": name["rating_1_3"]["order_num"]},
        "count_person_1_3_stend": {"id": name["count_person_1_3_stend"]["id"],
                                   "value": int(count_person["count_person_1_3_stend"]),
                                   "name": name["count_person_1_3_stend"]["text"],
                                   "parent": name["count_person_1_3_stend"]["parent"],
                                   "order_num": name["count_person_1_3_stend"]["order_num"]},
        "count_person_1_3_web": {"id": name["count_person_1_3_web"]["id"],
                                 "value": int(count_person["count_person_1_3_web"]),
                                 "name": name["count_person_1_3_web"]["text"],
                                 "parent": name["count_person_1_3_web"]["parent"],
                                 "order_num": name["count_person_1_3_web"]["order_num"]},

        "rating_2_1": {"id": name["rating_2_1"]["id"],
                       "value": ratings_json["rating_2_1"]['value'],
                       "name": name["rating_2_1"]["text"],
                       "parent": name["rating_2_1"]["parent"],
                       "order_num": name["rating_2_1"]["order_num"]},
        "rating_2_3": {"id": name["rating_2_3"]["id"],
                       "value": rating_2_3,
                       "name": name["rating_2_3"]["text"],
                       "parent": name["rating_2_3"]["parent"],
                       "order_num": name["rating_2_3"]["order_num"]},
        "count_person_2_3": {"id": name["count_person_2_3"]["id"],
                             "value": int(count_person["count_person_2_3"]),
                             "name": name["count_person_2_3"]["text"],
                             "parent": name["count_person_2_3"]["parent"],
                             "order_num": name["count_person_2_3"]["order_num"]},

        "rating_3_1": {"id": name["rating_3_1"]["id"],
                       "value": ratings_json["rating_3_1"]['value'],
                       "name": name["rating_3_1"]["text"],
                       "parent": name["rating_3_1"]["parent"],
                       "order_num": name["rating_3_1"]["order_num"]},
        "rating_3_2": {"id": name["rating_3_2"]["id"],
                       "value": ratings_json["rating_3_2"]['value'],
                       "name": name["rating_3_2"]["text"],
                       "parent": name["rating_3_2"]["parent"],
                       "order_num": name["rating_3_2"]["order_num"]},
        "rating_3_3": {"id": name["rating_3_3"]["id"],
                       "value": rating_3_3,
                       "name": name["rating_3_3"]["text"],
                       "parent": name["rating_3_3"]["parent"],
                       "order_num": name["rating_3_3"]["order_num"]},
        "count_invalid_person_3_3": {"id": name["count_invalid_person_3_3"]["id"],
                                     "value": int(count_person["count_invalid_person_3_3"]),
                                     "name": name["count_invalid_person_3_3"]["text"],
                                     "parent": name["count_invalid_person_3_3"]["parent"],
                                     "order_num": name["count_invalid_person_3_3"]["order_num"]},

        "rating_4_1": {"id": name["rating_4_1"]["id"],
                       "value": rating_4_1,
                       "name": name["rating_4_1"]["text"],
                       "parent": name["rating_4_1"]["parent"],
                       "order_num": name["rating_4_1"]["order_num"]},
        "count_person_4_1": {"id": name["count_person_4_1"]["id"],
                             "value": int(count_person["count_person_4_1"]),
                             "name": name["count_person_4_1"]["text"],
                             "parent": name["count_person_4_1"]["parent"],
                             "order_num": name["count_person_4_1"]["order_num"]},
        "rating_4_2": {"id": name["rating_4_2"]["id"],
                       "value": rating_4_2,
                       "name": name["rating_4_2"]["text"],
                       "parent": name["rating_4_2"]["parent"],
                       "order_num": name["rating_4_2"]["order_num"]},
        "count_person_4_2": {"id": name["count_person_4_2"]["id"],
                             "value": int(count_person["count_person_4_2"]),
                             "name": name["count_person_4_2"]["text"],
                             "parent": name["count_person_4_2"]["parent"],
                             "order_num": name["count_person_4_2"]["order_num"]},
        "rating_4_3": {"id": name["rating_4_3"]["id"],
                       "value": rating_4_3,
                       "name": name["rating_4_3"]["text"],
                       "parent": name["rating_4_3"]["parent"],
                       "order_num": name["rating_4_3"]["order_num"]},
        "count_person_4_3": {"id": name["count_person_4_3"]["id"],
                             "value": int(count_person["count_person_4_3"]),
                             "name": name["count_person_4_3"]["text"],
                             "parent": name["count_person_4_3"]["parent"],
                             "order_num": name["count_person_4_3"]["order_num"]},

        "rating_5_1": {"id": name["rating_5_1"]["id"],
                       "value": rating_5_1,
                       "name": name["rating_5_1"]["text"],
                       "parent": name["rating_5_1"]["parent"],
                       "order_num": name["rating_5_1"]["order_num"]},
        "count_person_5_1": {"id": name["count_person_5_1"]["id"],
                             "value": int(count_person["count_person_5_1"]),
                             "name": name["count_person_5_1"]["text"],
                             "parent": name["count_person_5_1"]["parent"],
                             "order_num": name["count_person_5_1"]["order_num"]},
        "rating_5_2": {"id": name["rating_5_2_education"]["id"],
                       "value": rating_5_2,
                       "name": name["rating_5_2_education"]["text"],
                       "parent": name["rating_5_2_education"]["parent"],
                       "order_num": name["rating_5_2_education"]["order_num"]},
        "count_person_5_2": {"id": name["count_person_5_2"]["id"],
                             "value": int(count_person["count_person_5_2"]),
                             "name": name["count_person_5_2_education"]["text"],
                             "parent": name["count_person_5_2_education"]["parent"],
                             "order_num": name["count_person_5_2_education"]["order_num"]},
        "rating_5_3": {"id": name["rating_5_3"]["id"],
                       "value": rating_5_3,
                       "name": name["rating_5_3"]["text"],
                       "parent": name["rating_5_3"]["parent"],
                       "order_num": name["rating_5_3"]["order_num"]},
        "count_person_5_3": {"id": name["count_person_5_3"]["id"],
                             "value": int(count_person["count_person_5_3"]),
                             "name": name["count_person_5_3"]["text"],
                             "parent": name["count_person_5_3"]["parent"],
                             "order_num": name["count_person_5_3"]["order_num"]},
    }

    return ratings