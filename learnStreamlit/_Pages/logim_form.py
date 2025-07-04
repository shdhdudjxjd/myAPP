import streamlit as st
from streamlit_card import card
# background: #f6f5f7

def Login_form(Sql,manager):
    # st.title("📚 在线背单词 软件")
    # st.markdown("---")
    st.set_page_config(layout="centered")


    if manager.getForm() == "login":
            col1, col2 = st.columns([3,4], gap=None)
            with col2:
                        with st.form("login_form_v6",height=400):
                            st.markdown(
                                "<h1 style='text-align: center; font-weight: bold;'>登录</h1>",
                                unsafe_allow_html=True
                            )

                            uname = st.text_input("用户名", key="login_uname_v6")
                            upassword = st.text_input("密码", type="password", key="login_pword_v6")
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True)
                            col_1,col_2=st.columns(2)
                            with col_1:
                                if st.form_submit_button("登录",use_container_width=True):
                                    id = Sql.check_credentials(uname, upassword)
                                    print(id)
                                    if id:
                                        manager.setForm("mainwindow")
                                        manager.setUser(uname)
                                        st.success(f"欢迎回来, {uname}!")
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        message("用户名或密码错误。")
                            with col_2:
                                if st.form_submit_button("注册",use_container_width=True):
                                    manager.setForm("register")
                                    st.rerun()
            with col1:
                card(
                    title="欢迎",
                    text="这是在线背单词软件的登陆表单",
                    styles={
                        "card": {
                            "width": "300px",
                            "height": "410px",
                            "padding":"0px",
                            "margin":"0px",

                        },
                        "text": {
                            "font-family": "serif",
                        },
                        "filter": {
                            "background-color": "#FF4B55",

                        },
                        "div":{
                            "transform": "scale(calc(1 / 0.95))"
                        }

                    }
                )




def Register_form(Sql,manager):
        col1, col2 = st.columns([3, 4], gap=None)
        with col2:
            with st.form("register_form_v6"):
                st.markdown(
                    "<h1 style='text-align: center; font-weight: bold;'>注册</h1>",
                    unsafe_allow_html=True
                )
                uname = st.text_input("用户名*", key="reg_uname_v6")
                pword = st.text_input("密码*", type="password", key="reg_pword_v6")
                conf_pword = st.text_input("确认密码*", type="password", key="reg_conf_pword_v6")
                col_1, col_2 = st.columns(2)
                with col_1:
                    if st.form_submit_button("注册",use_container_width=True):
                        if not uname or not pword:
                            st.warning("用户名和密码不能为空。")
                        elif pword == conf_pword:
                            if Sql.insert_credentials(uname, pword):
                                st.success("账户创建成功！请返回登录。")
                                st.balloons()
                                manager.setForm("login")
                                st.rerun()
                            else:
                                message("该用户名已被注册。")
                        else:
                            message("两次输入的密码不匹配。")
                with col_2:
                    if st.form_submit_button("返回登录",use_container_width=True):
                        manager.setForm("login")
                        st.rerun()
        with col1:
            card(
                title="欢迎",
                text="这是在线背单词软件的注册表单",
                styles={
                    "card": {
                        "width": "300px",
                        "height": "410px",
                        "padding": "0px",
                        "margin": "0px",

                    },
                    "text": {
                        "font-family": "serif",
                    },
                    "filter": {
                        "background-color": "#FF4B55",

                    },
                    "div": {
                        "transform": "scale(calc(1 / 0.95))"
                    }

                }
            )

@st.dialog(" ")
def message(name):
       st.error(name)
       if st.button('确认',use_container_width=True,type='primary'):
            st.rerun()
