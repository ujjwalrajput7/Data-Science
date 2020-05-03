# coding=utf-8
import copy
import numpy as np
import pandas as pd
import random
from json.decoder import JSONDecodeError

# -----------------pyecharts------------------
from pyecharts.chart import Chart
from pyecharts.base import Base
import pyecharts.constants as constants
import pyecharts
from pyecharts import Bar, Line, Pie, Overlap, EffectScatter, Scatter, Grid, Timeline, Kline

# --------------process date-------------------------
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time


def render_echarts(df,
                   chart_title="figure1",
                   chart_introduce="",
                   chart_kind="bar",
                   legend_name=None,
                   dropna=False,
                   width="100%",
                   height=400,
                   **kwargs):
    '''render chart from Dataframe of Series
    
    Parameters:
    -------------------------------
    df: pd.DataFrame or pd.Series
        data 
    chart_title: str, 
        title
    chart_introduce: str,default 'figure1'
        introduce
    chart_kind: {'line','pie','effectScatter','scatter','bar'}
        the kind of chart we want to show
    legend_name: str, default None
        legend name
    dropna: bool, default False
        if drop na
    width: str,int or float, default '100%'
        the width of div including chart
    height: int or float, default 400
        the height of div including chart

    Returns:
    ----------------------------------
    pyecharts.Chart
    '''

    # chart's style
    title_color = "#000000"
    subtitle_color = "#333333"
    background_color = "rgba(0,0,0,0)"
    title_text_size = 21
    subtitle_text_size = 15

    label_color = [
        "#dd6b66", "#759aa0", "#e69d87", "#8dc1a9", "#ea7e53", "#eedd78",
        "#73a373", "#73b9bc", "#7289ab", "#91ca8c", "#f49f42"
    ]

    legend_text_color = '#666666'
    tooltip_text_color = "#FFFFFF"
    line_width = 3

    # kinds of chart
    if chart_kind == "line":
        chart = Line(
            chart_title,
            chart_introduce,
            width=width,
            height=height,
            title_color=title_color,
            subtitle_color=subtitle_color,
            background_color=background_color,
            title_text_size=title_text_size,
            subtitle_text_size=subtitle_text_size)

    elif chart_kind == "pie":
        chart = Pie(
            chart_title,
            chart_introduce,
            width=width,
            height=height,
            title_color=title_color,
            subtitle_color=subtitle_color,
            background_color=background_color,
            title_text_size=title_text_size,
            subtitle_text_size=subtitle_text_size)

    elif chart_kind == "effectScatter":
        chart = EffectScatter(
            chart_title,
            chart_introduce,
            width=width,
            height=height,
            title_color=title_color,
            subtitle_color=subtitle_color,
            background_color=background_color,
            title_text_size=title_text_size,
            subtitle_text_size=subtitle_text_size)

    elif chart_kind == "scatter":
        chart = Scatter(
            chart_title,
            chart_introduce,
            width=width,
            height=height,
            title_color=title_color,
            subtitle_color=subtitle_color,
            background_color=background_color,
            title_text_size=title_text_size,
            subtitle_text_size=subtitle_text_size)

    elif chart_kind == "bar":
        chart = Bar(
            chart_title,
            chart_introduce,
            width=width,
            height=height,
            title_color=title_color,
            subtitle_color=subtitle_color,
            background_color=background_color,
            title_text_size=title_text_size,
            subtitle_text_size=subtitle_text_size)

    else:
        print('wrong')
        return

    # if type of data is Series
    if type(df) == pd.core.series.Series:

        if chart_kind == "kline":
            print('not support kline')
            return

        # drop na
        if dropna:
            df.dropna(inplace=True)

        # index
        chart_index = list(df.index)

        # value
        val = list(df)
        chart.add(
            chart_title,
            chart_index,
            val,
            label_color=label_color,
            legend_text_color=legend_text_color,
            tooltip_text_color=tooltip_text_color,
            line_width=line_width,
            **kwargs)
        return chart

    # if type of data is pd.DataFrame
    elif type(df) == pd.core.frame.DataFrame:

        # change columns
        df.columns = [str(i) if type(i) != str else i for i in df.columns]

        # drop na
        if dropna:
            df.dropna(axis=0, how="all", thresh=None, inplace=True)

        # index
        chart_index = list(df.index)

        values = []
        value_names = []

        values = [list(df[col_name]) for col_name in df.columns]
        value_names = list(df.columns)

        if len(value_names) != len(values):
            print("wrong:")
            print(
                "value_names is %s,it's len is %d;values is %s,it's len is %d"
                % (value_names, len(value_names), values, len(values)))
            return

        for val, col_name in zip(values, value_names):

            chart.add(
                col_name,
                chart_index,
                val,
                label_color=label_color,
                legend_text_color=legend_text_color,
                tooltip_text_color=tooltip_text_color,
                line_width=line_width,
                **kwargs)

        return chart
    else:
        raise ValueError("type of data is wrong")


def change_index(df, how="column"):
    '''change multiindex to simple index

    Parameters:
    ----------------------------------------------
    how:{"columns","row"}, default 'column'
        change the name of columns or rows

    Returns:
    ---------------------------------------
    changed data
    '''

    if type(df) == pd.core.series.Series:
        return df

    if not (type(df.columns) == pd.core.indexes.multi.MultiIndex
            or type(df.index) == pd.core.indexes.multi.MultiIndex):
        return df

    # deepcopy
    df = copy.deepcopy(df)

    # record levels and labels
    if how == "column":
        levels = df.columns.levels
        labels = df.columns.labels
    elif how == "row":
        levels = df.index.levels
        labels = df.index.labels
    else:
        raise ValueError("参数how错误")

    dimension = len(labels)
    label_len = len(labels[0])

    mod_index = []
    for i in range(label_len):
        name = None
        for d in range(dimension):
            short_label = levels[d][labels[d][i]]
            short_label = str(
                short_label) if type(short_label) != str else short_label

            # add label
            if name is None:
                name = short_label
            else:
                name = name + '-' + short_label
        mod_index.append(name)

    # change levels and labels
    if how == "column":
        df.columns = mod_index
    elif how == "row":
        df.index = mod_index

    return df
