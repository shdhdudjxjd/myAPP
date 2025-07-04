from streamlit_card import card
from . import RightBar
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def write_word(manager,sql):
    nowBook = manager.nowBook()
    nowID = manager.WID()
    nowRecord = nowBook[nowID]
    nowWord = list(nowBook[nowID].keys())[0]
    pos,mean=list(set(nowRecord[nowWord]['pos_mean']))[0]
    col1,col2=st.columns([0.7,0.3])
    with col1:
        with st.container(border=True):

            with stylable_container(
                        "circle-btn4",
                        css_styles="""
                                      button {
                                      border-radius: 20px;
                                      width: 80px;
                                      height: 40px;
                                      font-size: 24px;
                                      font-weight: bold;
                                      background-color: #8a8aff;
                                      justify-content: center;
                                      align-items: center;
                                      color: white;
                                      }
                                  """,
                ):
                    st.button("↩️返回", key="circle_btn4", on_click=Back, args=(manager,))
            st.progress(nowID, text=f"当前进度: ({nowID}/{100})")
            card(
                title=f"{pos}. {mean}",
                text="在下方输入框填写正确的单词",
                styles={
                    "card": {
                        "width": "700px",
                        "height": "700px",
                        "border-radius": "60px",
                    },
                    "text": {
                        "font-family": "serif",
                    },
                    "filter": {
                        "background-color": "rgb(249 121 51 / 84%)"
                    }
                }
            )

            Input=st.text_input(' ',label_visibility='hidden',key='My_text_input')
            col_1,col_2=st.columns(2)
            with col_1:
                is_correct = (Input == nowWord)
                args = (manager, sql, manager.getUser(), manager.nowName(), nowID, 2, is_correct)
                if st.button('提交', icon='📨',use_container_width=True,type='primary',on_click=ban_submit,args=args):
                    if Input != nowWord:
                        st.error("❌ 回答错误")
                        st.markdown(f"**正确答案是:** :green[{nowWord}]")
                    else:
                        st.balloons()
                        st.markdown("green[恭喜你，回答正确]")
            with col_2:
                st.button('下一个',icon='➡️',use_container_width=True,key='my_buttons',on_click=clearText,args=(manager,))

        with col2:
            RightBar.rightBar('write_page',manager,sql)

def Back(manager):
    manager.setState('chose')

def ban_submit(manager,sql,user_name,bookID,questionID,questionType,circ):
    sql.addAnswer(user_name,bookID,questionID,questionType,circ)

def clearText(manager):
    st.session_state.My_text_input = ''
    manager.addWID()