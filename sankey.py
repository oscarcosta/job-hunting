import pandas as pd
import numpy as np


# https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0
def gen_sankey(df, cat_cols=[], value_cols='', title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    color_palette = ['#4B8BBE', '#306998', '#FFE873', '#FFD43B', '#646464']
    label_list = []
    color_num_list = []
    for cat_col in cat_cols:
        label_list_temp = df[cat_col].unique().tolist()
        color_num_list.append(len(label_list_temp))
        label_list = label_list + label_list_temp

    # remove duplicates from label_list
    label_list = list(dict.fromkeys(label_list))

    # define colors based on number of levels
    color_list = []
    for idx, color_num in enumerate(color_num_list):
        color_list = color_list + [color_palette[idx]] * color_num

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

    # add count to labels
    labels_tuple = np.unique(df[cat_cols].fillna(''), return_counts=True)
    for i in range(len(labels_tuple[0])):
        try:
            index = label_list.index(labels_tuple[0][i])
            label_list[index] = labels_tuple[0][i] + ": " + str(labels_tuple[1][i])
        except ValueError:
            pass

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
