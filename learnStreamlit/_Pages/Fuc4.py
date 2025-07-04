from streamlit_card import card
from . import RightBar
import streamlit as st
from streamlit_antd_components import segmented
from streamlit_extras.stylable_container import stylable_container
def CN_EN(manager,sql):
   CN_EN=manager.getCN_EN()
   Record=CN_EN
   print(Record)
   CN=Record['CN']
   choice1=Record['choice1']
   choice2=Record['choice2']
   choice3=Record['choice3']
   choice4=Record['choice4']
   answer=Record['answer']
   nowID=manager.getCN_EN_ID()

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
                title=f"{CN}",
                text="在下方选择正确的英文意思",
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

            opt=[choice1,choice2,choice3,choice4]
            Mychoice = segmented(
                items=opt,
                index=None,
                use_container_width=True,
                direction='vertical',
                bg_color='#E6F7FF',
                color='blue'
            )

            col_1,col_2=st.columns(2)
            with col_1:
                nowID = manager.getCN_EN_ID()
                is_correct = (Mychoice == answer)
                args = (manager, sql, manager.getUser(), manager.nowName(), nowID, 4, is_correct)
                is_subimt=st.button('提交', icon='📨',
                             use_container_width=True,
                             type='primary',
                             on_click=ban_submit,
                             args=args,
                             disabled=Mychoice is None or manager.getValue('isable')
                             )
            with col_2:
                st.button('下一个',icon='➡️',use_container_width=True,on_click=addCN_EN_ID,args=(manager,))
            if is_subimt:
                if Mychoice != answer:
                    st.error("❌ 回答错误")
                    st.markdown(f"**正确答案是:** :green[{answer}]")
                else:
                    st.balloons()
                    st.success('恭喜你，回答正确', width='stretch')

        with col2:
            RightBar.rightBar('write_page',manager,sql)


def Back(manager):
    manager.setState('chose')

def ban_submit(manager,sql,user_name,bookID,questionID,questionType,circ):
    manager.setKey('isable',True)
    sql.addAnswer(user_name, bookID, questionID, questionType, circ)

def addCN_EN_ID(manager):
    manager.setKey('isable', False)
    manager.addCN_EN_ID()