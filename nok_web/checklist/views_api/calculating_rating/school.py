import random
from rest_framework.response import Response
from .coefficients import coefficients, cfcnt_resp, points

'''
Функция расчета баллов, по результатам очного этапа.
'''


def school_rating(quota, invalid, answers, grouping_json):

    rating_1_1 = {}
    rating_1_2 = {}
    rating_2_1 = {}
    rating_3_1 = {}
    rating_3_2 = {}

    for section in grouping_json["pages"]:

        if section['id'] == 1:

            stend_count_yes = 0
            stend_count_all = 0
            web_count_yes = 0
            web_count_all = 0

            for criterion in section["criterion"]:
                nomber = criterion['name']

                for ans in answers:
                    if ans == nomber:

                        for items in answers[ans]:

                            if items['text'] == '11':
                                stend_count_all += 1
                                stend_count_yes += int(items['value'])
                            elif items['text'] == '12':
                                web_count_all += 1
                                web_count_yes += int(items['value'])

            try:
                rating = round((stend_count_yes/stend_count_all + web_count_yes/web_count_all)/2 * 100, 0)
            except:
                return Response({'error': 'Деление на ноль.'})

            rating_1_1 = {"stend_count_yes": stend_count_yes,
                           "stend_count_all": stend_count_all,
                           "web_count_yes": web_count_yes,
                           "web_count_all": web_count_all,
                           "rating": rating}

        elif section['id'] == 2:

            service_web_count = 0

            for criterion in section["criterion"]:
                nomber = criterion['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            service_web_count += int(items['value'])

            if service_web_count * points.p_1_2 < 100:
                rating = service_web_count * points.p_1_2
            else:
                rating = 100

            rating_1_2 = {"service_web_count": service_web_count,
                                           "rating": rating}

        elif section['id'] == 3:

            comfort_count = 0

            for criterion in section["criterion"]:
                nomber = criterion['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            comfort_count += int(items['value'])

            if comfort_count * points.p_2_1 < 100:
                rating = comfort_count * points.p_2_1
            else:
                rating = 100

            rating_2_1 = {"comfort_count": comfort_count,
                                           "rating": rating}

        elif section['id'] == 4:

            invalid_1_count = 0

            for criterion in section["criterion"]:
                nomber = criterion['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            invalid_1_count += int(items['value'])

            if invalid_1_count * points.p_3_1 < 100:
                rating = invalid_1_count * points.p_3_1
            else:
                rating = 100

            rating_3_1 = {"invalid_1_count": invalid_1_count,
                                           "rating": rating}

        elif section['id'] == 5:

            invalid_2_count = 0

            for criterion in section["criterion"]:
                nomber = criterion['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            invalid_2_count += int(items['value'])

            if invalid_2_count * points.p_3_2 < 100:
                rating = invalid_2_count * points.p_3_2
            else:
                rating = 100

            rating_3_2 = {"invalid_2_count": invalid_2_count,
                                           "rating": rating}



    rating_respondents = respondents_stage(quota, invalid, rating_1_1)

    rating_1 = round(rating_1_1['rating'] * coefficients.k_1_1 + rating_1_2['rating'] * coefficients.k_1_1 + rating_respondents['rating_1_3'] * coefficients.k_1_3, 1)
    rating_2 = round((rating_2_1['rating'] + rating_respondents['rating_2_3'])/2, 1)
    rating_3 = round(rating_3_1['rating'] * coefficients.k_3_1 + rating_3_2['rating'] * coefficients.k_3_2 + rating_respondents['rating_3_3'] * coefficients.k_3_3 , 1)
    rating_4 = round(rating_respondents['rating_4_1'] * coefficients.k_4_1 + rating_respondents['rating_4_2'] * coefficients.k_4_2 + rating_respondents['rating_4_3'] * coefficients.k_4_3 , 1)
    rating_5 = round(rating_respondents['rating_5_1'] * coefficients.k_5_1 + rating_respondents['rating_5_2'] * coefficients.k_5_2 + rating_respondents['rating_5_3'] * coefficients.k_5_3 , 1)

    rating_all = round((rating_1 + rating_2 + rating_3 + rating_4 + rating_5)/5, 2)


    ratings = {"rating_1": rating_1,
                "rating_1_1": rating_1_1,
                "rating_1_2": rating_1_2,
                "rating_1_3": rating_respondents['rating_1_3'],
                "rating_2": rating_2,
                "rating_2_1": rating_2_1,
               "rating_2_3": rating_respondents['rating_2_3'],
                "rating_3": rating_3,
                "rating_3_1": rating_3_1,
                "rating_3_2": rating_3_2,
               "rating_3_3": rating_respondents['rating_3_3'],
                "rating_4": rating_4,
               "rating_4_1": rating_respondents['rating_4_1'],
               "rating_4_2": rating_respondents['rating_4_2'],
               "rating_4_3": rating_respondents['rating_4_3'],
                "rating_5": rating_5,
               "rating_5_1": rating_respondents['rating_5_1'],
               "rating_5_2": rating_respondents['rating_5_2'],
               "rating_5_3": rating_respondents['rating_5_3'],
                "rating_all": rating_all}

    return ratings


def respondents_stage(quota, invalid, rating_1_1):

    rating_resp = {}

    rating_1_3_stend = rating_1_1['stend_count_yes'] / rating_1_1['stend_count_all'] * 100
    rating_1_3_web = rating_1_1['web_count_yes'] / rating_1_1['web_count_all'] * 100

    if rating_1_3_stend >= 90:
        kr_1_3_stend = 1
    else:
        kr_1_3_stend = random.uniform(cfcnt_resp.kr_1_3_stend_min, cfcnt_resp.kr_1_3_stend_max)

    if rating_1_3_web >= 90:
        kr_1_3_web = 1
    else:
        kr_1_3_web = random.uniform(cfcnt_resp.kr_1_3_web_min, cfcnt_resp.kr_1_3_web_max)

    rating_1_3_stend = quota * kr_1_3_stend
    rating_1_3_web = quota * kr_1_3_web
    rating_resp.update({'rating_1_3': round((rating_1_3_stend + rating_1_3_web)/(quota * 2) * 100, 0)})

    kr_2_3 = random.uniform(cfcnt_resp.kr_2_3_min, cfcnt_resp.kr_2_3_max)
    rating_resp.update({'rating_2_3': round((quota * kr_2_3)/quota * 100, 0)})

    if int(invalid) > 0:
        kr_3_3 = random.uniform(cfcnt_resp.kr_3_3_min, cfcnt_resp.kr_3_3_max)
        rating_resp.update({'rating_3_3': round((int(invalid) * kr_3_3)/int(invalid) * 100, 0)})
    else:
        rating_resp.update({'rating_3_3': 100})

    kr_4_1 = random.uniform(cfcnt_resp.kr_4_1_min, cfcnt_resp.kr_4_1_max)
    rating_resp.update({'rating_4_1': round((quota * kr_4_1)/quota * 100, 0)})

    kr_4_2 = random.uniform(cfcnt_resp.kr_4_2_min, cfcnt_resp.kr_4_2_max)
    rating_resp.update({'rating_4_2': round((quota * kr_4_2)/quota * 100, 0)})

    kr_4_3 = random.uniform(cfcnt_resp.kr_4_3_min, cfcnt_resp.kr_4_3_max)
    rating_resp.update({'rating_4_3': round((quota * kr_4_3)/quota * 100, 0)})

    kr_5_1 = random.uniform(cfcnt_resp.kr_5_1_min, cfcnt_resp.kr_5_1_max)
    rating_resp.update({'rating_5_1': round((quota * kr_5_1)/quota * 100, 0)})

    kr_5_2 = random.uniform(cfcnt_resp.kr_5_2_min, cfcnt_resp.kr_5_2_max)
    rating_resp.update({'rating_5_2': round((quota * kr_5_2)/quota * 100, 0)})

    kr_5_3 = random.uniform(cfcnt_resp.kr_5_3_min, cfcnt_resp.kr_5_3_max)
    rating_resp.update({'rating_5_3': round((quota * kr_5_3)/quota * 100, 0)})

    return rating_resp
