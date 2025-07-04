import streamlit as st
from datetime import  datetime

class Management:
    def __init__(self,Sql):
        self.addKey("auth_form_to_show", "login")
        self.addKey('user_name', None)
        self.addKey('user_password', None)
        self.Names, self.Names_Chinese = Sql.getNames(st.session_state.user_name)
        self.addKey('user_message', {})
        self.addKey('isable', False)
        self.addKey('wordState','chose')
        Users = Sql.getUsers()
        for user_name in Users:
            user=user_name[0]
            if user not in st.session_state.user_message.keys():
                st.session_state.user_message[user] = {}
            for name in self.Names:
                if name not in st.session_state.user_message[user].keys():
                    st.session_state.user_message[user][name] = 0
                if 'nowBook' not in st.session_state.user_message[user].keys():
                    st.session_state.user_message[user]['nowBook'] = self.Names[0]
                if 'questionID' not in st.session_state.user_message[user].keys():
                    st.session_state.user_message[user]['questionID'] = 0
                if 'writeWord' not in st.session_state.user_message[user].keys():
                    st.session_state.user_message[user]['writeWord'] = 0
                if 'EN_CN_ID'not in st.session_state.user_message[user].keys():
                    st.session_state.user_message[user]['EN_CN_ID'] = 0
                if 'CN_EN_ID'not in st.session_state.user_message[user].keys():
                    st.session_state.user_message[user]['CN_EN_ID'] = 0

        self.addKey('Books', {})
        self.addKey('EN_CN',{})
        self.addKey('CN_EN', {})
        self.addKey('questions', {})
        for name in self.Names:
            if name not in st.session_state.Books.keys():
                st.session_state.Books[name] = Sql.getBook(name)
            if name not in st.session_state.questions.keys():
                st.session_state.questions[name] = Sql.getQuestion(name)
            if name not in st.session_state.EN_CN.keys():
                st.session_state.EN_CN[name] = Sql.getEN_CN(name)
            if name not in st.session_state.CN_EN.keys():
                st.session_state.CN_EN[name] = Sql.getCN_EN(name)
        self.addKey('year', datetime.now().year)
        self.addKey('month', datetime.now().month)
        self.addKey('day', datetime.now().day)



    def getUser(self):
        return st.session_state.user_name
    def setUser(self,uname):
        st.session_state.user_name=uname
    def getForm(self):
        return st.session_state.auth_form_to_show
    def setForm(self,state):
        st.session_state.auth_form_to_show=state
    def nowName(self):
        user=self.getUser()
        return st.session_state.user_message[user]['nowBook']

    def nowBook(self):
        name=self.nowName()
        return st.session_state.Books[name]
    def nowID(self):
        user=self.getUser()
        name=self.nowName()
        return  st.session_state.user_message[user][name]
    def addID(self):
        user = self.getUser()
        name = self.nowName()
        st.session_state.user_message[user][name]+=1

    def subID(self):
        user = self.getUser()
        name = self.nowName()
        st.session_state.user_message[user][name] = max(st.session_state.user_message[user][name]-1,0)

    def getYear(self):
        return st.session_state.year
    def getMonth(self):
        return st.session_state.month
    def getDay(self):
        return st.session_state.day
    def subMonth(self):
        st.session_state.month = st.session_state.month - 1
        if st.session_state.month < 1:
            st.session_state.month = 12
            st.session_state.year = st.session_state.year - 1
    def addMonth(self):
        st.session_state.month = st.session_state.month + 1
        if st.session_state.month > 12:
                st.session_state.month = 1
                st.session_state.year = st.session_state.year + 1


    def getQID(self):
        user=self.getUser()
        return st.session_state.user_message[user]['questionID']


    def getQue(self):
        name=self.nowName()
        id=self.getQID()
        return st.session_state['questions'][name][id]


    def getEN_CN_ID(self):
        user = self.getUser()
        return st.session_state.user_message[user]['EN_CN_ID']

    def getEN_CN(self):
        name = self.nowName()
        id = self.getEN_CN_ID()
        return st.session_state.EN_CN[name][id]

    def getCN_EN_ID(self):
        user = self.getUser()
        return st.session_state.user_message[user]['CN_EN_ID']

    def getCN_EN(self):
        name = self.nowName()
        id = self.getCN_EN_ID()
        return st.session_state.CN_EN[name][id]

    def addEN_CN_ID(self):
        user = self.getUser()
        st.session_state.user_message[user]['EN_CN_ID']+=1

    def addCN_EN_ID(self):
        user = self.getUser()
        st.session_state.user_message[user]['CN_EN_ID']+=1

    def addQID(self):
        user = self.getUser()
        st.session_state.user_message[user]['questionID']+=1

    def addWID(self):
        user = self.getUser()
        st.session_state.user_message[user]['writeWord'] +=1

    def WID(self):
        user = self.getUser()
        return st.session_state.user_message[user]['writeWord']

    def addKey(self,key,value):
        if key not in st.session_state:
            st.session_state[key]=value

    def getState(self):
        return st.session_state.test_state

    def setState(self,value):
        st.session_state.test_state=value

    def getValue(self,key):
        return st.session_state[key]

    def setKey(self,key,value):
            st.session_state[key] = value





