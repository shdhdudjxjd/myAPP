from streamlit_antd_components import segmented
import streamlit as st
from . import RightBar
from streamlit_extras.stylable_container import stylable_container
def test_page(manager,sql):
    manager.addKey('isable',False)
    custom_radio_css = """
       <style>
           div[role="radiogroup"][aria-label=" "] p{
               font-size: 20px !important;    
               line-height: 2.2 !important;   
           }
       </style>
       """
    st.markdown(custom_radio_css, unsafe_allow_html=True)
    nowBook = manager.nowName()
    nowID = manager.getQID()
    questions = manager.getQue()

    st.markdown("""
       <style>
           .centered-title {
               text-align: center;
               color: #4f46e5;
               font-size: 2rem;
               font-weight: 700;
               margin-bottom: 1.5rem;
               padding-bottom: 0.5rem;
           }

       </style>
       """, unsafe_allow_html=True)
    col_1, col_2 = st.columns([0.7, 0.3])
    with col_1:
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
            if 'select' not in st.session_state:
                st.session_state.select = False

            st.markdown(
                '<div class=centered-title>选择最合适的答案完成句子</div>',
                unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 20px;font-weight:bold;'>{questions['question']}</span>",
                        unsafe_allow_html=True)
            st.divider()
            opt = [questions['choice_1'], questions['choice_2'], questions['choice_3'], questions['choice_4']]
            choice = segmented(
                              items=opt,
                              index=None,
                              use_container_width=True,
                              direction='vertical',
                              bg_color='white',
                              color='blue'
                              )

            col1, col2 = st.columns(2)
            with col1:
                st.button('下一题', type="primary",on_click= next_page,use_container_width=True, key='skip-btn',args=(manager,))

            with col2:
                is_correct = (choice == questions['answer'])
                args=(manager,sql,manager.getUser(),manager.nowName(),nowID,1,is_correct)
                submit_btn = st.button(
                    "提交",
                    disabled=choice is None or manager.getValue('isable') ,
                    type="primary",
                    key='subim-btn',
                    use_container_width=True,
                    on_click=ban_submit,
                    args=args
                )


            st.divider()
            if submit_btn:
                if is_correct:
                    st.success("✅ 回答正确！")
                    with st.expander("查看解析"):
                        with stylable_container(
                                key="explanation-card",
                                css_styles="""
                                       {
                                           background-color: #f8fafc;
                                           border-radius: 8px;
                                           padding: 1rem;
                                           margin-top: 1rem;
                                           border-left: 3px solid #94a3b8;
                                       }
                                   """
                        ):
                            st.markdown("""
                                 <div style="font-weight: 500; margin-bottom: 0.5rem;">📖 题目解析</div>
                                 """, unsafe_allow_html=True
                                        )
                            st.markdown(questions["explain"])
                else:
                    st.error("❌ 回答错误")
                    with st.expander("查看解析"):
                        with stylable_container(
                                key="explanation-card",
                                css_styles="""
                                       {
                                           background-color: #f8fafc;
                                           border-radius: 8px;
                                           padding: 1rem;
                                           margin-top: 1rem;
                                           border-left: 3px solid #94a3b8;
                                       }
                                   """
                        ):
                            st.markdown("""
                                 <div style="font-weight: 500; margin-bottom: 0.5rem;">📖 题目解析</div>
                                 """, unsafe_allow_html=True)
                            st.markdown(questions["explain"])
                        correct_answer = questions['answer']
                    st.markdown(f"**正确答案:** :green[{correct_answer}]")

    with col_2:
        RightBar.rightBar('test_page',manager,sql)

def Back(manager):
    manager.setState('chose')

def ban_submit(manager,sql,user_name,bookID,questionID,questionType,circ):
    manager.setKey('isable',True)
    sql.addAnswer(user_name,bookID,questionID,questionType,circ)

def next_page(manager):
    manager.setKey('isable', False)
    manager.addQID()