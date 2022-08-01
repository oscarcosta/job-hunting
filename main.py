import pandas as pd
import numpy as np
import plotly
from datetime import datetime, timedelta

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


if __name__ == '__main__':
    # read the data file
    df = pd.read_csv('data/Job Hunting - Sheet1.csv', sep=',', header=0,
                     usecols=['Date', 'Position', 'Technology', 'Ref/Site', 'Last Interation',
                              'Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Status'])

    # adjust status and dates columns
    two_weeks = datetime.today() - timedelta(weeks=2)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Last Interation'] = pd.to_datetime(df['Last Interation'], dayfirst=True)
    df.loc[(df['Status'] == "?") & (df['Last Interation'] <= two_weeks), 'Status'] = 'No Response'
    df.loc[(df['Status'] == "?") & (df['Last Interation'] > two_weeks), 'Status'] = 'Waiting'

    # print(df.to_string())

    plot_by_status(df)
    # plot_status_by_items(df, ['Ref/Site'], remove_recruiters=False)
    # plot_status_by_items(df, ['Position', 'Technology'])
