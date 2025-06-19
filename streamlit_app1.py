import streamlit as st
import matplotlib.tri as tri
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import plotly.graph_objects as go
from bokeh.models import  HoverTool
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import BoxSelectTool, LassoSelectTool
from sklearn.preprocessing import MinMaxScaler
import matplotlib
import seaborn as sns
from PIL import Image
from streamlit.components.v1 import html
from sklearn.preprocessing import StandardScaler
from matplotlib.patches import Rectangle
import plotly.figure_factory as ff
from bokeh.plotting import figure, show
from bokeh.sampledata.penguins import data as data
from bokeh.transform import factor_cmap, factor_mark
from openai import OpenAI

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
# 初始化 session state，如果不存在的话
if 'selected' not in st.session_state:
   st.session_state.selected = None
st.markdown("""

""", unsafe_allow_html=True)

# HTML 代码
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> </title>
    <style>
        * {-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}
        *, body {padding: 0px;margin: 0px;color: white;font-family: "微软雅黑";}
        @font-face {font-family: electronicFont;src: url(https://example.com/font/DS-DIGIT.TTF); /* 替换为实际字体文件的 URL */}
        body {background: #000d4a url(https://example.com/images/bg.jpg) center top;background-size: cover;color: #666;font-size: 0.1rem;line-height: 1.3; /* 设置行间距为 1.3 倍 */}
        li {list-style-type: none;}
        #MainMenu { width: 100%;  padding: 20px; margin-top:-50px;margin-left: -350px;margin-bottom: 10px;}
        .st-container { width: 100%;  padding: 20px; margin-top:-50px;margin-left: -350px;margin-bottom: 10px;}
        /* CSS 样式 */ 
        .title {font-size: 32px; text-align: left;margin-top:-50px;margin-left: -350px;margin-bottom: 10px;padding: 0;color: white;}
        .canvas{position: relative;  width:100%; min-height: 0vh; /* 使用视窗高度 */z-index: auto; /* 移除手动z-index */}
      
        .stTabs {width:1400px;  /* 调整 Tab 容器的宽度 */margin-left;  /* 居中 Tab 容器 */ margin-top:-40px;margin-left: -350px;color: white;}
        .stExpander {width: 1000px;  /* 设置宽度为父容器宽度的50% */ margin: auto;  /* 可选，用于居中 expander */color: white;}


    </style>
</head>
<body>
    <div class="canvas">
    <h1 class="title">氢燃料电池发动机系统空压机大数据平台</h1>
    </div>
    <div class="canvas mainbox" id="streamlit-container">
        <!-- Streamlit 容器将插入到这里 -->
    </div>



</body>
</html>
"""

# 在 Streamlit 中渲染 HTML
st.markdown(html_code, unsafe_allow_html=True)

# 创建一组选项卡
tabs = st.tabs(["首页", "数据分析", "趋势分析", "AI对话", "操作示例"])



# 根据用户的选择显示不同的页面内容
with tabs[0]:

    # 创建三列布局，设置宽度比例为 4:3:3
    left, middle, right = st.columns([2.5, 5, 2.5])

    # 在左侧列填充内容
    with left:
        row1 = st.columns(1)
        row2 = st.columns(1)


        with row1[0]:
            tile = st.container(height=270, border=True)  # 创建容器
        with tile:
            # 定义 CSS 样式
            st.markdown(
                """
                <style>
                .custom-container {
                    width: 300px;              /* 设置容器宽度 */
                    height: 30px;             /* 设置容器高度 */
                    background: linear-gradient(45deg, #191c83, transparent);
                    
                    
                    padding: 10px;             /* 设置内边距 */
                    margin-top:-10px;margin-left: 0px;
                }
                .title1 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}

                </style>

                """,
                unsafe_allow_html=True
            )

            # 创建一个较小的自定义容器
            st.markdown("""
                <style>
                </style>
                <body>
                    <div class="custom-container">
                    <h2 class="title1">数据库介绍</h2>
                    </div>
       
                </body>
                """
                ,
                unsafe_allow_html=True
            )

            # 使用行内样式调整字号
            st.markdown(
                """
                <p>
                    <span style="font-size:15px;"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本数据库包含氢燃料电池发动机系统空压机结构参数、性能指标等信息。平台用于研究在燃料电池电堆空压机设计研发过程中遇到的空压机结构设计匹配问题。利用大数据分析和机器学习，辅助河北金士顿有限公司空压机进行结构设计和大数据性能分析，辅助其完成数据检索，基于机器学习工具，训练空压机结构同性能间的关系，为燃料电池电堆空压机的设计提供理论指导。</strong></span>
                </p>
                """,
                unsafe_allow_html=True
            )
        with row2[0]:
            tile1 = st.container(height=270, border=True)  # 创建容器
        with tile1:
            # 定义 CSS 样式
            st.markdown(
                """
                <style>
                .custom-container1 {
                    width: 300px;              /* 设置容器宽度 */
                    height: 30px;             /* 设置容器高度 */
                    background: linear-gradient(45deg, #191c83, transparent);


                    padding: 10px;             /* 设置内边距 */
                    margin-top:-10px;margin-left: 0px;
                }
                .title12 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}

                </style>

                """,
                unsafe_allow_html=True
            )

            # 创建一个较小的自定义容器
            st.markdown("""
                <style>
                </style>
                <body>
                    <div class="custom-container12">
                    <h1 class="title1">数据库数据详情</h1>
                    </div>

                </body>
                """
                        ,
                        unsafe_allow_html=True
                        )
            # 示例数据
            data = pd.DataFrame({
                'date': pd.date_range(start='1/1/2012', periods=365),
                'temp_max': np.random.randint(-5, 40, size=365),
                'precipitation': np.random.random(size=365) * 10,
                'weather': np.random.choice(["sun", "fog", "drizzle", "rain", "snow"], size=365)
            })

            source = data

            scale = alt.Scale(
                domain=["sun", "fog", "drizzle", "rain", "snow"],
                range=["#53e7cc", "#37e0f3", "#1661b8", "#4595a1", "#7bb1bd"])
            color = alt.Color("weather:N", scale=scale)

            # 创建两个选择器：
            # - 一个在顶部面板上活动的刷选
            # - 一个在底部面板上活动的多点选择
            brush = alt.selection_interval(encodings=["x"])
            click = alt.selection_multi(encodings=["color"])

            # 顶部面板是温度与时间的散点图
            points = (
                alt.Chart()
                .mark_point(filled=True)  # 设置为实心圆点
                .encode(
                    alt.X("monthdate(date):T", title="Date"),
                    alt.Y(
                        "temp_max:Q",
                        title="Maximum Daily Temperature (C)",
                        scale=alt.Scale(domain=[-5, 40]),
                    ),
                    color=alt.condition(brush, color, alt.value("lightgray")),
                    size=alt.Size("precipitation:Q", scale=alt.Scale(range=[5, 200])),
                )
                .properties(width=500, height=200)
                .add_selection(brush)
                .transform_filter(click)
            )

            # 底部面板是天气类型的条形图
            bars = (
                alt.Chart()
                .mark_bar()
                .encode(
                    x="count()",
                    y="weather:N",
                    color=alt.condition(click, color, alt.value("lightgray")),
                )
                .transform_filter(brush)
                .properties(
                    width=500, height=100
                )
                .add_selection(click)
            )

            chart = alt.vconcat(points, bars, data=source, title="Seattle Weather: 2012-2015")

            # 创建一个容器并显示内容
            with st.container():


                # Add histogram data
                x1 = np.random.randn(200) - 2
                x2 = np.random.randn(200)
                x3 = np.random.randn(200) + 2
                x4 = np.random.randn(200) + 4
                df_011 = pd.read_excel('./data/data.xlsx', usecols=[60],
                                      header=None)
                df_012 = pd.read_excel('./data/data.xlsx', usecols=[61],
                                      header=None)
                df_013 = pd.read_excel('./data/data.xlsx', usecols=[69],
                                      header=None)
                df_014 = pd.read_excel('./data/data.xlsx', usecols=[65],
                                       header=None)

                # Group data together
                hist_data = [x1, x2, x3, x4]

                group_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
                # 定义自定义颜色列表
                colors = ['#70C7F3', ' #00F5FF', '#C724F1', '#00FFA3']  # 蓝色、红色、橙色、绿色
                # Create distplot with custom bin_size
                fig1 = ff.create_distplot(hist_data, group_labels, colors = colors,bin_size=.2)
                # 调整图表布局和尺寸
                fig1.update_layout(
                    height=230,  # 设置图表高度
                    margin=dict(l=20, r=20, t=0, b=20),  # 调整边距
                    legend=dict(  # 调整图例位置
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )

                st.markdown('<div class="custom-container5">', unsafe_allow_html=True)
                # st.altair_chart(chart, theme="streamlit", use_container_width=True)
                st.plotly_chart( fig1, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


    # 在中间列填充内容
    with middle:
        # 定义 CSS 样式
        row1 = st.columns(1)
        with row1[0]:
            tile50 = st.container(height=560, border=True)  # 创建容器
        with tile50:
            st.markdown(
                """
                <style>
                .custom-container2 {
                    width: 500px;              /* 设置容器宽度 */
                    height: 30px;             /* 设置容器高度 */
                    
                    
    
                    padding: 10px;             /* 设置内边距 */
                    margin-top:-10px;margin-left: 0px;
                }
                 
    
                .title13 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}
    
                </style>
    
                """,
                unsafe_allow_html=True
            )

            # 创建一个较小的自定义容器
            st.markdown("""
                            <style>
                            </style>
                            <body>
                                <div class="custom-container2">
                                <h1 class="title13">氢燃料电池发动机系统空压机性能总览图</h1>
                                </div>
                            </body>
                            """
                        ,
                        unsafe_allow_html=True
                        )
            # 自定义 CSS 调整容器样式
            st.markdown(
                """
                <style>
                
                .custom-container5 {
                    width: 500px;              /* 设置宽度 */
                    height: auto;              /* 自动调整高度 */
                    padding: 10px;             /* 设置内边距 */
                    margin: 0;                 /* 移除外边距 */
                     }
                </style>
                """,
                unsafe_allow_html=True
            )
            df011 = pd.read_excel('./data1/data1.xlsx', usecols=[61],
                                  header=None, skiprows=137, nrows=53)
            df012 = pd.read_excel('./data1/data1.xlsx', usecols=[61],
                                  header=None, skiprows=437, nrows=17)
            df013 = pd.read_excel('./data1/data1.xlsx', usecols=[61],
                                  header=None, skiprows=521, nrows=50)
            df021 = pd.read_excel('./data1/data1.xlsx', usecols=[60],
                                  header=None, skiprows=137, nrows=53)
            df022 = pd.read_excel('./data1/data1.xlsx', usecols=[60],
                                  header=None, skiprows=437, nrows=17)
            df023 = pd.read_excel('./data1/data1.xlsx', usecols=[60],
                                  header=None, skiprows=521, nrows=50)
            df031 = pd.read_excel('./data1/data1.xlsx', usecols=[70],
                                  header=None, skiprows=137, nrows=53)
            df032 = pd.read_excel('./data1/data1.xlsx', usecols=[70],
                                  header=None, skiprows=437, nrows=17)

            df033 = pd.read_excel('./data1/data1.xlsx', usecols=[70],
                                  header=None, skiprows=521, nrows=50)
            #./data/data.xlsx
            # 合并数据并转换为一维数组
            df01 = pd.concat([df011, df012, df013], ignore_index=True).squeeze()
            df02 = pd.concat([df021, df022, df023], ignore_index=True).squeeze()
            df03 = pd.concat([df031, df032, df033], ignore_index=True).squeeze()

            print("数据类型:", df01.dtype, df02.dtype, df03.dtype)
            print("NaN数量:", pd.isna(df01).sum(), pd.isna(df02).sum(), pd.isna(df03).sum())
            # 检查数据长度和NaN值
            print("数据长度:", len(df01), len(df02), len(df03))
            print("NaN数量:", pd.isna(df01).sum(), pd.isna(df02).sum(), pd.isna(df03).sum())

            array = df03
            value_array = df03  # 或者使用其他颜色数据

            fig = go.Figure(data=[go.Scatter3d(
                x=df01,
                y=df02,
                z=array,
                mode='markers',
                marker=dict(
                    size=12,
                    color=array,  # set color to an array/list of desired values
                    colorscale='Viridis',  # choose a colorscale
                    opacity=0.8
                )
            )])

            fig.update_layout(scene=dict(
                zaxis=dict(showbackground=False, title="等熵效率"),
                xaxis=dict(title="转速r/min", ),
                yaxis=dict(title="质量流量g/s"),
                aspectmode="manual",
                aspectratio=dict(x=2, y=1, z=0.5),
            ),
                width=500,  # 设置图表宽度，略小于容器宽度以考虑内边距
                height=450,  # 设置图表高度，略小于容器高度以考虑标题和内边距
                margin=dict(l=0, r=0, b=0, t=0), template="plotly_dark", )  # 暗色主题
            st.plotly_chart(fig, use_container_width=True, height=450)


    # 在右侧列填充内容
    with right:
        row1 = st.columns(1)
        row2 = st.columns(1)


        with row1[0]:
            tile = st.container(height=270, border=True)  # 创建容器
        with tile:
            # 定义 CSS 样式
            st.markdown(
                """
                <style>
                .custom-container3 {
                    width: 300px;              /* 设置容器宽度 */
                    height: 30px;             /* 设置容器高度 */
                    background: linear-gradient(45deg, #191c83, transparent);


                    padding: 10px;             /* 设置内边距 */
                    margin-top:-10px;margin-left: 0px;
                }
                .title5 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}

                </style>

                """,
                unsafe_allow_html=True
            )

            # 创建一个较小的自定义容器
            st.markdown("""
                        <style>
                        </style>
                        <body>
                            <div class="custom-container3">
                            <h1 class="title5">数据库结构设计参数</h1>
                            </div>

                        </body>
                        """
                        ,
                        unsafe_allow_html=True
                        )
            # 创建地球表面数据
            # 假设Excel文件名为'data.xlsx'，数据在第一个工作表
            df011 = pd.read_excel('./data/data.xlsx', usecols=[60], header=None,
                                  skiprows=575, nrows=100)
            df012 = pd.read_excel('./data/data.xlsx', usecols=[60], header=None,
                                  skiprows=192, nrows=80)
            df013 = pd.read_excel('./data/data.xlsx', usecols=[60], header=None,
                                  skiprows=1008, nrows=60)
            df021 = pd.read_excel('./data/data.xlsx', usecols=[61], header=None,
                                  skiprows=575, nrows=100)
            df022 = pd.read_excel('./data/data.xlsx', usecols=[61], header=None,
                                  skiprows=192, nrows=80)
            df023 = pd.read_excel('./data/data.xlsx', usecols=[61], header=None,
                                  skiprows=1008, nrows=60)
            df031 = pd.read_excel('./data/data.xlsx', usecols=[66], header=None,
                                  skiprows=575, nrows=100)
            df032 = pd.read_excel('./data/data.xlsx', usecols=[66], header=None,
                                  skiprows=192, nrows=80)

            df033 = pd.read_excel('./data/data.xlsx', usecols=[66], header=None,
                                  skiprows=1008, nrows=60)

            # 合并数据并转换为一维数组
            df01 = pd.concat([df011, df012, df013], ignore_index=True).squeeze()
            df02 = pd.concat([df021, df022, df023], ignore_index=True).squeeze()
            df03 = pd.concat([df031, df032, df033], ignore_index=True).squeeze()

            print("数据类型:", df01.dtype, df02.dtype, df03.dtype)
            print("NaN数量:", pd.isna(df01).sum(), pd.isna(df02).sum(), pd.isna(df03).sum())
            # 检查数据长度和NaN值
            print("数据长度:", len(df01), len(df02), len(df03))
            print("NaN数量:", pd.isna(df01).sum(), pd.isna(df02).sum(), pd.isna(df03).sum())

            array = df03

            value_array = df03  # 或者使用其他颜色数据


            fig = go.Figure(data=[go.Scatter3d(
                x=df01,
                y=df02,
                z=array,
                mode='markers',
                marker=dict(
                    size=12,
                    color=array,  # set color to an array/list of desired values
                    colorscale='Viridis',  # choose a colorscale
                    opacity=0.8
                )
            )])

            fig.update_layout(scene=dict(
                zaxis=dict(showbackground=False, title="压缩比"),
                xaxis=dict(title="转速r/min", ),
                yaxis=dict(title="质量流量g/s"),
                aspectmode="manual",
                aspectratio=dict(x=2, y=1, z=0.5),
            ),
                width=280,  # 设置图表宽度，略小于容器宽度以考虑内边距
                height=230,  # 设置图表高度，略小于容器高度以考虑标题和内边距
                margin=dict(l=0, r=0, b=0, t=0), template="plotly_dark", )  # 暗色主题

            from bokeh.plotting import figure, show
            from bokeh.sampledata.penguins import data
            from bokeh.transform import factor_cmap, factor_mark

            # 交互控制面板
            point_size = 12
            opacity = 0.6

            # 准备数据
            SPECIES = sorted(data.species.unique())
            MARKERS = ['hex', 'circle_x', 'triangle']

            # 创建图表
            p = figure(
                title="",
                tools="pan,wheel_zoom,box_zoom,reset,save,hover",
                background_fill_color=None,  # 设置背景为透明
                border_fill_color=None,  # 设置边框填充为透明
                width=200,
                height=200
            )
            p.scatter(
                "flipper_length_mm", "body_mass_g",
                source=data, size=18,
                fill_alpha=0.2, line_alpha=0,
                color=factor_cmap('species', 'Category10_3', SPECIES))
            # 配置坐标轴
            p.xaxis.axis_label = ''
            p.yaxis.axis_label = ''
            p.xaxis.axis_label_text_color = "white"
            p.yaxis.axis_label_text_color = "white"

            # 添加散点图（去掉legend_group参数以去除图例）
            scatter = p.scatter(
                "flipper_length_mm",
                "body_mass_g",
                source=data,
                fill_alpha=opacity,
                size=point_size,
                line_width=1,
                line_color="black",
                marker=factor_mark('species', MARKERS, SPECIES),
                color=factor_cmap('species', 'Category10_3', SPECIES)
            )

            # 配置图表样式
            p.title.text_color = "white"
            p.xgrid.grid_line_color = "#555555"
            p.ygrid.grid_line_color = "#555555"
            p.axis.major_tick_line_color = "white"
            p.axis.minor_tick_line_color = "white"
            p.axis.major_label_text_color = "white"

            # 显示图表
            st.bokeh_chart(p, use_container_width=True)
        with row2[0]:
            tile1 = st.container(height=270, border=True)  # 创建容器
        with tile1:
            # 定义 CSS 样式
            st.markdown(
                """
                <style>
                .custom-container11 {
                    width: 300px;              /* 设置容器宽度 */
                    height: 30px;             /* 设置容器高度 */
                    background: linear-gradient(45deg, #191c83, transparent);


                    padding: 10px;             /* 设置内边距 */
                    margin-top:-20px;margin-left: 0px;
                }
                .title6 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}

                </style>

                """,
                unsafe_allow_html=True
            )

            # 创建一个较小的自定义容器
            st.markdown("""
                        <style>
                        </style>
                        <body>
                            <div class="custom-container11">
                            <h1 class="title6">数据库数据类型</h1>
                            </div>

                        </body>
                        """
                        ,
                        unsafe_allow_html=True
                        )

            # 原始数据

            datas = [
                [
                    {"name": "国外论文", "value": 72.34},
                    {"name": "国内论文", "value": 27.66}
                ],
                [
                    {"name": "数值仿真", "value": 57.49},
                    {"name": "程序", "value": 3.74},
                    {"name": "实验", "value": 38.0}
                ]
            ]
            # 数据
            labels = ['国外论文', '国内论文']
            values = [72.34, 27.66]
            labels1 = ['数值仿真', '程序','实验']
            values1 = [57.49, 3.74, 38.0]



            htmlpath1 = "http://192.168.43.181:9089/tzgy8hfiu2a1/"
            st.components.v1.iframe(htmlpath1, width=None, height=200)



with tabs[1]:
# elif st.session_state.selected == '数据分析':
# 创建三列布局，设置宽度比例为 4:3:3
    left1, middle2,middle1 = st.columns([0.3, 0.1,0.7])

    # 在左侧列填充内容
    with left1:

    # 定义 CSS 样式
        st.markdown(
            """
            <style>
            .custom-container6 {
                width: 370px;              /* 设置容器宽度 */
                height: 30px;             /* 设置容器高度 */
                background: linear-gradient(45deg, #191c83, transparent);
        
        
                padding: 10px;             /* 设置内边距 */
                margin-top:-10px;margin-left: 0px;
            }
            .title7 {font-size: 25px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}
        
            </style>
        
            """,
            unsafe_allow_html=True
        )

        # 创建一个较小的自定义容器
        st.markdown("""
                        <style>
                        </style>
                        <body>
                            <div class="custom-container6">
                            <h1 class="title1">数据录入</h1>
                            </div>
        
                        </body>
                        """
                    ,
                    unsafe_allow_html=True
                    )

    # 文件上传组件
        uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

        if uploaded_file is not None:
            # 根据文件类型读取数据
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file,header=2)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file,header=2,engine='openpyxl')

            # 显示数据
            st.write("上传的文件数据：")
            st.write(df)
        st.markdown(
            """
            <style>
            .custom-container7 {
                width: 370px;              /* 设置容器宽度 */
                height: 30px;             /* 设置容器高度 */
                background: linear-gradient(45deg, #191c83, transparent);
    
    
                padding: 10px;             /* 设置内边距 */
                
            }
            .title2 {font-size: 25px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}
    
            </style>
    
            """,
            unsafe_allow_html=True
        )
        if uploaded_file is not None:
            # 根据文件类型读取数据
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, header=2)  # 直接传递文件对象给 pandas
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, header=2 ,engine='openpyxl')  # 需要指定引擎

    with middle1:
        tile11 = st.container(height=560, border=True)  # 创建容器
        with tile11:

            st.markdown(
                """
                <style>
                .custom-container7 {
                    width: 500px;              /* 设置容器宽度 */
                    height: 30px;             /* 设置容器高度 */
                    background: linear-gradient(45deg, #191c83, transparent);


                    padding: 10px;             /* 设置内边距 */
                    margin-top:-10px;margin-left: 0px;
                }


                .title8 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}

                </style>

                """,
                unsafe_allow_html=True
            )

            # 创建一个较小的自定义容器
            st.markdown("""
                                    <style>
                                    </style>
                                    <body>
                                        <div class="custom-container1">
                                        <h1 class="title8">数据分析</h1>
                                        </div>
                                    </body>
                                    """
                        ,
                        unsafe_allow_html=True
                        )
            ''
            ''



            option = st.selectbox(
                "图表类型选择",
                ("散点图1", "间距不规则数据的等值线图", "重叠密度（“山脊图”）", "散点图", "相关性分析","小提琴图","散点频率图","直方图、kde 图和地毯图","二维散点图","三维散点图"),
            )
            # 根据选择显示不同内容

            if option == "散点图1":


                # 1. 先获取清洗后的数据
                all_columns = df.columns.tolist()


                title1 = st.selectbox("请选择x轴的列", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                titlex = st.text_input("请输入x轴的列名")
                title2 = st.selectbox("请选择y轴参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                titley = st.text_input("请输入y轴的列名")
                values2 = st.slider("选择第一个y的表格范围", 0, 2000, (25, 75))
                values3 = st.slider("选择第二个y的表格范围", 0, 2000, (25, 75))
                values4 = st.slider("选择第三个y的表格范围", 0, 2000, (25, 75))
                values5 = st.slider("选择第四个y的表格范围", 0, 2000, (25, 75))


                titlex1 = st.text_input("请输入图表名称")





                # 2. 定义分组列（类似 species）和标记
                MARKERS = ['hex', 'circle_x', 'triangle','square']
                # 1.1 输入species名称（支持多个）
                # 品种名称
                species_input = st.text_input("输入品种名称（用逗号分隔4个名称）",
                                              "品种1,品种2,品种3,品种4")
                species_list = [s.strip() for s in species_input.split(",") if s.strip()][:4]

                titlex1 = st.text_input("请输入图表名称", f"{title2} 四范围对比")

                # 3. 准备数据
                ranges = [values2, values3, values4, values5]
                data_combined = pd.DataFrame()

                for i, (start, end) in enumerate(ranges):
                    section = df.iloc[start:end + 1].copy()
                    section["group"] = species_list[i] if i < len(species_list) else f"品种{i + 1}"
                    data_combined = pd.concat([data_combined, section])

                SPECIES = sorted(data_combined["group"].unique())
                MARKERS = ['hex', 'circle_x', 'triangle','square']
                p = figure(title = titlex1, background_fill_color="#fafafa")
                p.xaxis.axis_label = titlex
                p.yaxis.axis_label = titley

                p.scatter(title1, title2, source=data_combined,
                          legend_group="group",  # 按分组列区分
                          fill_alpha=0.4, size=12,
                          marker=factor_mark('group', MARKERS, SPECIES),  # 按分组分配标记形状
                          color=factor_cmap('group', 'Category10_4', SPECIES)  # 按分组分配颜色
                          )
                p.legend.location = "top_left"
                p.legend.title = "Species"

                show(p)


            elif option == "相关性分析":
                def heatmap(data, row_labels, col_labels, ax=None,
                            cbar_kw=None, cbarlabel="", **kwargs):
                    """
                    Create a heatmap from a numpy array and two lists of labels.

                    Parameters
                    ----------
                    data
                        A 2D numpy array of shape (M, N).
                    row_labels
                        A list or array of length M with the labels for the rows.
                    col_labels
                        A list or array of length N with the labels for the columns.
                    ax
                        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
                        not provided, use current Axes or create a new one.  Optional.
                    cbar_kw
                        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
                    cbarlabel
                        The label for the colorbar.  Optional.
                    **kwargs
                        All other arguments are forwarded to `imshow`.
                    """

                    if ax is None:
                        ax = plt.gca()

                    if cbar_kw is None:
                        cbar_kw = {}

                    # Plot the heatmap
                    im = ax.imshow(data, **kwargs)

                    # Create colorbar
                    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
                    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

                    # Show all ticks and label them with the respective list entries.
                    ax.set_xticks(range(data.shape[1]), labels=col_labels,
                                  rotation=-30, ha="right", rotation_mode="anchor")
                    ax.set_yticks(range(data.shape[0]), labels=row_labels)

                    # Let the horizontal axes labeling appear on top.
                    ax.tick_params(top=True, bottom=False,
                                   labeltop=True, labelbottom=False)

                    # Turn spines off and create white grid.
                    ax.spines[:].set_visible(False)

                    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
                    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
                    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
                    ax.tick_params(which="minor", bottom=False, left=False)

                    return im, cbar


                def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                                     textcolors=("black", "white"),
                                     threshold=None, **textkw):
                    """
                    A function to annotate a heatmap.

                    Parameters
                    ----------
                    im
                        The AxesImage to be labeled.
                    data
                        Data used to annotate.  If None, the image's data is used.  Optional.
                    valfmt
                        The format of the annotations inside the heatmap.  This should either
                        use the string format method, e.g. "$ {x:.2f}", or be a
                        `matplotlib.ticker.Formatter`.  Optional.
                    textcolors
                        A pair of colors.  The first is used for values below a threshold,
                        the second for those above.  Optional.
                    threshold
                        Value in data units according to which the colors from textcolors are
                        applied.  If None (the default) uses the middle of the colormap as
                        separation.  Optional.
                    **kwargs
                        All other arguments are forwarded to each call to `text` used to create
                        the text labels.
                    """

                    if not isinstance(data, (list, np.ndarray)):
                        data = im.get_array()

                    # Normalize the threshold to the images color range.
                    if threshold is not None:
                        threshold = im.norm(threshold)
                    else:
                        threshold = im.norm(data.max()) / 2.

                    # Set default alignment to center, but allow it to be
                    # overwritten by textkw.
                    kw = dict(horizontalalignment="center",
                              verticalalignment="center")
                    kw.update(textkw)

                    # Get the formatter in case a string is supplied
                    if isinstance(valfmt, str):
                        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

                    # Loop over the data and create a `Text` for each "pixel".
                    # Change the text's color depending on the data.
                    texts = []
                    for i in range(data.shape[0]):
                        for j in range(data.shape[1]):
                            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                            texts.append(text)

                    return texts
                # 获取所有列（包括非数值列）
                all_columns = df.columns.tolist()  # 替代原先的 numeric_columns
                # 让用户选择多个列

                selected_columns = st.multiselect(
                    "选择要做相关性分析的列",
                    options=df.columns.tolist(),
                    default=df.columns.tolist()[:2]  # 默认选择前两列
                )
                # 根据选择的列创建一个新的DataFrame
                df = df[selected_columns]
                # 去除包含缺失值的行
                df_clean = df.dropna()

                genre = st.radio(
                    "请选择相关性分析方法",
                    ["Pearson", "Spearman ", ],
                    index=None,
                )

                st.write("You selected:", genre)
                if genre == "Pearson":

                    # 计算相关系数矩阵
                    print('几种变量的相关系数矩阵为：\n', df_clean.corr(method='pearson'))
                    st.write('几种变量的相关系数矩阵为：\n', df_clean.corr(method='pearson'))
                    #绘制热力图

                    vegetables = selected_columns
                    farmers = selected_columns
                    harvest =df_clean.corr(method='pearson')

                    fig, ax = plt.subplots()

                    im, cbar = heatmap(harvest, vegetables, farmers, ax=ax,
                                       cmap="YlGn", cbarlabel="")
                    texts = annotate_heatmap(im, valfmt="{x:.3f}")

                    fig.tight_layout()
                    plt.show()
                    st.pyplot(fig)
                elif genre == "Spearman ":
                    # 计算相关系数矩阵
                    print('几种变量的相关系数矩阵为：\n', df_clean.corr(method='spearman'))
                    st.write('几种变量的相关系数矩阵为：\n', df_clean.corr(method='spearman'))
                    # 绘制热力图

                    vegetables = selected_columns
                    farmers = selected_columns
                    harvest = df_clean.corr(method='spearman')

                    fig, ax = plt.subplots()

                    im, cbar = heatmap(harvest, vegetables, farmers, ax=ax,
                                       cmap="YlGn", cbarlabel="")
                    texts = annotate_heatmap(im, valfmt="{x:.3f}")

                    fig.tight_layout()
                    plt.show()
                    st.pyplot(fig)

            elif option == "直方图、kde 图和地毯图":


                all_columns = df.columns.tolist()  # 替代原先的 numeric_columns
                normalize_choice = st.radio(
                    "是否要进行标准化处理",
                    ["是", "否", ],
                    index=None,
                )

                st.write("You selected:", normalize_choice)
                selected = []
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    selected.append(st.selectbox(
                        "第一个结构设计参数",
                        all_columns,
                        index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0
                    ))
                with col2:
                    selected.append(st.selectbox(
                        "第二个结构设计参数",
                        all_columns,
                        index=all_columns.index("压缩比") if "压缩比" in all_columns else 0
                    ))
                with col3:
                    selected.append(st.selectbox(
                        "第三个结构设计参数",
                        all_columns,
                        index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0
                    ))
                with col4:
                    selected.append(st.selectbox(
                        "第四个结构设计参数",
                        all_columns,
                        index=all_columns.index("压缩比") if "压缩比" in all_columns else 0
                    ))

                cleaned_data = {}
                for i, col in enumerate(selected, 1):
                    try:
                        # 转换为数值类型并去除非数值
                        series = pd.to_numeric(df[col], errors='coerce').dropna()
                        if len(series) > 0:
                            cleaned_data[f"col{i}"] = series
                        else:
                            st.warning(f"列 '{col}' 无有效数值数据")
                    except Exception as e:
                        st.error(f"处理列 '{col}' 时出错: {str(e)}")

                # 标准化处理
                if normalize_choice == "是":
                    scaler = StandardScaler()
                    for i in range(1, 5):
                        col_key = f"col{i}"
                        if col_key in cleaned_data:
                            col_data = cleaned_data[col_key]
                            cleaned_data[col_key] = pd.Series(
                                scaler.fit_transform(col_data.values.reshape(-1, 1)).flatten(),
                                index=col_data.index
                            )
                            st.success(f"列 {selected[i - 1]} 已标准化")


                # # 删除包含NaN的行
                # df_clean = df.dropna(subset=cols_to_check)
                # 转为NumPy数组（显式调用，推荐）
                # array1 = cleaned_data["df_clean1"].to_numpy()  # 第1列数组
                # array2 = cleaned_data["df_clean2"].to_numpy()  # 第2列数组
                # array3 = cleaned_data["df_clean3"].to_numpy()  # 第3列数组
                # array4 = cleaned_data["df_clean4"].to_numpy()  # 第4列数组

                    # Add histogram data
                # x1 = np.random.randn(200) - 2
                # x2 = np.random.randn(200)
                # x3 = np.random.randn(200) + 2
                # x4 = np.random.randn(200) + 4
                #
                # # Group data together
                hist_data = [ ]

                group_labels = []
                for i in range(1, 5):
                    col_key = f"col{i}"
                    if col_key in cleaned_data:
                        hist_data.append(cleaned_data[col_key].values)
                        group_labels.append(selected[i - 1])
                # Create distplot with custom bin_size
                colors = ['#898988', '#79cb9b', '#547ac0', '#a369b0']
                # colors = ['#d7f0fc', '#9499c0','#ddedd1','#7fc7a5']  # 蓝色和橙色
                colors = ['#A4C8D7', '#8AB78E', '#C8AFDC', '#FFB466']

                fig = ff.create_distplot(hist_data, group_labels, bin_size=.2,colors=colors)
                # 调整透明度和边缘线
                for trace in fig.data:
                    trace.update(
                        opacity=1,  # 设置透明度（0-1）
                        marker=dict(
                            line=dict(
                                color='black',  # 边缘线颜色
                                width=1  # 边缘线宽度
                            )
                        )
                    )
                # 在 x=0 处添加红色虚线
                fig.add_vline(
                    x=0,
                    line_dash="dash",  # 虚线样式
                    line_color="red",  # 红色
                    line_width=2,  # 线宽
                    opacity=0.8,  # 透明度
                    # annotation_text="x=0",  # 可选：添加标注文本
                    # annotation_position="top right"  # 文本位置
                )
                # 设置图例位置和样式
                fig.update_layout(
                    plot_bgcolor='white',  # 图表区域背景色
                    paper_bgcolor='white',  # 整个画布背景色
                    margin=dict(l=100, r=100, t=100, b=100),  # 边距（避免内容紧贴边框）
                    xaxis=dict(
                        tickfont=dict(size=20, family='SimHei', color='black'),
                        linewidth=2,  # 设置x轴线条粗细
                        linecolor='black'  # 设置x轴线条颜色
                    ),
                    yaxis=dict(
                        tickfont=dict(size=20, family='SimHei', color='black'),
                        linewidth=2,  # 设置y轴线条粗细
                        linecolor='black'  # 设置y轴线条颜色
                    ),
                    legend=dict(
                        x=0.1,  # 水平位置（0-1，1为最右侧）
                        y=1,  # 垂直位置（0-1，1为顶部）
                        bgcolor='rgba(255, 255, 255, 0.7)',  # 半透明背景
                        bordercolor='#ddd',
                        borderwidth=1,
                        font=dict(
                            size=20,  # 字体大小
                            color='#333',
                            family='SimHei',
                        ),
                        itemsizing='constant'  # 图例图标大小一致
                    ),
                    # 修改后的shapes设置
                    shapes=[
                        # 先添加红色虚线（确保它在边框上层）
                        dict(
                            type="line",
                            x0=0, x1=0,
                            y0=0, y1=1,
                            yref="paper",
                            line=dict(color="red", width=2, dash="dash"),
                            layer="above"  # 确保在顶层
                        ),
                        # 再添加黑色边框
                        dict(
                            type="rect",
                            xref="paper", yref="paper",
                            x0=-0.1, y0=-0.1,
                            x1=1.1, y1=1.1,
                            line=dict(color="black", width=2),
                            fillcolor="rgba(0,0,0,0)",
                            layer="below"  # 边框在底层
                        )
                    ]
                )

                fig.show()
            elif option == "间距不规则数据的等值线图":

                all_columns = df.columns.tolist()  # 替代原先的 numeric_columns
                #请选择x轴的变量
                x_col = st.selectbox("请选择x变量", all_columns,
                                      index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                y_col = st.selectbox("请选择y变量", all_columns,
                                      index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                z_col = st.selectbox("请选择z变量", all_columns,
                                      index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                # 数据预处理：去掉NaN值
                df_clean = df[[x_col, y_col, z_col]].dropna()

                # 提取数据
                x = df_clean[x_col].values
                y = df_clean[y_col].values
                z = df_clean[z_col].values

                # 创建图形和子图
                fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 12))


                # 创建网格
                ngridx, ngridy = 100, 100
                xi = np.linspace(x.min(), x.max(), ngridx)
                yi = np.linspace(y.min(), y.max(), ngridy)

                # 三角剖分和插值
                triang = tri.Triangulation(x, y)
                interpolator = tri.LinearTriInterpolator(triang, z)
                Xi, Yi = np.meshgrid(xi, yi)
                zi = interpolator(Xi, Yi)

                # 绘制等高线
                line_contour1 = ax1.contour(xi, yi, zi, levels=14, linewidths=0.1, colors='k')  # 线等高线
                cntr1 = ax1.contourf(xi, yi, zi, levels=14, cmap="plasma")  # 填充等高线

                ax1.clabel(line_contour1,
                           inline=True,
                           fontsize=8,
                           fmt='%.1f',
                           colors='k')
                fig.colorbar(cntr1, ax=ax1)
                ax1.set(xlim=(x.min(), x.max()), ylim=(y.min(), y.max()))
                ax1.set_title(f' Contour (x={x_col}, y={y_col}, z={z_col})')
                ax1.set_xlabel(x_col)
                ax1.set_ylabel(y_col)

                # -----------------------
                # 三角剖分方法 (ax2)
                # -----------------------
                line_contour2 =ax2.tricontour(x, y, z, levels=14, linewidths=0.1, colors='k')
                cntr2 = ax2.tricontourf(x, y, z, levels=14, cmap="plasma")
                ax2.clabel( line_contour2,
                           inline=True,
                           fontsize=8,
                           fmt='%.1f',
                           colors='k')  # 仅在此处设置字体

                fig.colorbar(cntr2, ax=ax2)
                ax2.set(xlim=(x.min(), x.max()), ylim=(y.min(), y.max()))
                ax2.set_title(f' Contour (x={x_col}, y={y_col}, z={z_col})')
                ax2.set_xlabel(x_col)
                ax2.set_ylabel(y_col)

                # 调整布局并显示
                plt.subplots_adjust(hspace=0.3)
                st.pyplot(fig)


            elif option == "重叠密度（“山脊图”）":
                sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
                #输入数据
                # 获取所有列（包括非数值列）
                all_columns = df.columns.tolist()  # 替代原先的 numeric_columns
                genre = st.radio(
                    "是否要进行norm='max'归一化处理",
                    ["是", "否", ],
                    index=None,
                )

                st.write("You selected:", genre)

                # 创建列选择器
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    title1 = st.selectbox("请选择第一个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col2:
                    title2 = st.selectbox("请选择第二个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                with col3:
                    title3 = st.selectbox("请选择第三个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col4:
                    title4 = st.selectbox("请选择第四个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                col11, col21, col31, col111 = st.columns(4)
                with col11:
                    title5 = st.selectbox("请选择第五个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col21:
                    title6 = st.selectbox("请选择第六个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                with col31:
                    title7 = st.selectbox("请选择第七个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col111:
                    title8 = st.selectbox("请选择第八个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                col1111, col1112, col31, col111 = st.columns(4)
                with col1111:
                    title9 = st.selectbox("请选择第九个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col1112:
                    title10 = st.selectbox("请选择第十个山脊图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比"))
                # 获取所有选择的列
                selected_columns = [title1, title2, title3, title4, title5, title6, title7, title8, title9, title10]
                if genre == "是":
                    scaler = StandardScaler()  # 使用标准化（Z-score）
                    df_standardized = df.copy()

                    for col in selected_columns:

                        col_data = df[[col]].values
                        df_standardized[col] = scaler.fit_transform(col_data)

                    df_to_use = df_standardized
                else:
                    df_to_use = selected_columns  # 使用原始数据
                # 准备山脊图数据（转换为长格式）
                ridge_data = pd.DataFrame()
                for col in selected_columns:
                    temp_df = pd.DataFrame({
                        'value': df_to_use[col],
                        'variable': col,
                        'group': selected_columns.index(col)  # 用于保持原始顺序
                    })
                    ridge_data = pd.concat([ridge_data, temp_df])

                # 绘制山脊图
                plt.figure(figsize=(10, 6))
                pal = sns.cubehelix_palette(len(selected_columns), rot=-.25, light=.7)
                g = sns.FacetGrid(ridge_data, row="variable", hue="variable", aspect=15, height=0.5, palette=pal)

                # 绘制密度曲线
                g.map(sns.kdeplot, "value",
                      bw_adjust=0.5, clip_on=False,
                      fill=True, alpha=1, linewidth=1.5)
                g.map(sns.kdeplot, "value", clip_on=False, color="w", lw=2, bw_adjust=0.5)

                # 添加参考线
                g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


                # 添加标签
                def label(x, color, label):
                    ax = plt.gca()
                    ax.text(0, 0.2, label, fontweight="bold", color=color,
                            ha="left", va="center", transform=ax.transAxes)


                g.map(label, "value")

                # 调整子图间距
                g.figure.subplots_adjust(hspace=-0.25)

                # 移除不必要的坐标轴元素
                g.set_titles("")
                g.set(yticks=[], ylabel="")
                g.despine(bottom=True, left=True)

                # 添加标题
                title_input = st.text_input("请输入图片名称", "山脊图")
                st.write("图片标题为", title_input)
                plt.suptitle(title_input, y=1.02)

                # 显示图表
                st.pyplot(g.fig)

            elif option == "小提琴图":

                fig = go.Figure()
                # 获取所有列（包括非数值列）
                all_columns = df.columns.tolist()  # 替代原先的 numeric_columns
                genre = st.radio(
                    "是否要进行norm='max'归一化处理",
                    ["是", "否",],
                    index=None,
                )

                st.write("You selected:", genre)


                # 创建列选择器
                col1,col2,col3, col4 = st.columns(4)
                with col1:
                    title1 = st.selectbox("请选择第一个小提琴图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col2:
                    title2 = st.selectbox("请选择第二个小提琴图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                with col3:
                    title3 = st.selectbox("请选择第三个小提琴图的结构设计参数", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col4:
                    title4 = st.selectbox("请选择第四个小提琴图的结构设计参数", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)
                # 对每一列单独处理
                cleaned_data = {}
                for i, col in enumerate([title1, title2, title3, title4], 1):

                    # 转换为数值类型
                    series = pd.to_numeric(df[col], errors='coerce')
                    # 去除缺失值
                    cleaned_series = series.dropna()
                    cleaned_data[f"df_clean{i}"] = cleaned_series


                # # 选择需要处理的两列,去除含有空格和文本的行
                # cols_to_check = [title1, title2,title3,title4]
                #
                # # 尝试将列转换为数值类型（无法转换的会变成NaN）
                # df[cols_to_check] = df[cols_to_check].apply(pd.to_numeric, errors='coerce')
                #
                # # 删除包含NaN的行
                # df_clean = df.dropna(subset=cols_to_check)
                # 转为NumPy数组（显式调用，推荐）
                array1 = cleaned_data["df_clean1"].to_numpy()  # 第1列数组
                array2 = cleaned_data["df_clean2"].to_numpy()  # 第2列数组
                array3 = cleaned_data["df_clean3"].to_numpy()  # 第3列数组
                array4 = cleaned_data["df_clean4"].to_numpy()  # 第4列数组

                colors = ['#1965B0', '#882E72', '#7BAFDE', ' #4EB265']  # 自定义颜色列表




                if genre =="是":
                    # 初始化scaler
                    scaler = MinMaxScaler()

                    # 对每个数组单独归一化并命名
                    array1_normalized = scaler.fit_transform(array1.reshape(-1, 1)).flatten()
                    array2_normalized = scaler.fit_transform(array2.reshape(-1, 1)).flatten()
                    array3_normalized = scaler.fit_transform(array3.reshape(-1, 1)).flatten()
                    array4_normalized = scaler.fit_transform(array4.reshape(-1, 1)).flatten()



                    for arr, title, color in zip([array1_normalized, array2_normalized, array3_normalized, array4_normalized],[title1, title2, title3, title4],colors):
                        fig.add_trace(go.Violin(x=[title] * len(arr),  # X轴数据，重复列名以匹配Y轴数据的长度
                                                y=arr,  # Y轴数据，这里是数组arr的所有值
                                                name=title,  # 图例名称，对应数组的名称
                                                box_visible=True,
                                                meanline_visible=True,
                                                # fillcolor=color
                                                ))
                    # 调整布局
                    fig.update_layout(
                        # 调整图例
                        legend=dict(
                            font=dict(
                                size=24,  # 图例文字大小
                                family="SimHei"   # 字体
                            ),
                            title_font=dict(
                                size=24,  # 图例标题大小（如果有）
                                family="SimHei"
                            ),
                            itemsizing='constant',  # 图例项大小一致
                            traceorder='normal',  # 图例顺序
                        ),

                        # 调整X轴
                        xaxis=dict(
                            title_font=dict(size=24),  # X轴标题大小
                            tickfont=dict(size=24)  # X轴刻度数字大小
                        ),

                        # 调整Y轴
                        yaxis=dict(
                            title_font=dict(size=24),  # Y轴标题大小
                            tickfont=dict(size=24)  # Y轴刻度数字大小
                        ),

                        # 整体字体设置（可选）
                        font=dict(
                            family="SimHei",
                            size=24
                        )
                    )

                    fig.show()
                elif genre =="否":
                    array1_normalized = array1
                    array2_normalized = array2
                    array3_normalized = array3
                    array4_normalized = array4

                    for arr, col in zip([array1, array2, array3, array4], ['col1', 'col2', 'col3', 'col4']):
                        fig.add_trace(go.Violin(x=[col] * len(arr),  # X轴数据，重复列名以匹配Y轴数据的长度
                                                y=arr,  # Y轴数据，这里是数组arr的所有值
                                                name=col,  # 图例名称，对应数组的名称
                                                box_visible=True,
                                                meanline_visible=True))

                    fig.show()

            elif option == "散点频率图":

                # 生成示例数据
                x1 = np.random.normal(loc=5.0, size=400) * 100
                y1 = np.random.normal(loc=10.0, size=400) * 10

                x2 = np.random.normal(loc=5.0, size=800) * 50
                y2 = np.random.normal(loc=5.0, size=800) * 10

                x3 = np.random.normal(loc=55.0, size=200) * 10
                y3 = np.random.normal(loc=4.0, size=200) * 10

                x = np.concatenate((x1, x2, x3))
                y = np.concatenate((y1, y2, y3))

                # 创建ColumnDataSource
                source = ColumnDataSource(data=dict(x=x, y=y))
                source_selected = ColumnDataSource(data=dict(x=[], y=[]))
                source_unselected = ColumnDataSource(data=dict(x=[], y=[]))

                # 工具设置
                TOOLS = "pan,wheel_zoom,box_select,lasso_select,reset"

                # 创建主散点图
                p = figure(tools=TOOLS, width=600, height=600, min_border=10, min_border_left=50,
                           toolbar_location="above", title="Linked Histograms")
                p.background_fill_color = "#fafafa"
                p.select(BoxSelectTool).select_every_mousemove = False
                p.select(LassoSelectTool).select_every_mousemove = False

                r = p.scatter('x', 'y', source=source, size=3, color="#3A5785", alpha=0.6)

                # 创建水平直方图
                hhist, hedges = np.histogram(x, bins=20)
                hzeros = np.zeros(len(hedges) - 1)
                hmax = max(hhist) * 1.1

                LINE_ARGS = dict(color="#3A5785", line_color=None)

                ph = figure(toolbar_location=None, width=p.width, height=200, x_range=p.x_range,
                            y_range=(-hmax, hmax), min_border=10, min_border_left=50, y_axis_location="right")
                ph.xgrid.grid_line_color = None
                ph.yaxis.major_label_orientation = np.pi / 4
                ph.background_fill_color = "#fafafa"

                ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white",
                        line_color="#3A5785")
                hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
                hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)

                # 创建垂直直方图
                vhist, vedges = np.histogram(y, bins=20)
                vzeros = np.zeros(len(vedges) - 1)
                vmax = max(vhist) * 1.1

                pv = figure(toolbar_location=None, width=200, height=p.height, x_range=(-vmax, vmax),
                            y_range=p.y_range, min_border=10, y_axis_location="right")
                pv.ygrid.grid_line_color = None
                pv.xaxis.major_label_orientation = np.pi / 4
                pv.background_fill_color = "#fafafa"

                pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white",
                        line_color="#3A5785")
                vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
                vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)


                # 定义更新函数
                def update(attr, old, new):
                    inds = new
                    if len(inds) == 0 or len(inds) == len(x):
                        hhist1, hhist2 = hzeros, hzeros
                        vhist1, vhist2 = vzeros, vzeros
                    else:
                        neg_inds = np.ones_like(x, dtype=bool)
                        neg_inds[inds] = False
                        hhist1, _ = np.histogram(x[inds], bins=hedges)
                        vhist1, _ = np.histogram(y[inds], bins=vedges)
                        hhist2, _ = np.histogram(x[neg_inds], bins=hedges)
                        vhist2, _ = np.histogram(y[neg_inds], bins=vedges)

                    hh1.data_source.data["top"] = hhist1
                    hh2.data_source.data["top"] = -hhist2
                    vh1.data_source.data["right"] = vhist1
                    vh2.data_source.data["right"] = -vhist2


                # 设置选择回调
                r.data_source.selected.on_change('indices', update)

                # 创建布局
                layout = gridplot([[p, pv], [ph, None]], merge_tools=False)

                # 在Streamlit中展示
                st.bokeh_chart(layout, use_container_width=True)

            elif option == "散点图":
                # 1. 先获取清洗后的数据
                all_columns = df.columns.tolist()

                # 创建双列布局
                col1, col2 = st.columns(2)
                with col1:
                    title1 = st.selectbox("请选择x轴的列", all_columns,
                                          index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0)
                with col2:
                    title2 = st.selectbox("请选择y轴的列", all_columns,
                                          index=all_columns.index("压缩比") if "压缩比" in all_columns else 0)

                # 2. 立即执行数据清洗（关键修改点！）
                cols_to_check = [title1, title2]
                df_clean = df.copy()
                df_clean[cols_to_check] = df_clean[cols_to_check].apply(pd.to_numeric, errors='coerce')
                df_clean = df_clean.dropna(subset=cols_to_check)

                # 检查有效数据量
                if len(df_clean) == 0:
                    st.error("错误：选择的两列没有有效的数值数据！")
                    st.stop()  # 停止执行后续代码

                # 3. 创建Bokeh数据源（关键修改点！）
                source = ColumnDataSource(df_clean)

                # 悬停提示工具
                hover = HoverTool(
                    tooltips=[
                        (f"{title1}", f"@{title1}"),  # 使用列名引用
                        (f"{title2}", f"@{title2}"),
                        ("索引", "@index")
                    ]
                )

                # 创建图表对象
                p = figure(
                    width=800,
                    height=400,
                    tools=[hover, "pan,wheel_zoom,box_zoom,reset"],
                    title=f"{title2} 随 {title1} 的变化趋势",
                    x_axis_label=title1,
                    y_axis_label=title2
                )

                # 4. 使用ColumnDataSource绘制散点图（关键修改点！）
                p.scatter(
                    x=title1,
                    y=title2,
                    source=source,
                    size=10,
                    fill_color="steelblue",
                    alpha=0.6,
                    line_color="white",
                    line_width=1,
                    hover_fill_color="firebrick",
                    hover_alpha=0.8,
                    hover_line_color="white"
                )

                # 5. 更安全的趋势线添加方式
                if len(df_clean) >= 2:  # 至少需要2个点才能绘制趋势线
                    try:
                        x_vals = df_clean[title1].values
                        y_vals = df_clean[title2].values
                        coef = np.polyfit(x_vals, y_vals, 1)
                        trendline = np.poly1d(coef)
                        p.line(x_vals, trendline(x_vals),
                               color='red',
                               line_width=2,
                               legend_label="趋势线")
                    except Exception as e:
                        st.warning(f"趋势线添加失败: {str(e)}")

                # 图表美化
                p.grid.visible = True
                p.grid.grid_line_color = "lightgray"
                p.grid.grid_line_alpha = 0.5
                p.legend.location = "top_left"
                p.legend.click_policy = "hide"
                p.toolbar.autohide = True  # 自动隐藏工具栏

                # 最终显示
                st.bokeh_chart(p, use_container_width=True)

            elif option == "二维散点图":
                all_columns = df.columns.tolist()


                all_columns = df.columns.tolist()  # 获取所有列名

                # 1. 让用户选择3个参数（使用3列布局）
                col1, col2, col3 = st.columns(3)

                with col1:
                    x_col = st.selectbox(
                        "X轴数据",
                        all_columns,
                        index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0
                    )
                with col2:
                    y_col = st.selectbox(
                        "Y轴数据",
                        all_columns,
                        index=all_columns.index("压缩比") if "压缩比" in all_columns else 0
                    )
                with col3:
                    z_col = st.selectbox(
                        "颜色数据（Z轴）",
                        all_columns,
                        index=all_columns.index("效率") if "效率" in all_columns else 0
                    )

                # 2. 检查列名是否有效
                selected_columns = [x_col, y_col, z_col]
                filtered_df = df[[x_col, y_col, z_col]].dropna()





                # 4. 提取数据（确保过滤后的 DataFrame 非空）
                if not filtered_df.empty:
                    x_data = filtered_df[x_col]
                    y_data = filtered_df[y_col]
                    z_data = filtered_df[z_col]

                    # 这里可以继续你的绘图代码
                    st.success("数据过滤完成！")
                else:
                    st.warning("过滤后无有效数据，请检查原始数据或列选择！")
                # 2. 绘制散点图

                fig, ax = plt.subplots()



                # 创建散点图
                sc = ax.scatter(x_data, y_data, c=z_data, cmap='viridis')

                # 设置标签
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)

                # 添加颜色条
                cbar = fig.colorbar(sc)
                cbar.set_label(z_col)

                # 显示图形
                st.pyplot(fig)
            elif option == "三维散点图":

                all_columns = df.columns.tolist()

                col1, col2, col3,col4 = st.columns(4)

                with col1:
                    x_col = st.selectbox(
                        "X轴数据",
                        all_columns,
                        index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0
                    )
                with col2:
                    y_col = st.selectbox(
                        "Y轴数据",
                        all_columns,
                        index=all_columns.index("压缩比") if "压缩比" in all_columns else 0
                    )
                with col3:
                    z_col = st.selectbox(
                        "Z轴",
                        all_columns,
                        index=all_columns.index("效率") if "效率" in all_columns else 0
                    )
                with col4:
                    m_col = st.selectbox(
                        "颜色数据",
                        all_columns,
                        index=all_columns.index("效率") if "效率" in all_columns else 0
                    )
                # 2. 检查列名是否有效
                selected_columns = [x_col, y_col, z_col,m_col]
                filtered_df = df[[x_col, y_col, z_col,m_col]].dropna()

                # 4. 提取数据（确保过滤后的 DataFrame 非空）
                if not filtered_df.empty:
                    x_data = filtered_df[x_col]
                    y_data = filtered_df[y_col]
                    z_data = filtered_df[z_col]
                    m_data = filtered_df[m_col]
                    # 这里可以继续你的绘图代码
                    st.success("数据过滤完成！")
                else:
                    st.warning("过滤后无有效数据，请检查原始数据或列选择！")



                fig = plt.figure(figsize=(10, 7))
                ax = fig.add_subplot(111, projection='3d')

                # 固定散点大小（示例值为50，可根据需要调整）
                fixed_size = 100

                # 绘制带发光效果的散点（通过叠加多层实现）
                # 核心散点（带黑色边缘线）
                scatter = ax.scatter(
                    x_data, y_data, z_data,
                    c=m_data,
                    cmap='viridis',
                    s=fixed_size,  # 固定大小
                    alpha=0.8,  # 核心散点透明度
                    edgecolors='black',  # 黑色边缘线
                    linewidths=1  # 边缘线宽度
                )

                # 发光层（3层半透明散点，逐渐放大）
                # 削弱后的发光层
                glow_sizes = [fixed_size * 1.2, fixed_size * 1.5]
                glow_alphas = [0.03, 0.01]

                for size, alpha in zip(glow_sizes, glow_alphas):
                    ax.scatter(
                        x_data, y_data, z_data,
                        c=m_data,
                        cmap='viridis',
                        s=size,
                        alpha=alpha,
                        edgecolors='none',
                        zorder=1
                    )

                # 交互式输入标签
                titlex1 = st.text_input("请输入图表名称", "3D Scatter Plot")
                titlex2 = st.text_input("请输入X轴名称", "compressor speed (RPM)")
                titlex3 = st.text_input("请输入Y轴名称", "Air Mass Flow Rate(g/s)")
                titlex4 = st.text_input("请输入Z轴名称", "compressor pressure ratio")
                titlex5 = st.text_input("请输入颜色条名称", "Number of blades")

                # 添加颜色条
                cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
                cbar.set_label(titlex5, fontsize=15)

                # 设置标签和美化
                ax.set_xlabel(titlex2, fontsize=15)
                ax.set_ylabel(titlex3, fontsize=15)
                ax.set_zlabel(titlex4, fontsize=15)
                ax.set_title(titlex1, fontsize=25, pad=20)
                # 设置刻度标签字号
                ax.tick_params(axis='x', labelsize=15)  # X轴刻度字号12
                ax.tick_params(axis='y', labelsize=15)  # Y轴刻度
                ax.tick_params(axis='z', labelsize=15)  # Z轴刻度
                # 设置刻度标签字号
                cbar.ax.tick_params(labelsize=15)  # 刻度数字字号
                # 坐标平面半透明化
                ax.xaxis.set_pane_color((0.95, 0.95, 0.95, 0.1))
                ax.yaxis.set_pane_color((0.95, 0.95, 0.95, 0.1))
                ax.zaxis.set_pane_color((0.95, 0.95, 0.95, 0.1))

                fig.patches.extend([
                    Rectangle(
                        (0, 0), 1, 1,  # 覆盖整个图形区域
                        transform=fig.transFigure,
                        fill=False,
                        edgecolor='black',
                        linewidth=1,  # 边框粗细
                        zorder=100  # 确保在最上层
                    )
                ])
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()  # 避免重复显示
                st.pyplot(fig)
                plt.show()




with tabs[2]:
    image1 = Image.open("pic/1.png")  # 替换为您的图片路径
    st.image(image1, width=1200)
    image2= Image.open("pic/2.png")  # 替换为您的图片路径
    st.image(image2, width=1200)
    image3 = Image.open("pic/3.png")  # 替换为您的图片路径
    st.image(image3, width=1200)
    image4 = Image.open("pic/4.png")  # 替换为您的图片路径
    st.image(image4, width=1200)
    image5 = Image.open("pic/5.png")  # 替换为您的图片路径
    st.image(image5, width=1200)
    image6 = Image.open("pic/6.png")  # 替换为您的图片路径
    st.image(image6, width=1200)
    image7 = Image.open("pic/7.png")  # 替换为您的图片路径
    st.image(image7, width=1200)
    image8 = Image.open("pic/8.png")  # 替换为您的图片路径
    st.image(image8, width=1200)
    image9 = Image.open("pic/9.png")  # 替换为您的图片路径
    st.image(image9, width=1200)
    image10 = Image.open("pic/10.png")  # 替换为您的图片路径
    st.image(image10, width=1200)
    image11 = Image.open("pic/11.png")  # 替换为您的图片路径
    st.image(image11, width=1200)
    image12 = Image.open("pic/12.png")  # 替换为您的图片路径
    st.image(image12, width=1200)
    image13 = Image.open("pic/13.png")  # 替换为您的图片路径
    st.image(image13, width=1200)
    image14 = Image.open("pic/14.png")  # 替换为您的图片路径
    st.image(image14, width=1200)
    image15 = Image.open("pic/15.png")  # 替换为您的图片路径
    st.image(image15, width=1200)
    image16 = Image.open("pic/16.png")  # 替换为您的图片路径
    st.image(image16, width=1200)
    image17 = Image.open("pic/17.png")  # 替换为您的图片路径
    st.image(image17, width=1200)
    image18 = Image.open("pic/18.png")  # 替换为您的图片路径
    st.image(image18, width=1200)
    image19 = Image.open("pic/19.png")  # 替换为您的图片路径
    st.image(image19, width=1200)
    image20 = Image.open("pic/20.png")  # 替换为您的图片路径
    st.image(image20, width=1200)
    image21 = Image.open("pic/21.png")  # 替换为您的图片路径
    st.image(image21, width=1200)
    image22 = Image.open("pic/22.png")  # 替换为您的图片路径
    st.image(image22, width=1200)
    image23 = Image.open("pic/23.png")  # 替换为您的图片路径
    st.image(image23, width=1200)
    image24 = Image.open("pic/24.png")  # 替换为您的图片路径
    st.image(image24, width=1200)
    image25 = Image.open("pic/25.png")  # 替换为您的图片路径
    st.image(image25, width=1200)
    image26 = Image.open("pic/26.png")  # 替换为您的图片路径
    st.image(image26, width=1200)
    image27 = Image.open("pic/27.png")  # 替换为您的图片路径
    st.image(image27, width=1200)
    image28 = Image.open("pic/28.png")  # 替换为您的图片路径
    st.image(image28, width=1200)
    image29 = Image.open("pic/29.png")  # 替换为您的图片路径
    st.image(image29, width=1200)



with tabs[3]:
    # elif st.session_state.selected == 'AI对话':
    # Show title and description.
    # 显示标题和描述
    st.title("💬 DeepSeek")
    st.write(
        "这是一个简单的聊天机器人，它使用 DeepSeek 的 DeepSeek-V3-0324 模型来生成响应。 "
        "要使用此应用程序，您需要提供一个 DeepSeek API 密钥，您可以在此处获取(https://platform.deepseek.com/api_keys). "
    )
    api_key= st.chat_input("请输入DeepSeek API 密钥")
    # 初始化客户端和会话状态
    client = OpenAI(api_key=api_key,
                    base_url="https://api.deepseek.com/v1")  # 注意添加/v1
    # api_key = "sk-d571ccc1d36942a7a937e14ecd7cb535"
    # 初始化消息历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])  # 使用markdown更好显示格式

    # 聊天输入
    if prompt := st.chat_input("Say something"):
        # 添加用户消息到历史并显示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages
        )

        # 获取AI回复内容
        ai_response = response.choices[0].message.content

        # 添加AI回复到历史并显示
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)

        # 调试打印(可选)
        st.write(f"Tokens used: {response.usage.total_tokens}")

with tabs[4]:
# elif st.session_state.selected == '操作示例':
    st.write("这是操作示例页面")
    image1 = Image.open("pic/30.png")  # 替换为您的图片路径
    st.image(image1, width=1200)
    image2= Image.open("pic/31.png")  # 替换为您的图片路径
    st.image(image2, width=1200)
    image3 = Image.open("pic/32.png")  # 替换为您的图片路径
    st.image(image3, width=1200)
    image4 = Image.open("pic/33.png")  # 替换为您的图片路径
    st.image(image4, width=1200)

