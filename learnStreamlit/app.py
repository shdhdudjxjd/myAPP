import streamlit as st
import  db_utils
import  calendar
from datetime import  datetime
from _Pages import  logim_form
from _Pages import  Learn
from _Pages import Test
from _Pages import Wordbook
from _Pages import Staticist
import sesstion_managment
from streamlit_extras.stylable_container import stylable_container
class app:
    def __init__(self):
        self.Sql=db_utils.Sql()
        self.manger=sesstion_managment.Management(self.Sql)
        self.runAPP()




    def chose_change(self):
        radio_key=st.session_state.radio_key
        for name in self.manger.Names:
            if self.manger.Names_Chinese[name] == radio_key:
                st.session_state.user_message[st.session_state.user_name]['nowBook'] = name
                return





    def main_window(self):
        st.set_page_config(layout="wide")
        with st.sidebar:
            col1, col2, col3 = st.columns(3)  # 比例可调整
            with col2:
                img=self.Sql.getMessage(self.manger.getUser())[0]
                st.image(img,width=100)
                st.markdown(f'<h3 style="text-align:center;">{self.manger.getUser()}</h3>', unsafe_allow_html=True)
            with stylable_container(
                        "change_message",
                        css_styles="""
                                    button {
                                    border-radius: 20px;
                                    background-color: #007bff;
                                    color:white;
                                    margin:0px;
                                            }
                                                        """,
                ):
                    if st.button('个人信息查看',key="change_message",use_container_width=True):
                        self.user_message()
            st.divider()
            st.subheader("📖 我的词书")
            opt=[]
            for name in self.manger.Names:
                opt.append(self.manger.Names_Chinese[name])
            st.radio(
                "📕选择词书",
                options=opt,
                label_visibility="collapsed",
                key="radio_key",
                on_change=self.chose_change
            )
            st.divider()
            with stylable_container(
                    "adding_plan" ,
                    css_styles="""
                                  button {
                                  border-radius: 20px;
                                  color:white;
                                      }
                                                       """,
            ):
                if st.button("📝添加计划", use_container_width=True,key="adding_plan",type='primary'):
                    self.plan()


        st.markdown("""
            <style>
            .stTabs [data-baseweb="tab-list"] {
                justify-content: space-around;
            }
            .stTabs [data-baseweb="tab"] {
                flex-grow: 1;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
            }
            </style>
            """, unsafe_allow_html=True)
        nav_tabs_keys = ["学  习", "词  书 ", "测  试", "统  计"]
        learn_tab, wordlist_tab, test_tab, stats_tab = st.tabs(nav_tabs_keys)
        with learn_tab:
            Learn.learn_page(self.manger,self.Sql)
        with wordlist_tab:
            Wordbook.wordBook_page(self.Sql,self.manger)
        with test_tab:
            Test.chose_model(self.manger,self.Sql)
        with stats_tab:
            Staticist.staticist_page(self.manger,self.Sql)


    #--学习计划表单----
    @st.dialog(" ")
    def plan(self):
        st.markdown("<h2 style='text-align: center; margin-bottom: 35px;'>请设置你的打卡计划?</h2>",
                    unsafe_allow_html=True)
        col = st.columns(3)
        nowTime=datetime.now()
        year=nowTime.year
        with col[0]:
            select_year=st.selectbox('年份', [i for i in range(year,year+2)])
        with col[1]:
            select_month=st.selectbox('月份', [i for i in range(1,12)])
        with col[2]:
            select_day=calendar.monthrange(select_year,select_month)[1]
            thisday=st.selectbox('天', [i for i in range(1,select_day+1)])
        num = st.slider('请选择你要学习的单词数目', 0, 2000, 0)
        st.write("学习时段(可多选)")
        col_1 = st.columns(3)
        st.markdown("""
               <style>
                   div[data-testid="stCheckbox"] > label {
                       white-space: nowrap;
                   }
               </style>
           """, unsafe_allow_html=True)
        with col_1[0]:
            morning=st.checkbox("早晨(8:00-11:30)")
        with col_1[1]:
            afternoon=st.checkbox("下午(14:00-17:30)")
        with col_1[2]:
            night=st.checkbox("晚上(19:00-21:30)")
        opt = []
        for name in self.manger.Names:
            opt.append(self.manger.Names_Chinese[name])
        tmpDict={v:k for k,v in self.manger.Names_Chinese.items()}
        bookID=tmpDict[st.selectbox("选择词书", opt)]
        if st.button("提交计划", type="primary", use_container_width=True):
            if num>0 and (morning or afternoon or night):
                uname=st.session_state.user_name
                uyear=select_year
                umonth=select_month
                uday=thisday
                wordCount=num
                self.Sql.addPlan(uname,uyear,umonth,uday,wordCount,morning,afternoon,night,bookID)
                st.rerun()
            elif num<=0:
                st.warning('选择的单词数必须>0')
            else:
                st.warning('至少选择一个时间段')

    @st.dialog("个人信息查看与修改")
    def user_message(self):
        tabs = ['个人信息','更改信息']
        messages,change_message = st.tabs(tabs)
        message = self.Sql.getMessage(self.manger.getUser())
        img =message[0]
        birthday=message[1]
        print(birthday)
        with messages:
            col_1, col_2, col_3 = st.columns(3)
            with col_2:
                st.image(img, width=100)
                st.markdown(f"姓名🆔: **{self.manger.getUser()}** 词")
                st.write(' ')
                st.write(' ')
                st.markdown(f"生日🎂: **{birthday}** ")

        with change_message:
            col_1,col_2,col_3=st.columns(3)
            with col_2:
                st.image(img, width=100)
            file=st.file_uploader('新头像在此长传',type=["jpg", "jpeg", "png"])
            if file is not None:
                st.write('图片预览')
                st.image(file,width=300)

            newName=st.text_input('请输入你的新姓名🆔')
            newPass=st.text_input('请输入新密码🔐',type='password')
            cPass = st.text_input('确认密码🔐', type='password')
            head=file
            birthday=st.date_input('请输入你的生日🎂',datetime.now())
            if head is None:
                head=''
            else:
                head='picture/'+file.name
            col1,col2=st.columns(2)
            with col1:
                with stylable_container(
                        "confirm_change_message",
                        css_styles="""
                        button {
                        border-radius: 20px;
                        background-color:rgb(92, 184, 92);
                        color:white;
                        margin:0px;
                        }
                                                                       """,
                ):
                    args=(self.manger.getUser(),newName,newPass,head,birthday,file)
                    if st.button('确定',use_container_width=True,key="confirm_change_message",on_click=self.updateMessage,args=args):
                        st.rerun()

            with col2:
                with stylable_container(
                        "rollback_change_message",
                        css_styles="""
                                                               button {
                                                               border-radius: 20px;
                                                               background-color:rgb(217, 83, 79);
                                                               color:white;
                                                               margin:0px;
                                                                       }
                                                                                   """,
                ):
                    if st.button('取消',use_container_width=True,key="rollback_change_message"):
                        st.rerun()


    def updateMessage(self,oldname,newName,newPass,head,birthday,file):
            self.Sql.changeMessage(oldname,newName,newPass,head,birthday)
            with open(head, "wb") as f:
                f.write(file.getbuffer())



    def runAPP(self):

        if self.manger.getForm() == "login" :
            logim_form.Login_form(self.Sql,self.manger)
        elif  self.manger.getForm() == "register":
            logim_form.Register_form(self.Sql,self.manger)
        else :
            self.main_window()




if __name__=='__main__':
   App=app()


