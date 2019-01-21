import pandas as pd

#将工作要求分离出来
# data = pd.read_csv('./boss_ZP.csv',encoding='gbk',usecols=[0,1,2,3,4,5])
#
# # a = []
# # a.append()
# for i,text in enumerate(data['工作要求']):
#     with open('job_require.txt','a') as f:
#         f.write(text)
#         print(i)

#制作词云
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import jieba
#
# text= open('./job_require.txt').read()
# word_list = jieba.cut(text,cut_all=True)
# wl_split = ' '.join(word_list).replace('算机','')
# print(wl_split)
# my_wordcloud = WordCloud(font_path='C:\Windows\Fonts\simfang.ttf').generate(wl_split)
# plt.imshow(my_wordcloud)
# plt.axis('off')
# plt.show()

#
#饼图制作-工资
# from pyecharts import Pie,Line,Scatter
# datas = pd.read_csv('./boss_ZP.csv',encoding='gbk',usecols=[0,1,2,3,4,5,6,7,8])

# scores = datas['avg_salary_codes'].groupby(datas['avg_salary_codes']).count()
# # print(scores)
# pie1 = Pie("工资", title_pos='left', width=900)
# pie1.add(
#     "工资",background_color='black',
#     attr=['1.5-20.0', '20.0-27.5', '27.5-30.0', '30.0-40.0', '40.0-95.0'],
#     value=scores.values,
#     # radius=[40, 75],
# #    center=[50, 50],
#     is_random=True,
# #    radius=[30, 75],
# #     is_legend_show=False,
#     is_label_show=True,
# )
# pie1.render(path='salary.html')


#饼图制作-经验
# from pyecharts import Pie,Line,Scatter
# datas = pd.read_csv('./boss_ZP.csv',encoding='gbk',usecols=[0,1,2,3,4,5,6,7,8])
# # print(datas['平均工资编码'])
# scores = datas['经验'].groupby(datas['经验']).count()
# print(scores)
# pie1 = Pie("经验", title_pos='left', width=900)
# pie1.add(
#     "工资",background_color='black',
#     attr=['1-3年', '10年以上', '1年以内', '3-5年 ', '5-10年','应届生','经验不限'],
#     value=scores.values,
#     radius=[40, 75],
#    center=[50, 50],
#     is_random=True,
#     # radius=[30, 75],
# #     is_legend_show=False,
#     is_label_show=True,
# )
# pie1.render(path='experience.html')

