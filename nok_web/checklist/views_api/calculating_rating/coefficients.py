class Coefficients:
    cfcnt_main = [
        {"healthcare": {"k_1_1": "0.3",
                        "k_1_3": "0.4",

                        "k_3_1": "0.3",
                        "k_3_2": "0.4",
                        "k_3_3": "0.3",

                        "k_4_1": "0.4",
                        "k_4_2": "0.4",
                        "k_4_3": "0.2",

                        "k_5_1": "0.3",
                        "k_5_2": "0.2",
                        "k_5_3": "0.5"}},

        {"culture": {"k_1_1": "0.3",
                        "k_1_3": "0.4",

                        "k_3_1": "0.3",
                        "k_3_2": "0.4",
                        "k_3_3": "0.3",

                        "k_4_1": "0.4",
                        "k_4_2": "0.4",
                        "k_4_3": "0.2",

                        "k_5_1": "0.3",
                        "k_5_2": "0.2",
                        "k_5_3": "0.5"}},

        {"education": {"k_1_1": "0.3",
                     "k_1_3": "0.4",

                     "k_3_1": "0.3",
                     "k_3_2": "0.4",
                     "k_3_3": "0.3",

                     "k_4_1": "0.4",
                     "k_4_2": "0.4",
                     "k_4_3": "0.2",

                     "k_5_1": "0.3",
                     "k_5_2": "0.2",
                     "k_5_3": "0.5"}},
    ]

    cfcnt_resp = [
        {"healthcare": {"k_1_1": "0.3",
                        "k_1_3": "0.4",
                        "correct_1_3": "0.05",

                        "k_3_1": "0.3",
                        "k_3_2": "0.4",
                        "k_3_3": "0.3",

                        "k_4_1": "0.4",
                        "k_4_2": "0.4",
                        "k_4_3": "0.2",

                        "k_5_1": "0.3",
                        "k_5_2": "0.2",
                        "k_5_3": "0.5"}},

        {"culture": {"k_1_1": "0.3",
                     "k_1_3": "0.4",
                     "correct_1_3": "0.05",

                     "k_3_1": "0.3",
                     "k_3_2": "0.4",
                     "k_3_3": "0.3",

                     "k_4_1": "0.4",
                     "k_4_2": "0.4",
                     "k_4_3": "0.2",

                     "k_5_1": "0.3",
                     "k_5_2": "0.2",
                     "k_5_3": "0.5"}},

        {"education": {"kindergarden": {"kr_1_3_stend_min": "0.85",
                                        "kr_1_3_stend_max": "0.95",
                                        "kr_1_3_web_min": "0.85",
                                        "kr_1_3_web_max": "0.95",
                                        "correct_1_3": "0.05",

                                        "kr_2_3_min": "0.7",
                                        "kr_2_3_max": "0.9",

                                        "kr_3_3_min": "0.8",
                                        "kr_3_3_max": "0.95",

                                        "kr_4_1_min": "0.7",
                                        "kr_4_1_max": "0.9",

                                        "kr_4_2_min": "0.7",
                                        "kr_4_2_max": "0.9",

                                        "kr_4_3_min": "0.7",
                                        "kr_4_3_max": "0.9",

                                        "kr_5_1_min": "0.7",
                                        "kr_5_1_max": "0.9",

                                        "kr_5_2_min": "0.7",
                                        "kr_5_2_max": "0.9",

                                        "kr_5_3_min": "0.7",
                                        "kr_5_3_max": "0.9"},

                       "school": {"kr_1_3_stend_min": "0.7",
                                  "kr_1_3_stend_max": "0.9",
                                  "kr_1_3_web_min": "0.7",
                                  "kr_1_3_web_max": "0.9",
                                  "correct_1_3": "0.05",

                                  "kr_2_3_min": "0.7",
                                  "kr_2_3_max": "0.9",

                                  "kr_3_3_min": "0.8",
                                  "kr_3_3_max": "0.95",

                                  "kr_4_1_min": "0.7",
                                  "kr_4_1_max": "0.9",

                                  "kr_4_2_min": "0.7",
                                  "kr_4_2_max": "0.9",

                                  "kr_4_3_min": "0.7",
                                  "kr_4_3_max": "0.9",

                                  "kr_5_1_min": "0.7",
                                  "kr_5_1_max": "0.9",

                                  "kr_5_2_min": "0.7",
                                  "kr_5_2_max": "0.9",

                                  "kr_5_3_min": "0.7",
                                  "kr_5_3_max": "0.9"},

                       "techcollege": {"kr_1_3_stend_min": "0.7",
                                  "kr_1_3_stend_max": "0.9",
                                  "kr_1_3_web_min": "0.7",
                                  "kr_1_3_web_max": "0.9",
                                  "correct_1_3": "0.05",

                                  "kr_2_3_min": "0.7",
                                  "kr_2_3_max": "0.9",

                                  "kr_3_3_min": "0.8",
                                  "kr_3_3_max": "0.95",

                                  "kr_4_1_min": "0.7",
                                  "kr_4_1_max": "0.9",

                                  "kr_4_2_min": "0.7",
                                  "kr_4_2_max": "0.9",

                                  "kr_4_3_min": "0.7",
                                  "kr_4_3_max": "0.9",

                                  "kr_5_1_min": "0.7",
                                  "kr_5_1_max": "0.9",

                                  "kr_5_2_min": "0.7",
                                  "kr_5_2_max": "0.9",

                                  "kr_5_3_min": "0.7",
                                  "kr_5_3_max": "0.9"},

                       "addeducation": {"kr_1_3_stend_min": "0.7",
                                       "kr_1_3_stend_max": "0.9",
                                       "kr_1_3_web_min": "0.7",
                                       "kr_1_3_web_max": "0.9",
                                       "correct_1_3": "0.05",

                                       "kr_2_3_min": "0.7",
                                       "kr_2_3_max": "0.9",

                                       "kr_3_3_min": "0.8",
                                       "kr_3_3_max": "0.95",

                                       "kr_4_1_min": "0.7",
                                       "kr_4_1_max": "0.9",

                                       "kr_4_2_min": "0.7",
                                       "kr_4_2_max": "0.9",

                                       "kr_4_3_min": "0.7",
                                       "kr_4_3_max": "0.9",

                                       "kr_5_1_min": "0.7",
                                       "kr_5_1_max": "0.9",

                                       "kr_5_2_min": "0.7",
                                       "kr_5_2_max": "0.9",

                                       "kr_5_3_min": "0.7",
                                       "kr_5_3_max": "0.9"},}},
    ]

    points = [
        {"healthcare": {"p_1_2": "30",
                        "p_2_1": "20",
                        "p_3_1": "20",
                        "p_3_2": "20"}},

        {"culture": {"p_1_2": "30",
                     "p_2_1": "20",
                     "p_3_1": "20",
                     "p_3_2": "20"}},

        {"education": {"p_1_2": "30",
                       "p_2_1": "20",
                       "p_3_1": "20",
                       "p_3_2": "20"}},
    ]