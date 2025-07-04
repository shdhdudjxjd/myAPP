import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
from st_aggrid import AgGrid
import pandas as pd

def create_status_chart(manager,sql):
    kind = sql.Nums(manager.nowName())
    know = kind.get('know', 0)
    amb = kind.get('amb', 0)
    unknow = kind.get('unknow', 0)
    unlearned = kind.get('unlearned', 0)
    data = {
        '状态': ['认识的单词 🤔', '模糊的单词 😳', '不认识的单词 ❌', '未学单词 📖'],
        '数量': [know,amb,unknow,unlearned]
    }
    df = pd.DataFrame(data)
    colors = ['#2ECC71', '#F39C12', '#E74C3C', '#BDC3C7']

    fig = px.pie(df, values='数量', names='状态',
                 hole=0.4,
                 title=' ',
                 color_discrete_sequence=colors)

    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont_size=12,
        marker=dict(line=dict(color='#FFFFFF', width=4))
    )
    fig.update_layout(
        showlegend=False,
        title_x=0.5,
        margin=dict(t=50, b=20, l=20, r=20),
        annotations=[dict(text=f'已学<br>{know+amb+unknow}', x=0.5, y=0.5, font_size=24, showarrow=False)]
    )
    col_1, col_2, col_3 = st.columns(3)
    col_1.metric(label="认识的单词✅", value=know, delta=know)
    col_2.metric(label="模糊的单词😳", value=amb, delta=amb)
    col_3.metric(label="不认识的单词❌", value=unknow, delta=unknow)
    style_metric_cards()
    st.divider()
    st.markdown(f'<h4 style="text-align: center;">单词记忆情况分布</h4>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)


def rader(manager,sql):
    user=manager.getUser()
    bookID=manager.nowName()
    Rate=sql.getText(user,bookID)
    Rate1,Rate2,Rate3,Rate4=Rate.get(1,0),Rate.get(2, 0),Rate.get(3, 0), Rate.get(4, 0)
    num1,num2,num3,num4=0,0,0,0
    if Rate1!=0:
        num1 = Rate1[1]
        Rate1=Rate1[0]
    if Rate2!=0:
        num2 = Rate2[1]
        Rate2=Rate2[0]
    if Rate3!=0:
        num3 = Rate3[1]
        Rate3=Rate3[0]
    if Rate4!=0:
        num4 = Rate4[1]
        Rate4=Rate4[0]
    df= pd.DataFrame({
        "Category": ['例句填空', '单词拼写', '看英选义', '看义选英'],
        "Score": [f"{Rate1:.2%}",f"{Rate2:.2%}",f"{Rate3:.2%}",f"{Rate4:.2%}"]
    })
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df['Score'],
        theta=df['Category'],
        fill='toself',
        name='平均正确率',
        marker=dict(color='rgba(231, 76, 60, 0.6)')
    ))

    col_1, col_2 = st.columns(2)
    col_1.metric(label="例句填空(答题数)", value=num1, delta=num1)
    col_2.metric(label="单词拼写(答题数)", value=num2, delta=num2)
    col_3, col_4= st.columns(2)
    col_3.metric(label="看英选义(答题数)", value=num3, delta=num3)
    col_4.metric(label="看义选英(答题数)", value=num4, delta=num4)
    style_metric_cards()
    st.divider()
    st.markdown(f'<h4 style="text-align: center;">各模块题目正确率</h4>',unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)


def staticist_page(manager,sql):
    col1,col2=st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown(f'<h2 style="text-align: center;">当前词库学习情况</h2>',unsafe_allow_html=True)
            create_status_chart(manager,sql)

    with col2:
        with st.container(border=True):
            st.markdown(f'<h2 style="text-align: center;">测试情况</h2>', unsafe_allow_html=True)
            rader(manager,sql)
    events=sql.allPlan(manager.getUser())
    for event in events:
        event['词书名称']=manager.Names_Chinese[event['词书名称']]
    events=pd.DataFrame(events)
    with st.container(border=True):
        st.markdown(f'<h4 style="text-align: center;">计划汇总</h4>', unsafe_allow_html=True)
        AgGrid(events,fit_columns_on_grid_load=True,show_search=True,show_toolbar=True,show_download_button=True)


if __name__ == '__main__':
    pass