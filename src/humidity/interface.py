import pandas as pd


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
        mode['slice_length'] == len(mode['md'][i]) for i in ['hum', 'temp'])


def calculate(mode_slice):
    pass


def handle_mode(mode):
    if not mode_valid(mode):
        raise ValueError('Invalid humidity mode data provided')

    log = parse_xlsx((log['file'], log['desc']) for log in mode['logs'])

    # splits log data in slices of required length
    # check if the test for slice is passed
    # if passed build result dict and return it
    # else try next slice till success or end of data
    # return result dict

    return log  # TODO return result dict
