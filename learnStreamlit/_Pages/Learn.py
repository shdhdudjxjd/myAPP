import  streamlit as st
from . import RightBar
import  requests
import  io
from streamlit_extras.stylable_container import stylable_container

@st.cache_data(ttl=24 * 60 * 60, show_spinner=False)
def get_audio(word, accent_type=1) -> io.BytesIO | None:
    if not word:
        st.warning("请求音频的单词为空。")
        return None

    url = f"https://dict.youdao.com/dictvoice?audio={word}&type={accent_type}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if response.content:
            return io.BytesIO(response.content)
        else:
            return None
    except requests.exceptions.HTTPError as e:
        st.error(f"有道音频API HTTP错误: {e.response.status_code} for word '{word}'. URL: {url}")
    except requests.exceptions.Timeout:
        st.error(f"请求有道音频超时 for word '{word}'. URL: {url}")
    except requests.exceptions.ConnectionError:
        st.error(f"无法连接到有道音频服务 for word '{word}'. URL: {url}")
    except requests.exceptions.RequestException as e:
        st.error(f"请求有道音频时发生一般错误: {e} for word '{word}'. URL: {url}")
    except Exception as e:
        st.error(f"处理有道音频时发生未知错误: {type(e).__name__} - {e} for word '{word}'")

    return None

def learn_page(manager,sql):
    nowName = manager.nowName()
    nowBook = manager.nowBook()
    nowID = manager.nowID()
    nowRecord = nowBook[nowID]
    nowWord = list(nowBook[nowID].keys())[0]
    year=manager.getYear()
    month=manager.getMonth()
    day=manager.getDay()
    user=manager.getUser()
    num = sql.getPlan(user,year,month,day)
    if len(num)==0:
        num=100
    else:
        num=num['count']
    main_area_cols = st.columns([0.7,0.3])
    with main_area_cols[0]:
        with st.container(border=True):
            word_cols = st.columns([0.7, 0.3])
            with word_cols[0]:
                st.subheader(nowWord, anchor=False)
            with word_cols[1]:
                audio_bytes = get_audio(nowWord)
                if audio_bytes:
                    st.audio(audio_bytes)
            if manager.getValue('wordState') == 'chose':
                    st.markdown("你认识这个单词吗？")
                    recognition_btn_cols = st.columns(3)
                    with recognition_btn_cols[0]:
                        with stylable_container(
                                "know_the_word",
                                css_styles="""
                                        button {
                                            border-radius: 20px;
                                            background-color: rgb(147 254 183);
                                            margin:10px;
                                                }
                                            """,
                        ):
                            my_args=(manager,sql,nowWord,nowName,"know")
                            st.button("✅ 我认识", use_container_width=True,on_click=change,args=my_args,key="know_the_word")
                    with recognition_btn_cols[1]:
                        with stylable_container(
                                "not_really_word",
                                css_styles="""
                                            button {
                                            border-radius: 20px;
                                            background-color: rgb(229 238 60);
                                             margin:10px;
                                                }
                                         """,
                        ):
                            my_args = (manager,sql, nowWord, nowName, "amb")
                            st.button("🤔 有点模糊", use_container_width=True,on_click=change,args=my_args,key="not_really_word")
                    with recognition_btn_cols[2]:
                        with stylable_container(
                                "uknow_the_word",
                                css_styles="""
                                        button {
                                        border-radius: 20px;
                                        background-color: rgb(255 85 85);
                                        margin:10px;
                                                }
                                        """,
                        ):
                            my_args = (manager,sql, nowWord, nowName, "unknow")
                            st.button("❌ 不认识", use_container_width=True,on_click=change,args=my_args ,key="uknow_the_word")
            else:
                    for pos, mean in list(set(nowRecord[nowWord]['pos_mean'])):
                        st.markdown(f"**{pos}**. {mean}")

                    with st.expander("查看例句"):
                        for english, chinese in nowRecord[nowWord]['english_chinese']:
                            st.markdown(f"▪️ {english} ({chinese})")

                    st.caption(f"美式音标: {nowRecord[nowWord]['us_pho']}")
                    st.caption(f"英式音标: {nowRecord[nowWord]['uk_pho']}")
                    st.text("")
                    st.button("下一个单词 ❯", type="primary", use_container_width=True,on_click=getNext,args=(manager,))
                    st.markdown("---")

        with st.container(border=True):
            st.subheader("学习设置与进度", anchor=False)
            st.write(f"当前词书: **{manager.Names_Chinese[nowName]}**")
            st.progress(nowID, text=f"当前进度: ({nowID}/{num})")


    with main_area_cols[1]:
        RightBar.rightBar('learn_page',manager,sql)

def change(manager,sql,word,bookID,state):
        manager.setKey('wordState','next')
        sql.changeState(word,bookID,state)





def getNext(manager):
    manager.setKey('wordState', 'chose')
    st.toast("加载下一个单词...")
    manager.addID()

