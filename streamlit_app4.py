import streamlit as st
import matplotlib.tri as tri
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import plotly.graph_objects as go
from bokeh.models import HoverTool
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
from bokeh.plotting import figure
from bokeh.sampledata.penguins import data as bokeh_penguins_data
from bokeh.transform import factor_cmap, factor_mark
from openai import OpenAI

# ---- FONT SETUP FOR MATPLOTLIB ----
matplotlib.rc("font", family='YouYuan')
font_msg = "Using 'YouYuan' font as default."
print(font_msg)  # For logs
plt.rcParams['axes.unicode_minus'] = False  # Correctly display minus sign
# ---- END FONT SETUP ----

# Add global CSS for background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #08103f;
    }
    .stApp * {
        color: white !important;
    }
    .stContainer {
        background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'selected' not in st.session_state:
    st.session_state.selected = None

# HTML code
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title></title>
    <style>
        * {-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}
        *, body {padding: 0px;margin: 0px;color: white;font-family: "微软雅黑", "YouYuan", sans-serif;}
        @font-face {font-family: electronicFont;src: url(https://example.com/font/DS-DIGIT.TTF);}
        body {background: #08103f url(https://example.com/images/bg.jpg) center top;background-size: cover;color: #666;font-size: 0.1rem;line-height: 1.3;}
        li {list-style-type: none;}
        #MainMenu {width: 100%; padding: 20px; margin-top:-50px;margin-left: -350px;margin-bottom: 10px;}
        .st-container {width: 100%; padding: 20px; margin-top:-50px;margin-left: -350px;margin-bottom: 10px;}
        .title {font-size: 32px; text-align: left;margin-top:-50px;margin-left: -350px;margin-bottom: 10px;padding: 0;color: white;}
        .canvas{position: relative; width:100%; min-height: 0vh; z-index: auto;}
        .stTabs {width:1400px; margin-left; margin-top:-40px;margin-left: -350px;color: white;}
        .stExpander {width: 1000px; margin: auto; color: white;}
    </style>
</head>
<body>
    <div class="canvas">
    <h1 class="title">氢燃料电池发动机系统空压机大数据平台</h1>
    </div>
    <div class="canvas mainbox" id="streamlit-container">
    </div>
</body>
</html>
"""

st.markdown(html_code, unsafe_allow_html=True)

# Create tabs
tabs = st.tabs(["首页", "数据分析", "趋势分析", "AI对话", "操作示例"])

with tabs[0]:
    left, middle, right = st.columns([2.5, 5, 2.5])

    with left:
        row1 = st.columns(1)
        row2 = st.columns(1)

        with row1[0]:
            tile = st.container(height=270, border=True)
            with tile:
                st.markdown(
                    """
                    <style>
                    .custom-container {
                        width: 300px;
                        height: 30px;
                        background: linear-gradient(45deg, #191c83, transparent);
                        padding: 10px;
                        margin: 0;
                    }
                    .title1 {font-size: 17px; text-align: left; margin: 0; padding: 0; color: white;}
                    .stContainer {border: 2px solid white; padding: 5px; background-color: #08103f;}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="custom-container">
                        <h2 class="title1">数据库介绍</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <p style="font-size:15px; color:white;">
                        <strong>本数据库包含氢燃料电池发动机系统空压机结构参数、性能指标等信息。平台用于研究在燃料电池电堆空压机设计研发过程中遇到的空压机结构设计匹配问题。利用大数据分析和机器学习，辅助河北金士顿有限公司空压机进行结构设计和大数据性能分析，辅助其完成数据检索，基于机器学习工具，训练空压机结构同性能间的关系，为燃料电池电堆空压机的设计提供理论指导。</strong>
                    </p>
                    """,
                    unsafe_allow_html=True
                )

        with row2[0]:
            tile1 = st.container(height=270, border=True)
            with tile1:
                st.markdown(
                    """
                    <style>
                    .custom-container1 {
                        width: 300px;
                        height: 30px;
                        background: linear-gradient(45deg, #191c83, transparent);
                        padding: 10px;
                        margin: 0 0 5px 0;
                    }
                    .title12 {font-size: 17px; text-align: left; margin: 0; padding: 0; color: white;}
                    .stContainer {border: 2px solid white; padding: 5px; background-color: #08103f;}
                    .altair-viz {background-color: #08103f !important;}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="custom-container1">
                        <h1 class="title12">数据库数据详情</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                x1, x2, x3, x4 = np.random.randn(200) - 2, np.random.randn(200), np.random.randn(200) + 2, np.random.randn(200) + 4
                hist_data = [x1, x2, x3, x4]
                group_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
                colors = ['#70C7F3', '#00F5FF', '#C724F1', '#00FFA3']
                fig1 = ff.create_distplot(hist_data, group_labels, colors=colors, bin_size=0.2)
                fig1.update_layout(
                    height=230, margin=dict(l=20, r=20, t=0, b=20),
                    plot_bgcolor='#08103f', paper_bgcolor='#08103f',
                    font_color='white', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
                )
                st.plotly_chart(fig1, use_container_width=True)

    with middle:
        row1 = st.columns(1)
        with row1[0]:
            tile50 = st.container(height=560, border=True)
            with tile50:
                st.markdown(
                    """
                    <style>
                    .custom-container2 {
                        width: 500px;
                        height: 30px;
                        background: linear-gradient(45deg, #191c83, transparent);
                        padding: 10px;
                        margin: 0;
                    }
                    .title13 {font-size: 17px; text-align: left; margin: 0; padding: 0; color: white;}
                    .stContainer {border: 2px solid white; padding: 5px; background-color: #08103f;}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="custom-container2">
                        <h1 class="title13">氢燃料电池发动机系统空压机性能总览图</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                df011 = pd.read_excel('./data1/data1.xlsx', usecols=[61], header=None, skiprows=137, nrows=53)
                df012 = pd.read_excel('./data1/data1.xlsx', usecols=[61], header=None, skiprows=437, nrows=17)
                df013 = pd.read_excel('./data1/data1.xlsx', usecols=[61], header=None, skiprows=521, nrows=50)
                df021 = pd.read_excel('./data1/data1.xlsx', usecols=[60], header=None, skiprows=137, nrows=53)
                df022 = pd.read_excel('./data1/data1.xlsx', usecols=[60], header=None, skiprows=437, nrows=17)
                df023 = pd.read_excel('./data1/data1.xlsx', usecols=[60], header=None, skiprows=521, nrows=50)
                df031 = pd.read_excel('./data1/data1.xlsx', usecols=[70], header=None, skiprows=137, nrows=53)
                df032 = pd.read_excel('./data1/data1.xlsx', usecols=[70], header=None, skiprows=437, nrows=17)
                df033 = pd.read_excel('./data1/data1.xlsx', usecols=[70], header=None, skiprows=521, nrows=50)
                df01 = pd.concat([df011, df012, df013], ignore_index=True).squeeze()
                df02 = pd.concat([df021, df022, df023], ignore_index=True).squeeze()
                df03 = pd.concat([df031, df032, df033], ignore_index=True).squeeze()
                fig = go.Figure(data=[go.Scatter3d(
                    x=df01, y=df02, z=df03, mode='markers',
                    marker=dict(size=12, color=df03, colorscale='Viridis', opacity=0.8)
                )])
                fig.update_layout(
                    scene=dict(zaxis=dict(showbackground=False, title="等熵效率", color="white"),
                               xaxis=dict(title="转速r/min", color="white"),
                               yaxis=dict(title="质量流量g/s", color="white"),
                               aspectmode="manual", aspectratio=dict(x=2, y=1, z=0.5)),
                    width=500, height=450, margin=dict(l=0, r=0, b=0, t=0),
                    template="plotly_dark", plot_bgcolor='#08103f', paper_bgcolor='#08103f'
                )
                st.plotly_chart(fig, use_container_width=True, height=450)

    with right:
        row1 = st.columns(1)
        with row1[0]:
            tile = st.container(height=270, border=True)
            with tile:
                st.markdown(
                    """
                    <style>
                    .custom-container3 {
                        width: 300px;
                        height: 30px;
                        background: linear-gradient(45deg, #191c83, transparent);
                        padding: 10px;
                        margin: 0 0 5px 0;
                    }
                    .title5 {font-size: 17px; text-align: left; margin: 0; padding: 0; color: white;}
                    .stContainer {border: 2px solid white; padding: 5px;}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="custom-container3">
                        <h1 class="title5">数据库结构设计参数</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                SPECIES = sorted(bokeh_penguins_data.species.unique())
                MARKERS = ['hex', 'circle_x', 'triangle']
                p_bokeh = figure(
                    title="", tools="hover,reset", background_fill_color=None, border_fill_color=None,
                    height=200, width=300, sizing_mode="scale_width"
                )
                p_bokeh.scatter("flipper_length_mm", "body_mass_g", source=bokeh_penguins_data, size=5, fill_alpha=0.2, line_alpha=0, color=factor_cmap('species', 'Category10_3', SPECIES))
                p_bokeh.scatter("flipper_length_mm", "body_mass_g", source=bokeh_penguins_data, fill_alpha=0.6, size=5, line_width=0.5, line_color="black", marker=factor_mark('species', MARKERS, SPECIES), color=factor_cmap('species', 'Category10_3', SPECIES))
                p_bokeh.xaxis.axis_label = None
                p_bokeh.yaxis.axis_label = None
                p_bokeh.xaxis.axis_label_text_color = "white"
                p_bokeh.yaxis.axis_label_text_color = "white"
                p_bokeh.title.text_color = "white"
                p_bokeh.xgrid.grid_line_color = "#555555"
                p_bokeh.ygrid.grid_line_color = "#555555"
                p_bokeh.axis.major_tick_line_color = "white"
                p_bokeh.axis.minor_tick_line_color = "white"
                p_bokeh.axis.major_label_text_color = "white"
                p_bokeh.toolbar.logo = None
                p_bokeh.min_border_left = 0
                p_bokeh.min_border_right = 0
                p_bokeh.min_border_top = 0
                p_bokeh.min_border_bottom = 0
                st.bokeh_chart(p_bokeh, use_container_width=True)

        with st.container(height=270, border=True):
            st.markdown(
                """
                <style>
                .custom-container11 {
                    width: 300px;
                    height: 30px;
                    background: linear-gradient(45deg, #191c83, transparent);
                    padding: 10px;
                    margin: 0;
                }
                .title6 {font-size: 17px; text-align: left; margin: 0; padding: 0; color: white;}
                .stContainer {border: 2px solid white; padding: 5px;}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div class="custom-container11">
                    <h1 class="title6">数据库数据类型</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            excel_file_path = './data1/data1.xlsx'
            df_db_types = pd.DataFrame(columns=["论文类型", "数据类型"])
            data_load_success = False
            try:
                actual_cols_to_read = ["论文类型", "Unnamed: 2"]
                df_temp = pd.read_excel(excel_file_path, usecols=actual_cols_to_read)
                df_temp.rename(columns={"Unnamed: 2": "数据类型"}, inplace=True)
                df_db_types = df_temp
                data_load_success = True
            except Exception as e:
                st.error(f"Error loading data for pie charts: {e}")
                pass
            paper_labels_all, paper_values_all = [], []
            data_type_labels_all, data_type_values_all = [], []
            if data_load_success:
                if "论文类型" in df_db_types.columns and not df_db_types["论文类型"].dropna().empty:
                    paper_type_counts = df_db_types["论文类型"].dropna().value_counts()
                    paper_labels_all = paper_type_counts.index.tolist()
                    paper_values_all = paper_type_counts.values.tolist()
                if "数据类型" in df_db_types.columns and not df_db_types["数据类型"].dropna().empty:
                    data_type_counts = df_db_types["数据类型"].dropna().value_counts()
                    data_type_labels_all = data_type_counts.index.tolist()
                    data_type_values_all = data_type_counts.values.tolist()

            if data_load_success:
                pie_col1, pie_col2 = st.columns(2)
                chart_font_color = 'white'
                donut_hole_color = '#0d1e56'

                with pie_col1:
                    if paper_labels_all and paper_values_all:
                        fig_paper, ax_paper = plt.subplots(figsize=(2.8, 2.8))
                        fig_paper.patch.set_alpha(0.0)
                        ax_paper.patch.set_alpha(0.0)
                        sorted_paper_data = sorted(zip(paper_values_all, paper_labels_all), reverse=True)
                        sorted_paper_values = [data[0] for data in sorted_paper_data]
                        sorted_paper_labels = [data[1] for data in sorted_paper_data]
                        paper_colors = sns.color_palette("Blues_r", len(sorted_paper_labels))

                        pie_textprops = {'fontsize': 10, 'color': 'white'}

                        wedges, texts, autotexts = ax_paper.pie(
                            sorted_paper_values,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=paper_colors,
                            pctdistance=0.85,
                            textprops=pie_textprops,
                            wedgeprops=dict(width=0.4, edgecolor=donut_hole_color)
                        )
                        for autotext_item in autotexts:
                            autotext_item.set_color('black' if sum(paper_colors[autotexts.index(autotext_item)][:3]) / 3 > 0.6 else 'white')

                        if sorted_paper_labels:
                            center_label_paper = sorted_paper_labels[0]
                            center_value_paper = (sorted_paper_values[0] / sum(sorted_paper_values)) * 100 if sum(sorted_paper_values) > 0 else 0
                            text_args_center = {'ha': 'center', 'va': 'center', 'color': chart_font_color, 'weight': 'bold'}
                            ax_paper.text(0, 0.1, f"{center_label_paper}", fontsize=12, **text_args_center)
                            ax_paper.text(0, -0.15, f"{center_value_paper:.1f}%", fontsize=14, **text_args_center)

                        ax_paper.axis('equal')
                        if len(sorted_paper_labels) > 1:
                            legend_labels_list = [f"{sorted_paper_labels[i]}" for i in range(1, min(len(sorted_paper_labels), 4))]
                            legend_wedges_list = wedges[1:min(len(wedges), 4)]
                            if legend_labels_list:
                                legend_font_properties = {'size': 10}
                                ax_paper.legend(legend_wedges_list, legend_labels_list,
                                                loc="lower center", bbox_to_anchor=(0.5, -0.25),
                                                labelcolor=chart_font_color, facecolor='none', edgecolor='none', ncol=2,
                                                prop=legend_font_properties)
                        st.pyplot(fig_paper, use_container_width=True)
                    else:
                        st.markdown("<p style='color:white; text-align:center; font-size:12px; margin-top: 50px;'>No paper type data</p>", unsafe_allow_html=True)

                with pie_col2:
                    if data_type_labels_all and data_type_values_all:
                        fig_data, ax_data = plt.subplots(figsize=(2.8, 2.8))
                        fig_data.patch.set_alpha(0.0)
                        ax_data.patch.set_alpha(0.0)
                        sorted_data_type_data = sorted(zip(data_type_values_all, data_type_labels_all), reverse=True)
                        sorted_data_type_values = [data[0] for data in sorted_data_type_data]
                        sorted_data_type_labels = [data[1] for data in sorted_data_type_data]
                        data_type_colors = sns.color_palette("Greens_r", len(sorted_data_type_labels))

                        pie_textprops_data = {'fontsize': 10, 'color': 'white'}

                        wedges_data, texts_data, autotexts_data = ax_data.pie(
                            sorted_data_type_values,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=data_type_colors,
                            pctdistance=0.85,
                            textprops=pie_textprops_data,
                            wedgeprops=dict(width=0.4, edgecolor=donut_hole_color)
                        )
                        for autotext_item in autotexts_data:
                            autotext_item.set_color('black' if sum(data_type_colors[autotexts_data.index(autotext_item)][:3]) / 3 > 0.6 else 'white')

                        if sorted_data_type_labels:
                            center_label_data = sorted_data_type_labels[0]
                            center_value_data = (sorted_data_type_values[0] / sum(sorted_data_type_values)) * 100 if sum(sorted_data_type_values) > 0 else 0
                            text_args_center_data = {'ha': 'center', 'va': 'center', 'color': chart_font_color, 'weight': 'bold'}
                            ax_data.text(0, 0.1, f"{center_label_data}", fontsize=12, **text_args_center_data)
                            ax_data.text(0, -0.15, f"{center_value_data:.1f}%", fontsize=14, **text_args_center_data)

                        ax_data.axis('equal')
                        if len(sorted_data_type_labels) > 1:
                            legend_labels_list_2 = [f"{sorted_data_type_labels[i]}" for i in range(1, min(len(sorted_data_type_labels), 4))]
                            legend_wedges_list_2 = wedges_data[1:min(len(wedges_data), 4)]
                            if legend_labels_list_2:
                                legend_font_properties_data = {'size': 10}
                                ax_data.legend(legend_wedges_list_2, legend_labels_list_2,
                                               loc="lower center", bbox_to_anchor=(0.5, -0.25),
                                               labelcolor=chart_font_color, facecolor='none', edgecolor='none', ncol=2,
                                               prop=legend_font_properties_data)
                        st.pyplot(fig_data, use_container_width=True)
                    else:
                        st.markdown("<p style='color:white; text-align:center; font-size:12px; margin-top: 50px;'>No data type data</p>", unsafe_allow_html=True)

with tabs[1]:
    left1, middle2, middle1 = st.columns([0.3, 0.1, 0.7])

    with left1:
        st.markdown(
            """
            <style>
            .custom-container6 {
                width: 370px;
                height: 30px;
                background: linear-gradient(45deg, #191c83, transparent);
                padding: 10px;
                margin-top:-10px;margin-left: 0px;
            }
            .title7 {font-size: 25px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="custom-container6">
            <h1 class="title1">数据录入</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("上传CSV或Excel文件进行分析", type=["csv", "xlsx"], key="data_analysis_uploader")
        df = None
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, header=2)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, header=2, engine='openpyxl')
            st.write("上传的文件数据：")
            st.dataframe(df)

    with middle1:
        tile11 = st.container(height=560, border=True)
        with tile11:
            st.markdown(
                """
                <style>
                .custom-container7 {
                    width: 500px;
                    height: 30px;
                    background: linear-gradient(45deg, #191c83, transparent);
                    padding: 10px;
                    margin-top:-10px;margin-left: 0px;
                }
                .title8 {font-size: 17px; text-align: left;margin-top:-6px;margin-left: 30px;padding: 0;color: white;}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div class="custom-container1">
                <h1 class="title8">数据分析</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            if df is not None:
                option = st.selectbox(
                    "图表类型选择",
                    ("散点图1", "间距不规则数据的等值线图", "重叠密度（“山脊图”）", "散点图", "相关性分析", "小提琴图", "散点频率图", "直方图、kde 图和地毯图", "二维散点图", "三维散点图"),
                    key="chart_type_selector"
                )
                if option == "散点图1":
                    all_columns = df.columns.tolist()
                    title1_col, titlex_col = st.columns(2)
                    with title1_col:
                        title1 = st.selectbox("请选择x轴的列", all_columns,
                                            index=all_columns.index("叶顶间隙") if "叶顶间隙" in all_columns else 0, key="s1_x_axis")
                    with titlex_col:
                        titlex = st.text_input("请输入x轴的列名", value=title1, key="s1_x_label")

                    title2_col, titley_col = st.columns(2)
                    with title2_col:
                        title2 = st.selectbox("请选择y轴参数", all_columns,
                                            index=all_columns.index("压缩比") if "压缩比" in all_columns else 0, key="s1_y_axis")
                    with titley_col:
                        titley = st.text_input("请输入y轴的列名", value=title2, key="s1_y_label")

                    st.write("请选择Y轴的4个数据范围进行对比：")
                    range_col1, range_col2 = st.columns(2)
                    with range_col1:
                        values2 = st.slider("选择第一个y的表格范围", 0, len(df)-1 if df is not None else 2000, (0, min(25, len(df)-1 if df is not None else 25)) if df is not None else (25,75), key="s1_range1")
                        values3 = st.slider("选择第二个y的表格范围", 0, len(df)-1 if df is not None else 2000, (min(26, len(df)-1 if df is not None else 26), min(50, len(df)-1 if df is not None else 50)) if df is not None else (25,75), key="s1_range2")
                    with range_col2:
                        values4 = st.slider("选择第三个y的表格范围", 0, len(df)-1 if df is not None else 2000, (min(51, len(df)-1 if df is not None else 51), min(75, len(df)-1 if df is not None else 75)) if df is not None else (25,75), key="s1_range3")
                        values5 = st.slider("选择第四个y的表格范围", 0, len(df)-1 if df is not None else 2000, (min(76, len(df)-1 if df is not None else 76), min(100, len(df)-1 if df is not None else 100)) if df is not None else (25,75), key="s1_range4")

                    titlex1_val = st.text_input("请输入图表名称", f"{titley} 四范围对比", key="s1_chart_title")
                    species_input = st.text_input("输入品种名称（用逗号分隔4个名称）",
                                                "范围1,范围2,范围3,范围4", key="s1_species_names")
                    species_list_raw = [s.strip() for s in species_input.split(",") if s.strip()]
                    species_list = (species_list_raw + [f"范围{i+1}" for i in range(len(species_list_raw), 4)])[:4]

                    ranges = [values2, values3, values4, values5]
                    data_combined = pd.DataFrame()

                    try:
                        df[title1] = pd.to_numeric(df[title1], errors='coerce')
                        df[title2] = pd.to_numeric(df[title2], errors='coerce')
                        df_plot = df.dropna(subset=[title1, title2])
                        if df_plot.empty:
                            st.warning(f"选择的列 '{title1}' 或 '{title2}' 经过数值转换后没有有效数据。")
                        else:
                            for i, (start, end) in enumerate(ranges):
                                if start <= end and start < len(df_plot) and end < len(df_plot):
                                    section = df_plot.iloc[start:end + 1].copy()
                                    section["group"] = species_list[i]
                                    data_combined = pd.concat([data_combined, section])
                                else:
                                    st.warning(f"范围 {i+1} ({start}-{end}) 无效或超出数据界限。跳过此范围.")

                            if not data_combined.empty:
                                SPECIES_plot = sorted(data_combined["group"].unique())
                                MARKERS_plot = ['hex', 'circle_x', 'triangle', 'square']
                                num_groups = len(SPECIES_plot)
                                current_markers = MARKERS_plot[:num_groups]
                                current_colors_palette = 'Category10_' + str(max(3, num_groups))

                                p_bokeh_s1 = figure(title=titlex1_val, background_fill_color="#fafafa")
                                p_bokeh_s1.xaxis.axis_label = titlex
                                p_bokeh_s1.yaxis.axis_label = titley
                                p_bokeh_s1.scatter(title1, title2, source=data_combined,
                                        legend_group="group",
                                        fill_alpha=0.4, size=12,
                                        marker=factor_mark('group', current_markers, SPECIES_plot),
                                        color=factor_cmap('group', current_colors_palette, SPECIES_plot))
                                p_bokeh_s1.legend.location = "top_left"
                                p_bokeh_s1.legend.title = "分组"
                                st.bokeh_chart(p_bokeh_s1, use_container_width=True)
                            else:
                                st.warning("没有数据可用于绘制散点图1。请检查范围选择和数据。")
                    except KeyError as e:
                        st.error(f"列名错误: {e}. 请确保选择的列在上传的文件中。")
                    except Exception as e:
                        st.error(f"绘制散点图1时发生错误: {e}")

                elif option == "相关性分析":
                    def heatmap(data, row_labels, col_labels, ax=None, cbar_kw=None, cbarlabel="", **kwargs):
                        if ax is None: ax = plt.gca()
                        if cbar_kw is None: cbar_kw = {}
                        im = ax.imshow(data, **kwargs)
                        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
                        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
                        ax.set_xticks(range(data.shape[1])); ax.set_xticklabels(col_labels, rotation=-30, ha="right", rotation_mode="anchor")
                        ax.set_yticks(range(data.shape[0])); ax.set_yticklabels(row_labels)
                        ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
                        ax.spines[:].set_visible(False)
                        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
                        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
                        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
                        ax.tick_params(which="minor", bottom=False, left=False)
                        return im, cbar

                    def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"), threshold=None, **textkw):
                        if not isinstance(data, (list, np.ndarray)): data = im.get_array()
                        if threshold is not None: threshold = im.norm(threshold)
                        else: threshold = im.norm(data.max()) / 2.
                        kw = dict(horizontalalignment="center", verticalalignment="center")
                        kw.update(textkw)
                        if isinstance(valfmt, str): valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
                        texts = []
                        for i in range(data.shape[0]):
                            for j in range(data.shape[1]):
                                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                                texts.append(text)
                        return texts

                    all_columns_corr = df.columns.tolist()
                    default_cols_corr = all_columns_corr[:min(2, len(all_columns_corr))] if all_columns_corr else []
                    selected_columns_corr = st.multiselect(
                        "选择要做相关性分析的列 (至少选择2列数值型数据)",
                        options=all_columns_corr,
                        default=default_cols_corr,
                        key="corr_selected_cols"
                    )
                    if len(selected_columns_corr) < 2:
                        st.warning("请至少选择两列进行相关性分析。")
                    else:
                        df_numeric_corr = df[selected_columns_corr].copy()
                        for col in selected_columns_corr:
                            df_numeric_corr[col] = pd.to_numeric(df_numeric_corr[col], errors='coerce')
                        df_clean_corr = df_numeric_corr.dropna()
                        final_numeric_cols = df_clean_corr.columns[df_clean_corr.dtypes.apply(lambda x: pd.api.types.is_numeric_dtype(x))].tolist()

                        if len(final_numeric_cols) < 2:
                            st.warning(f"选择的列中，数值型数据不足两列进行相关性分析。可用的数值列: {final_numeric_cols}")
                        else:
                            df_for_corr = df_clean_corr[final_numeric_cols]
                            genre_corr = st.radio("请选择相关性分析方法", ["Pearson", "Spearman"], index=0, key="corr_method")
                            st.write("您选择了:", genre_corr)
                            method_corr = 'pearson' if genre_corr == "Pearson" else 'spearman'
                            corr_matrix = df_for_corr.corr(method=method_corr)
                            st.write(f'{genre_corr} 相关系数矩阵为：')
                            st.dataframe(corr_matrix)
                            fig_corr, ax_corr = plt.subplots(figsize=(max(8, len(final_numeric_cols)), max(6, len(final_numeric_cols))))
                            im_corr, cbar_corr = heatmap(corr_matrix.values, final_numeric_cols, final_numeric_cols, ax=ax_corr,
                                                    cmap="YlGn", cbarlabel=f"{genre_corr} Correlation")
                            texts_corr = annotate_heatmap(im_corr, valfmt="{x:.3f}")
                            fig_corr.tight_layout()
                            st.pyplot(fig_corr)
                            plt.close(fig_corr)

                elif option == "直方图、kde 图和地毯图":
                    all_columns_hist = df.columns.tolist()
                    normalize_choice_hist = st.radio("是否要进行标准化处理 (StandardScaler)", ["是", "否"], index=1, key="hist_normalize")
                    st.write("您选择了:", normalize_choice_hist)
                    selected_hist = []
                    col_selectors = st.columns(4)
                    default_indices = [0, 1, 0, 1]

                    for i, col_sel_container in enumerate(col_selectors):
                        with col_sel_container:
                            idx = default_indices[i] if default_indices[i] < len(all_columns_hist) else 0
                            selected_hist.append(st.selectbox(f"第{i+1}个参数", all_columns_hist, index=idx, key=f"hist_param_{i+1}"))

                    hist_data_plotly = []
                    group_labels_plotly = []
                    for i, col_name in enumerate(selected_hist):
                        try:
                            series = pd.to_numeric(df[col_name], errors='coerce').dropna()
                            if not series.empty:
                                if normalize_choice_hist == "是":
                                    scaler = StandardScaler()
                                    series_scaled = pd.Series(scaler.fit_transform(series.values.reshape(-1, 1)).flatten(), index=series.index)
                                    hist_data_plotly.append(series_scaled.values)
                                    group_labels_plotly.append(f"{col_name} (标准化)")
                                else:
                                    hist_data_plotly.append(series.values)
                                    group_labels_plotly.append(col_name)
                            else:
                                st.warning(f"列 '{col_name}' 无有效数值数据，已跳过。")
                        except Exception as e:
                            st.error(f"处理列 '{col_name}' 时出错: {str(e)}")

                    if hist_data_plotly:
                        colors_plotly = ['#A4C8D7', '#8AB78E', '#C8AFDC', '#FFB466'][:len(hist_data_plotly)]
                        try:
                            fig_hist = ff.create_distplot(hist_data_plotly, group_labels_plotly, bin_size=.2, colors=colors_plotly)
                            for trace_hist in fig_hist.data:
                                if 'marker' in trace_hist:
                                    trace_hist.update(opacity=1, marker=dict(line=dict(color='black', width=1)))
                            fig_hist.add_vline(x=0, line_dash="dash", line_color="red", line_width=2, opacity=0.8)
                            fig_hist.update_layout(
                                title="直方图与KDE密度图",
                                plot_bgcolor='white', paper_bgcolor='white',
                                margin=dict(l=50, r=50, t=50, b=50),
                                xaxis=dict(title_text="数值", tickfont=dict(size=12, family='YouYuan', color='black'), linewidth=2, linecolor='black'),
                                yaxis=dict(title_text="密度", tickfont=dict(size=12, family='YouYuan', color='black'), linewidth=2, linecolor='black'),
                                legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.7)', bordercolor='#ddd', borderwidth=1, font=dict(size=12, color='#333', family='YouYuan'), itemsizing='constant')
                            )
                            st.plotly_chart(fig_hist, use_container_width=True)
                        except Exception as e:
                            st.error(f"创建 Plotly distplot 时出错: {e}. 可能的原因是数据列只有单一值或标准差为0。")
                            st.write("用于绘图的数据:", hist_data_plotly)
                            st.write("分组标签:", group_labels_plotly)
                    else:
                        st.warning("没有可用于绘制直方图的数据.")

                elif option == "间距不规则数据的等值线图":
                    all_columns_contour = df.columns.tolist()
                    x_col_c = st.selectbox("请选择x变量", all_columns_contour, index=0, key="contour_x")
                    y_col_c = st.selectbox("请选择y变量", all_columns_contour, index=min(1, len(all_columns_contour)-1), key="contour_y")
                    z_col_c = st.selectbox("请选择z变量", all_columns_contour, index=min(2, len(all_columns_contour)-1), key="contour_z")

                    try:
                        df_clean_c = df[[x_col_c, y_col_c, z_col_c]].copy()
                        df_clean_c[x_col_c] = pd.to_numeric(df_clean_c[x_col_c], errors='coerce')
                        df_clean_c[y_col_c] = pd.to_numeric(df_clean_c[y_col_c], errors='coerce')
                        df_clean_c[z_col_c] = pd.to_numeric(df_clean_c[z_col_c], errors='coerce')
                        df_clean_c = df_clean_c.dropna()

                        if len(df_clean_c) < 3:
                            st.warning("进行三角剖分至少需要3个有效的数值数据点。请检查数据或选择其他列。")
                        else:
                            x_c = df_clean_c[x_col_c].values
                            y_c = df_clean_c[y_col_c].values
                            z_c = df_clean_c[z_col_c].values

                            fig_c, (ax1_c, ax2_c) = plt.subplots(nrows=2, figsize=(10, 12))
                            fig_c.patch.set_facecolor('#08103f')

                            ngridx, ngridy = 100, 100
                            xi_c = np.linspace(x_c.min(), x_c.max(), ngridx)
                            yi_c = np.linspace(y_c.min(), y_c.max(), ngridy)

                            triang_c = tri.Triangulation(x_c, y_c)
                            interpolator_c = tri.LinearTriInterpolator(triang_c, z_c)
                            Xi_c, Yi_c = np.meshgrid(xi_c, yi_c)
                            zi_c = interpolator_c(Xi_c, Yi_c)

                            for ax_current in [ax1_c, ax2_c]:
                                ax_current.set_facecolor('#08103f')
                                ax_current.tick_params(colors='white')
                                ax_current.xaxis.label.set_color('white')
                                ax_current.yaxis.label.set_color('white')
                                ax_current.title.set_color('white')
                                for spine in ax_current.spines.values():
                                    spine.set_edgecolor('white')

                            line_contour1_c = ax1_c.contour(xi_c, yi_c, zi_c, levels=14, linewidths=0.5, colors='white', alpha=0.7)
                            cntr1_c = ax1_c.contourf(xi_c, yi_c, zi_c, levels=14, cmap="viridis")
                            ax1_c.clabel(line_contour1_c, inline=True, fontsize=8, fmt='%.1f', colors='white')
                            cbar1 = fig_c.colorbar(cntr1_c, ax=ax1_c)
                            cbar1.ax.tick_params(colors='white')
                            cbar1.set_label(z_col_c, color='white')

                            ax1_c.set(xlim=(x_c.min(), x_c.max()), ylim=(y_c.min(), y_c.max()))
                            ax1_c.set_title(f'插值等值线 (x={x_col_c}, y={y_col_c}, z={z_col_c})')
                            ax1_c.set_xlabel(x_col_c)
                            ax1_c.set_ylabel(y_col_c)

                            line_contour2_c = ax2_c.tricontour(x_c, y_c, z_c, levels=14, linewidths=0.5, colors='white', alpha=0.7)
                            cntr2_c = ax2_c.tricontourf(x_c, y_c, z_c, levels=14, cmap="viridis")
                            ax2_c.clabel(line_contour2_c, inline=True, fontsize=8, fmt='%.1f', colors='white')

                            cbar2 = fig_c.colorbar(cntr2_c, ax=ax2_c)
                            cbar2.ax.tick_params(colors='white')
                            cbar2.set_label(z_col_c, color='white')

                            ax2_c.set(xlim=(x_c.min(), x_c.max()), ylim=(y_c.min(), y_c.max()))
                            ax2_c.set_title(f'三角剖分等值线 (x={x_col_c}, y={y_col_c}, z={z_col_c})')
                            ax2_c.set_xlabel(x_col_c)
                            ax2_c.set_ylabel(y_col_c)

                            plt.subplots_adjust(hspace=0.4)
                            st.pyplot(fig_c)
                            plt.close(fig_c)
                    except Exception as e:
                        st.error(f"绘制等值线图时发生错误: {e}")
            else:
                st.info("请先在左侧上传一个CSV或Excel文件以进行数据分析.")

with tabs[2]:
    st.markdown("### 趋势分析图示")
    image_folder = "pic"
    image_files = [f"{i}.png" for i in range(1, 30)]
    for img_file in image_files:
        try:
            full_path = os.path.join(image_folder, img_file)
            if os.path.exists(full_path):
                image = Image.open(full_path)
                st.image(image, width=1200, caption=f"趋势图: {img_file}")
            else:
                st.warning(f"图片文件 {full_path} 未找到。")
        except Exception as e:
            st.error(f"加载图片 {img_file} 时出错: {e}")

with tabs[3]:
    st.title("💬 DeepSeek AI 对话")
    st.write(
        "这是一个简单的聊天机器人，它使用 DeepSeek 的模型来生成响应。 "
        "要使用此应用程序，您需要提供一个 DeepSeek API 密钥，您可以在 DeepSeek官网 获取。"
    )

    if "api_key" not in st.session_state:
        st.session_state.api_key = os.environ.get("DEEPSEEK_API_KEY", None)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "你是一个乐于助人的AI助手."}]

    if not st.session_state.api_key:
        api_key_input = st.text_input("请输入DeepSeek API 密钥", type="password", key="deepseek_api_key_input")
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.success("API密钥已设置成功！请开始对话。")
            st.experimental_rerun()
        else:
            st.info("请输入您的DeepSeek API密钥以启用聊天功能.")
            st.stop()
    else:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        try:
            client = OpenAI(api_key=st.session_state.api_key, base_url="https://api.deepseek.com/v1")
            if prompt := st.chat_input("请输入您的问题..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    try:
                        stream = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                            stream=True,
                        )
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    except Exception as e:
                        st.error(f"调用 DeepSeek API 时出错: {e}")
                        if st.session_state.messages[-1]["role"] == "user":
                            st.session_state.messages.pop()
        except Exception as e:
            st.error(f"初始化 OpenAI 客户端时出错: {e}. 请检查您的 API 密钥和网络连接。")
            st.session_state.api_key = None
            st.experimental_rerun()

with tabs[4]:
    st.markdown("### 操作示例说明")
    op_example_image_folder = "pic"
    op_example_image_files = [f"{i}.png" for i in range(30, 34)]
    for img_file in op_example_image_files:
        try:
            full_path = os.path.join(op_example_image_folder, img_file)
            if os.path.exists(full_path):
                image = Image.open(full_path)
                st.image(image, width=1200, caption=f"操作示例: {img_file}")
            else:
                st.warning(f"图片文件 {full_path} 未找到。")
        except Exception as e:
            st.error(f"加载图片 {img_file} 时出错: {e}")