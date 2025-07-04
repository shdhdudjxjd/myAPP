import streamlit as st
import json
from . import RightBar

def wordBook_page(Sql,manager):
    with open('bookList.json', 'r', encoding='utf-8') as f:
        Books = json.load(f)
    col_1, col_2 = st.columns([0.7, 0.3])
    with col_1:
        with st.container(border=True):
            st.subheader("选择词书")
            st.markdown("---")
            if not Books:
                st.caption("暂无词书")
            else:
                for catgorys in Books.items():
                    catgory = catgorys[0]
                    wordbook = catgorys[1]
                    with st.expander(catgory):
                        for book in wordbook:

                            book_id = book["id"]

                            cols = st.columns([1.2, 3, 1.5])
                            with cols[0]:
                                st.image(book['picture'], width=100)
                            with cols[1]:
                                st.subheader(book["title"])
                                st.caption(book["subtitle"])

                            with cols[2]:
                                st.write("")
                                if book_id in manager.Names:
                                    st.button("已添加", key=f"btn_added_{book_id}", disabled=True,
                                              use_container_width=True)
                                else:
                                    if st.button("添加", key=f"btn_add_{book_id}", type="primary",
                                                 use_container_width=True):
                                        Sql.userAddbook(book_id, manager.getUser(), book["title"])
                                        st.rerun()

                            st.divider()
    with col_2:
        RightBar.rightBar('wordBook_page',manager,Sql)