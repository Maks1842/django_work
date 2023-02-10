from .coefficients import Coefficients

'''
Функция расчета баллов, по результатам корректировки количества респондентов.
'''


def education_rating(ratings_json, count_person):

    cfcnt_main = None

    for item_m in Coefficients.cfcnt_main:
        if "education" in item_m.keys():
            cfcnt_main = item_m["education"]

    quota = ratings_json["quota"]
    invalid_person = ratings_json["invalid_person"]

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

    rating_1 = round(ratings_json["rating_1_1"]["rating"] * float(cfcnt_main["k_1_1"]) + ratings_json["rating_1_2"]["rating"] * float(cfcnt_main["k_1_1"]) + rating_1_3 * float(cfcnt_main["k_1_3"]), 1)
    rating_2 = round((ratings_json["rating_2_1"]["rating"] + rating_2_3)/2, 1)
    rating_3 = round(ratings_json["rating_3_1"]["rating"] * float(cfcnt_main["k_3_1"]) + ratings_json["rating_3_2"]["rating"] * float(cfcnt_main["k_3_2"]) + rating_3_3 * float(cfcnt_main["k_3_3"]), 1)
    rating_4 = round(rating_4_1 * float(cfcnt_main["k_4_1"]) + rating_4_2 * float(cfcnt_main["k_4_2"]) + rating_4_3 * float(cfcnt_main["k_4_3"]), 1)
    rating_5 = round(rating_5_1 * float(cfcnt_main["k_5_1"]) + rating_5_2 * float(cfcnt_main["k_5_2"]) + rating_5_3 * float(cfcnt_main["k_5_3"]), 1)

    rating_total = round((rating_1 + rating_2 + rating_3 + rating_4 + rating_5)/5, 2)

    ratings = {
        "quota": {"value": quota,
                  "name": Coefficients.name["quota"]},
        "invalid_person": {"value": invalid_person,
                           "name": Coefficients.name["invalid_person"]},
        "rating_total": {"value": rating_total,
                         "name": Coefficients.name["rating_total"]},
        "rating_1": {"value": rating_1,
                     "name": Coefficients.name["rating_1"]},
        "rating_2": {"value": rating_2,
                     "name": Coefficients.name["rating_2"]},
        "rating_3": {"value": rating_3,
                     "name": Coefficients.name["rating_3"]},
        "rating_4": {"value": rating_4,
                     "name": Coefficients.name["rating_4"]},
        "rating_5": {"value": rating_5,
                     "name": Coefficients.name["rating_5"]},

        "rating_1_1": {"value": ratings_json["rating_1_1"],
                       "name": Coefficients.name["rating_1_1"]},
        "rating_1_2": {"value": ratings_json["rating_1_2"],
                       "name": Coefficients.name["rating_1_2"]},
        "rating_1_3": {"value": rating_1_3,
                       "name": Coefficients.name["rating_1_3"]},
        "count_person_1_3_stend": {"value": int(count_person["count_person_1_3_stend"]),
                                   "name": Coefficients.name["count_person_1_3_stend"]},
        "count_person_1_3_web": {"value": int(count_person["count_person_1_3_web"]),
                                 "name": Coefficients.name["count_person_1_3_web"]},

        "rating_2_1": {"value": ratings_json["rating_2_1"],
                       "name": Coefficients.name["rating_2_1"]},
        "rating_2_3": {"value": rating_2_3,
                       "name": Coefficients.name["rating_2_3"]},
        "count_person_2_3": {"value": int(count_person["count_person_2_3"]),
                             "name": Coefficients.name["count_person_2_3"]},

        "rating_3_1": {"value": ratings_json["rating_3_1"],
                       "name": Coefficients.name["rating_3_1"]},
        "rating_3_2": {"value": ratings_json["rating_3_2"],
                       "name": Coefficients.name["rating_3_2"]},
        "rating_3_3": {"value": rating_3_3,
                       "name": Coefficients.name["rating_3_3"]},
        "count_invalid_person_3_3": {"value": int(count_person["count_invalid_person_3_3"]),
                                     "name": Coefficients.name["count_invalid_person_3_3"]},

        "rating_4_1": {"value": rating_4_1,
                       "name": Coefficients.name["rating_4_1"]},
        "count_person_4_1": {"value": int(count_person["count_person_4_1"]),
                             "name": Coefficients.name["count_person_4_1"]},
        "rating_4_2": {"value": rating_4_2,
                       "name": Coefficients.name["rating_4_2"]},
        "count_person_4_2": {"value": int(count_person["count_person_4_2"]),
                             "name": Coefficients.name["count_person_4_2"]},
        "rating_4_3": {"value": rating_4_3,
                       "name": Coefficients.name["rating_4_3"]},
        "count_person_4_3": {"value": int(count_person["count_person_4_3"]),
                             "name": Coefficients.name["count_person_4_3"]},

        "rating_5_1": {"value": rating_5_1,
                       "name": Coefficients.name["rating_5_1"]},
        "count_person_5_1": {"value": int(count_person["count_person_5_1"]),
                             "name": Coefficients.name["count_person_5_1"]},
        "rating_5_2": {"value": rating_5_2,
                       "name": Coefficients.name["rating_5_2"]},
        "count_person_5_2": {"value": int(count_person["count_person_5_2"]),
                             "name": Coefficients.name["count_person_5_2"]},
        "rating_5_3": {"value": rating_5_3,
                       "name": Coefficients.name["rating_5_3"]},
        "count_person_5_3": {"value": int(count_person["count_person_5_3"]),
                             "name": Coefficients.name["count_person_5_3"]},
    }

    return ratings