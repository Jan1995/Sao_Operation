from pyecharts import Bar, Line, Pie, WordCloud, Overlap
import pandas as pd


FILENAME = 'demo_anjuke.xlsx'


def get_sheet_names():
    df = pd.read_excel(FILENAME, None)
    return list(df.keys())[1:]


def get_datas(sheet):
    return pd.read_excel(FILENAME, sheet_name=sheet)


def get_district_price(dataframe, num_area):
    group = dataframe['价格（元/月）'].groupby(dataframe['位置2'])
    info = group.agg(['mean', 'count'])
    info = info.sort_values('count', ascending=False)[:num_area].astype(int)
    key = info.index
    value_1 = info['count']
    value_2 = info['mean']

    group = (dataframe['价格（元/月）']/dataframe['面积（平米）']
             ).groupby(dataframe['位置2'])
    info = group.agg(['mean', 'count'])
    info = info.sort_values('count', ascending=False)[:num_area].astype(int)
    value_3 = info['mean']

    bar = Bar('杭州主要区域房源数量与均价')
    bar.add('区域', key, value_1, xaxis_rotate=30, is_splitline_show=False)
    line1 = Line()
    line1.add('均价', key, value_2, xaxis_rotate=30, is_splitline_show=False, mark_point=['min', 'max', 'average'],
              line_width=3, line_color='blue')
    line2 = Line()
    line2.add('均价（面积）', key, value_3, xaxis_rotate=30, is_splitline_show=False, mark_point=['min', 'max', 'average'],
              line_width=3, line_color='black')
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line1, yaxis_index=1, is_add_yaxis=True)
    overlap.add(line2, yaxis_index=1, is_add_yaxis=True)
    overlap.render('区域与价格.html')


def get_num_price(dataframe):
    price = dataframe[['位置2', '价格（元/月）']]

    bins = [0, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000]
    level = ['0-1000', '1000-1500', '1500-2000', '2000-3000', '3000-4000',
             '4000-5000', '5000-6000', '6000-8000', '8000-1000', '10000以上']
    price_info = pd.cut(price['价格（元/月）'], bins=bins,
                        labels=level).value_counts().sort_index()

    key = price_info.index
    value = price_info.values
    bar = Bar('房源数量的价格分布')
    bar.add('数量', key, value, is_stack=True,
            xaxis_rotate=30, is_splitline_show=False)
    bar.render('房源数量与价格.html')


def get_num_area(dataframe):
    price = dataframe[['位置2', '面积（平米）']]

    bins = [0, 30, 60, 90, 120, 150, 200, 500]
    level = ['0-30', '30-60', '60-90', '90-120', '120-150', '150-200', '200以上']
    area_info = pd.cut(price['面积（平米）'], bins=bins,
                       labels=level).value_counts().sort_index()

    key = area_info.index
    value = area_info.values
    pie = Pie('房源数量的面积分布')
    pie.add('', key, value, radius=[40, 75],
            is_label_show=True, legend_orient='vertical', legend_pos='right')
    pie.render('房源数量与面积.html')


def get_num_roomtype(dataframe):
    group = dataframe['价格（元/月）'].groupby(dataframe['户型'])
    info = group.agg(['count'])
    key = info.index
    value = info['count']

    wordcloud = WordCloud('户型词云图')
    wordcloud.add('', key, value, word_size_range=[20, 80], shape='diamond')
    wordcloud.render('户型词云.html')

if __name__ == '__main__':
    sheets = get_sheet_names()

    dataframe = get_datas(sheets[0])
    for sheet in sheets[1:]:
        dataframe = dataframe.append(get_datas(sheet), ignore_index=True)

    get_district_price(dataframe, len(sheets))
    get_num_price(dataframe)
    get_num_area(dataframe)
    get_num_roomtype(dataframe)
