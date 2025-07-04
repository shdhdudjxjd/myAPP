import streamlit as st
from . import RightBar
from streamlit_card import card
from .import Fuc1,Fuc2,Fuc3,Fuc4

def chose_model(manager,sql):
    manager.addKey('test_state','chose')
    if manager.getState()=='chose':
        col1,col2=st.columns([0.7,0.3])
        with col1:
            with st.container(border=True):
                st.markdown(
                    '<h1 style="text-align: center;">请选择一个测试模式</h1>',
                    unsafe_allow_html=True
                )
                col_1,col_2=st.columns(2)
                with col_1:
                    if card(
                        title="例句填空📝",
                        text="选择合适的单词完成句子",
                        styles={
                            "card": {
                                "width": "250px",
                                "height": "250px",
                                "border-radius": "60px",
                            },
                            "text": {
                                "font-family": "serif",
                            },
                            "filter": {
                                "background-color": "rgb(249 121 51 / 84%)"
                            }
                        }
                    ):
                       manager.setState('test')
                       st.rerun()
                    if card(
                        title="看英选义🀄",
                        text="根据英文选对应中文",
                        styles={
                            "card": {
                                "width": "250px",
                                "height": "250px",
                                "border-radius": "60px",
                            },
                            "text": {
                                "font-family": "serif",
                            },
                            "filter": {
                                "background-color": "rgb(195, 174, 214)"
                            }
                        }
                    ):
                       manager.setState('EN_CN')
                       st.rerun()
                with col_2:
                    if card(
                            title="单词拼写✍",
                            text="根据对应的中文拼写单词",
                            styles={
                                "card": {
                                    "width": "250px",
                                    "height": "250px",
                                    "border-radius": "60px",
                                },
                                "text": {
                                    "font-family": "serif",
                                },
                                "filter": {
                                    "background-color": "rgb(149, 209, 184)"
                                }
                            }
                    ):
                        manager.setState('write')
                        st.rerun()
                    if card(
                        title="看义选英🆎",
                        text="根据中文选对应英文",
                        styles={
                            "card": {
                                "width": "250px",
                                "height": "250px",
                                "border-radius": "60px",
                            },
                            "text": {
                                "font-family": "serif",
                            },
                            "filter": {
                                "background-color": "rgb(129, 178, 217)"
                            }
                        }
                ):
                        manager.setState('CN_EN')
                        st.rerun()

            with col2:
                RightBar.rightBar('chose_model',manager,sql)
    elif manager.getState()=='write':
        Fuc2.write_word(manager,sql)
    elif manager.getState()=='EN_CN':
        Fuc3.EN_CN(manager,sql)
    elif manager.getState()=='CN_EN':
        Fuc4.CN_EN(manager,sql)
    else:
        Fuc1.test_page(manager,sql)






