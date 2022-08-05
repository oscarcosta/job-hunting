import pandas as pd
import numpy as np
import plotly
from datetime import datetime, timedelta
from currency_converter import CurrencyConverter
from sankey import gen_sankey


def plot_by_status(df):
    # filter out recruiters interviews
    df.query("`Status` != 'Recruiter'", inplace=True)

    # move Status to the first NaN column
    idx = pd.isna(df.values).argsort(axis=1)
    df = pd.DataFrame(
        df.values[np.arange(df.shape[0])[:, None], idx],
        index=df.index,
        columns=df.columns,
    )
    # print(df.to_string())

    fig = gen_sankey(df, cat_cols=['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5'],
                     title='Job Hunting Update - ' + datetime.today().strftime("%d/%m/%Y"))
    plotly.offline.plot(fig, validate=False)


def plot_status_by_items(df, items, remove_recruiters=True):
    # filter out recruiters interviews
    if remove_recruiters:
        df.query("`Status` != 'Recruiter'", inplace=True)

    fig = gen_sankey(df, cat_cols=['Step 1'] + items + ['Status'],
                     title='Job Hunting Status by ' + str(items) + ' - ' + datetime.today().strftime("%d/%m/%Y"))
    plotly.offline.plot(fig, validate=False)


def plot_salaries(df, filter_statuses=[]):
    # filter out recruiters and specified statuses
    filter_statuses.append('Recruiter')
    df = df[~df['Status'].isin(filter_statuses)]

    # expand the salary range column
    pattern = '((?P<salary_min>\d+)-)?(?P<salary_max>\d+)(?P<thousands>k?)\s(?P<currency>\w+)/(?P<period>H|M|Y)'
    df_salary = df['Salary Range'].str.extract(pattern, expand=True)
    df_salary[['thousands', 'currency', 'period']] = df_salary[['thousands', 'currency', 'period']].fillna('')
    # print(df_salary.to_string())

    pd.set_option("display.precision", 2)

    # normalize salary to a base currency and per year
    base_currency = 'USD'
    currencies = list(filter(lambda x: x != base_currency and x != '', df_salary['currency'].unique().tolist()))
    converter = CurrencyConverter(base_currency, currencies)
    df.insert(4, 'salary_min', df_salary.apply(lambda x: convert_salary(converter, x, 'salary_min'), axis=1))
    df.insert(5, 'salary_max', df_salary.apply(lambda x: convert_salary(converter, x, 'salary_max'), axis=1))
    # print(df.to_string())

    pd.options.plotting.backend = "plotly"
    fig = df.plot.bar(title='Salaries p/ Company', x='Company', y='salary_max')
    fig.show()


def convert_salary(converter, df, column):
    salary = float(df[column])
    if salary != salary:
        return salary
    salary = salary if df['thousands'] == '' else salary * 1000
    if df['period'] == 'M':
        salary *= 12
    elif df['period'] == 'H':
        salary *= 2080
    return converter.convert_to_base(salary, df['currency'])


# TODO structure project https://docs.python-guide.org/writing/structure/
if __name__ == '__main__':
    # read the data file
    df = pd.read_csv('data/Job Hunting - Sheet1.csv', sep=',', header=0,
                     usecols=['Date', 'Company', 'Position', 'Technology', 'Salary Range', 'Ref/Site',
                              'Last Interation', 'Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Status'])

    # adjust status and dates columns
    two_weeks = datetime.today() - timedelta(weeks=2)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Last Interation'] = pd.to_datetime(df['Last Interation'], dayfirst=True)
    df.loc[(df['Status'] == "?") & (df['Last Interation'] <= two_weeks), 'Status'] = 'No Response'
    df.loc[(df['Status'] == "?") & (df['Last Interation'] > two_weeks), 'Status'] = 'Waiting'
    # print(df.to_string())

    # plot_by_status(df)
    # plot_status_by_items(df, ['Ref/Site'], remove_recruiters=False)
    # plot_status_by_items(df, ['Ref/Site', 'Company'])
    # plot_status_by_items(df, ['Position', 'Technology'])

    plot_salaries(df, filter_statuses=['Reproved', 'No Response'])
