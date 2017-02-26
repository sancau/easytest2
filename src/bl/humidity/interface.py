# coding=utf-8

import pandas as pd

from bl.humidity.logic import calculate_mode


def parse_xlsx(data):
    dates = []
    df = pd.DataFrame()
    for item in data:
        file, label = item
        log = pd.read_excel(file, skiprows=56)
        log.columns = ['date', 'time', label + '_hum', label + '_temp', 'crap']
        dates.append(log.date[0].date())
        log.drop(['date', 'time', 'crap'], axis=1, inplace=True)
        df = log if df.empty else pd.merge(df, log,
                                           left_index=True,
                                           right_index=True,
                                           how='inner')

    date = max(dates)  # use latest date
    df['date'] = pd.Series([date for i in df.index])

    return df


def parse_csv(data):
    raise NotImplementedError('This method is not implemented yet')


def mode_valid(mode):
    return all(
        mode['slice_length'] == len(mode['md'][i])
        for i in ['humidity', 'temperature'])


def handle_mode(mode):
    # str to int
    mode['target']['temperature'] = int(mode['target']['temperature'])
    mode['target']['humidity'] = int(mode['target']['humidity'])
    mode['md']['temperature'] = [float(v) for v in mode['md']['temperature']]
    mode['md']['humidity'] = [float(v) for v in mode['md']['humidity']]

    if not mode_valid(mode):
        raise ValueError('Invalid humidity mode data provided')

    log = parse_xlsx((log['file'], log['desc']) for log in mode['logs'])

    log.drop(['DT1_temp', 'DT2_temp'], axis=1, inplace=True)  # no need

    slice_length = mode['slice_length']

    cursor = 0
    result = {}
    while True:
        log_slice = pd.DataFrame(log[cursor: cursor + slice_length])
        try:
            log_slice.DT1_hum = log_slice.DT1_hum.astype(float)
            log_slice.DT2_hum = log_slice.DT2_hum.astype(float)
            log_slice.KT_temp = log_slice.KT_temp.astype(float)
            log_slice.KT_hum = log_slice.KT_hum.astype(float)
        except ValueError:
            return result

        result = calculate_mode(mode, log_slice)

        if log_slice.shape[0] < 10 or result['result']['summary_mode_result']:
            return result  # if test totally passed return result or log ended
        else:
            cursor += 1  # move further
