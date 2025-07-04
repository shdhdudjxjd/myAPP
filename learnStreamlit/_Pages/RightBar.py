from calendar import month

import  streamlit as st
import calendar
from streamlit_extras.stylable_container import stylable_container
def Cal(key,manager,sql):

    st.markdown("<h3 style='text-align: center;'>🗓️ 日历</h3>",
                unsafe_allow_html=True)
    year = manager.getYear()
    month = manager.getMonth()
    thisday=manager.getDay()
    days = calendar.monthcalendar(year, month)
    show_calender = st.columns([0.2, 0.6, 0.2])
    with show_calender[0]:
        if st.button("＜", key=key + '1'):
            manager.subMonth()
            st.rerun()
    with show_calender[1]:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <span style="font-size: {25}px; font-weight: bold;">
                    {year} 年 {month} 月
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with show_calender[2]:
        if st.button("＞", key=key + '2'):

            manager.addMonth()
            st.rerun()

    data_col = st.columns(7)
    with data_col[0]:
        st.write('日')
    with data_col[1]:
        st.write('一')
    with data_col[2]:
        st.write('二')
    with data_col[3]:
        st.write('三')
    with data_col[4]:
        st.write('四')
    with data_col[5]:
        st.write('五')
    with data_col[6]:
        st.write('六')
    for i in range(len(days)):
        new_col = st.columns(7)
        for j in range(7):
            with new_col[j]:
                if days[i][j] != 0:
                    if sql.Checkin(year,month,days[i][j]):
                        st.write(  f'<span style="background-color: violet; border-radius: 50%;  display: inline-block; width: 3em; height: 3em; text-align: center; line-height: 3em;">{days[i][j]}</span>',unsafe_allow_html=True)
                    else:
                        st.write(  f'<span style="background-color: # fff; border-radius: 50%;  display: inline-block; width: 3em; height: 3em; text-align: center; line-height: 3em;">{days[i][j]}</span>',unsafe_allow_html=True)
    if not sql.Checkin(year,month,thisday):
        with stylable_container(
                "put_in_card"+key,
                css_styles="""
                            button {
                            border-radius: 20px;
                            background-color: #4285F4;
                            margin-bottom: 15px;
                            color:white;
                                }
                                                 """,
        ):

            user = manager.getUser()
            args = (sql, user, year, month, thisday)
            st.button('点击打卡',use_container_width=True,key="put_in_card"+key,on_click=Checkin,args=args)
    else:
        with stylable_container(
                "put_in_card_ready" + key,
                css_styles="""
                                    button {
                                    border-radius: 20px;
                                    background-color: #34A853;
                                    margin-bottom: 15px;
                                    color:white;
                                        }
                                                         """,
        ):
            st.button('已打卡', use_container_width=True, key="put_in_card_ready" + key)



def rightBar(key,manager,sql):
    with st.container(border=True):
        Cal(key,manager,sql)
    st.markdown("---")

    with st.container(border=True):
        st.subheader("📊 今日计划", anchor=False)
        count=todayPlan(manager,sql)
        if len(count)==0:
            st.markdown(f"- 学习单词数🆎: **{100}** 词")
            st.markdown(f"- 学习时间段⏱: **暂无** ")
            st.markdown(f"- 学习词书📚: **暂无** ")
            st.info('今日未设置学习计划')
        else:
            myList=[]
            if count['morning']:
                myList.append('8:00-11:30')
            if count['afternoon']:
                myList.append('14:00-17:30')
            if count['night']:
                myList.append('19:00-21:30')
            st.markdown(f"- 学习单词数🆎: **{count['count']}** 词")
            st.markdown(f"- 学习时间段⏱: **{','.join(myList)}** ")
            st.markdown(f"- 学习词书📚: **{manager.Names_Chinese[count['bookID']]}** ")



    st.divider()

def Checkin(sql,user,year,month,day):
    sql.PutCard(user,year,month,day)

def todayPlan(manger,sql):
    uname=manger.getUser()
    uyear=manger.getYear()
    umonth=manger.getMonth()
    uday=manger.getDay()
    count= sql.getPlan(uname,uyear,umonth,uday)
    return count


