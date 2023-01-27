from test_data import DataJson


def full_time_stage():
    coefficients = {
        "criterion_1": {
            "k1": 0.5,
            "k2": 2,
            "k3": 3,
        },
        "criterion_2": {
            "k1": 1,
            "k2": 2,
            "k3": 3,
        },
        "criterion_3": {
            "k1": 1,
            "k2": 2,
            "k3": 3,
        },
    }

    balls = {
        "ball_1": 10,
        "ball_2": 20,
        "ball_3": 30,
    }

    grouping_json = DataJson.grouping
    answers = DataJson.answers


    for section in grouping_json["pages"]:

        if section['id'] == 1:

            stend_count_yes = 0
            stend_count_all = 0
            web_count_yes = 0
            web_count_all = 0

            for crit in section["criterion"]:
                nomber = crit['name']

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
                rating_1_1 = round((stend_count_yes/stend_count_all + web_count_yes/web_count_all) * coefficients["criterion_1"]["k1"] * 100, 0)
            except Exception:
                print('Деление на ноль')



            print(f'stend_yes= {stend_count_yes}, stend_all= {stend_count_all}, web_yes= {web_count_yes}, web_all= {web_count_all}')
            print(f'rating_1_1= {rating_1_1}')


        elif section['id'] == 2:

            service_web_count = 0

            for crit in section["criterion"]:
                nomber = crit['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            service_web_count += int(items['value'])

            if service_web_count * balls['ball_3'] < 100:
                rating_1_2 = service_web_count * balls['ball_3']
            else:
                rating_1_2 = 100


            print(f'service_web_count= {service_web_count}')
            print(f'rating_1_2= {rating_1_2}')


        elif section['id'] == 3:

            service_web_count = 0

            for crit in section["criterion"]:
                nomber = crit['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            service_web_count += int(items['value'])

            if service_web_count * balls['ball_2'] < 100:
                rating_2_1 = service_web_count * balls['ball_2']
            else:
                rating_2_1 = 100


            print(f'service_web_count= {service_web_count}')
            print(f'rating_2_1= {rating_2_1}')



        elif section['id'] == 4:

            invalid_1_count = 0

            for crit in section["criterion"]:
                nomber = crit['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            invalid_1_count += int(items['value'])

            if invalid_1_count * balls['ball_2'] < 100:
                rating_3_1 = invalid_1_count * balls['ball_2']
            else:
                rating_3_1 = 100


            print(f'invalid_1_count= {invalid_1_count}')
            print(f'rating_3_1= {rating_3_1}')


        elif section['id'] == 5:

            invalid_2_count = 0

            for crit in section["criterion"]:
                nomber = crit['name']

                for ans in answers:
                    if ans == nomber:
                        for items in answers[ans]:
                            invalid_2_count += int(items['value'])

            if invalid_2_count * balls['ball_2'] < 100:
                rating_3_2 = invalid_2_count * balls['ball_2']
            else:
                rating_3_2 = 100


            print(f'invalid_2_count= {invalid_2_count}')
            print(f'rating_3_2= {rating_3_2}')





full_time_stage()