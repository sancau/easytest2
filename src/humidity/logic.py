"""
Humidity mode calculation logic (BL)
"""

from statistics import mean as python_mean


def calculate_mode(mode, log_slice):
    #######################
    # TEST BUSINESS LOGIC #
    #######################

    def mean(arr):
        return round(python_mean(arr), mode['round_to'])

    def rounded(number):
        return round(number, mode['round_to'])

    def get_abs_distance(a, b):
        return rounded(abs(max([a, b]) - min([a, b])))

    date = log_slice.date.max()

    dt1_humidity = log_slice.DT1_hum.values.tolist()
    dt2_humidity = log_slice.DT2_hum.values.tolist()

    kt_temperature = log_slice.KT_temp.values.tolist()
    kt_humidity = log_slice.KT_hum.values.tolist()

    target_humidity = mode['target']['humidity']
    hum_max_dev_settings = mode['max_deviation']['humidity']

    # if not special setting use default values
    humidity_max_deviation = \
        hum_max_dev_settings.get(target_humidity,
                                 hum_max_dev_settings['default'])

    max_mean_humidity = max(mean(dt1_humidity),
                            mean(dt2_humidity),
                            mean(kt_humidity))

    min_mean_humidity = min(mean(dt1_humidity),
                            mean(dt2_humidity),
                            mean(kt_humidity))

    md_delta_humidity = get_abs_distance(mean(kt_humidity),
                                         mean(mode['md']['humidity']))

    positive_deviation = get_abs_distance(max_mean_humidity, target_humidity)
    negative_deviation = get_abs_distance(min_mean_humidity, target_humidity)

    output = {  # resulting object with all the necessary data
        'date': date,
        'target': mode['target'],
        'max_allowed_deviation': {
            'temperature': mode['max_deviation']['temperature'],
            'humidity': humidity_max_deviation
        },
        'md_temperature': mode['md']['temperature'],
        'md_humidity': mode['md']['humidity'],
        'dt1_humidity': dt1_humidity,
        'dt2_humidity': dt2_humidity,
        'kt_humidity': kt_humidity,
        'kt_temperature': kt_temperature,
        'dt1_mean_temperature': mean(dt1_humidity),
        'dt2_mean_temperature': mean(dt2_humidity),
        'kt_mean_temperature': mean(kt_temperature),
        'kt_mean_humidity': mean(kt_humidity),
        'md_mean_temperature': mean(mode['md']['temperature']),
        'md_mean_humidity': mean(mode['md']['humidity']),
        'max_mean_humidity': max_mean_humidity,
        'min_mean_humidity': min_mean_humidity,
        'md_delta_humidity': md_delta_humidity,
        'positive_deviation': positive_deviation,
        'negative_deviation': negative_deviation,
        'humidity_deviation': rounded(max_mean_humidity - min_mean_humidity),
        'result': {}
    }

    if positive_deviation:
        tmp = rounded(abs(humidity_max_deviation[0]) - md_delta_humidity)
        output['result']['positive'] = {
            'passed': positive_deviation < tmp,
            'equation_result': tmp
        }

    if negative_deviation:
        tmp = rounded(abs(humidity_max_deviation[1]) - md_delta_humidity)
        output['result']['negative'] = {
            'passed': negative_deviation < tmp,
            'equation_result': tmp
        }

    output['result']['summary_mode_result'] = (
        output['result']['negative']['passed'] and
        output['result']['positive']['passed'])

    return output
