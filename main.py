import pandas as pd
import numpy as np
import plotly
from datetime import date


# https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0
def gen_sankey(df, cat_cols=[], value_cols='', title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    color_palette = ['#4B8BBE', '#306998', '#FFE873', '#FFD43B', '#646464']
    label_list = []
    color_num_list = []
    for catCol in cat_cols:
        label_list_temp = list(set(df[catCol].values))
        color_num_list.append(len(label_list_temp))
        label_list = label_list + label_list_temp

    # remove duplicates from label_list
    label_list = list(dict.fromkeys(label_list))

    # define colors based on number of levels
    color_list = []
    for idx, colorNum in enumerate(color_num_list):
        color_list = color_list + [color_palette[idx]] * colorNum

    # add default value col if not defined
    if value_cols == '':
        df['value_col'] = 1
        value_cols = 'value_col'

    # transform df into a source-target pair
    for i in range(len(cat_cols) - 1):
        if i == 0:
            source_target_df = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            source_target_df.columns = ['source', 'target', 'count']
        else:
            temp_df = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            temp_df.columns = ['source', 'target', 'count']
            source_target_df = pd.concat([source_target_df, temp_df])
        source_target_df = source_target_df.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

    # add index for source-target pair
    source_target_df['sourceID'] = source_target_df['source'].apply(lambda x: label_list.index(x))
    source_target_df['targetID'] = source_target_df['target'].apply(lambda x: label_list.index(x))

    # creating the sankey diagram
    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=label_list,
            color=color_list
        ),
        link=dict(
            source=source_target_df['sourceID'],
            target=source_target_df['targetID'],
            value=source_target_df['count']
        )
    )

    layout = dict(
        title=title,
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data], layout=layout)
    return fig


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
                     title='Job Hunting Update - ' + date.today().strftime("%d/%m/%Y"))
    plotly.offline.plot(fig, validate=False)


def plot_by_ref_site(df):
    fig = gen_sankey(df, cat_cols=['Step 1', 'Ref/Site', 'Status'],
                     title='Job Hunting by Ref/Site - ' + date.today().strftime("%d/%m/%Y"))
    plotly.offline.plot(fig, validate=False)


if __name__ == '__main__':
    # read the data file
    df = pd.read_csv('data/Job Hunting - Sheet1.csv', sep=',', header=0,
                     usecols=['Date', 'Ref/Site', 'Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Status'])

    # adjust status column
    df.loc[df["Status"] == "?", "Status"] = 'No Response'

    # plot_by_status(df)
    plot_by_ref_site(df)
