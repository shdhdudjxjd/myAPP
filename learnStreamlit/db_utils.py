import  sqlite3
from zipfile import error
import  json
import random


class Sql:
    def __init__(self):
        self.conn=sqlite3.connect("appData.db",check_same_thread=False)
        self.cursor=self.conn.cursor()



    def get_word_info(self,data):
        # 提取基本信息
        word = data["headWord"]
        us_phonetic = data["content"]["word"]["content"].get("usphone",None)
        uk_phonetic = data["content"]["word"]["content"].get("ukphone",None)
        exam_data = data["content"]["word"]["content"].get('exam',None)
        question=None
        explain=None
        choices=None
        answer=None
        if exam_data is not None:
            exam_data=exam_data[0]
            question=exam_data['question']
            explain=exam_data['answer']['explain']
            rightIndex=exam_data['answer']['rightIndex']
            choices=[]
            for choice in  exam_data['choices']:
                choices.append(choice['choice'])
            answer =exam_data['choices'][rightIndex-1]['choice']


        # 提取词性和释义
        translations = []
        for trans in data["content"]["word"]["content"]["trans"]:
            translations.append({
                "part_of_speech": trans.get('pos',None),
                "chinese_meaning": trans.get('tranCn',None)
            })

        # 提取例句
        examples = []
        for sentence in data.get("content", {}).get("word", {}).get("content", {}).get("sentence", {}).get("sentences", []):
            if len(sentence)==0:
                continue
            examples.append({
                "english": sentence["sContent"],
                "chinese": sentence["sCn"]
            })
        bookid=data["bookId"]
        # 整理结果
        result = {
            "word": word,
            "bookid":bookid,
            "phonetics": {
                "us": us_phonetic,
                "uk": uk_phonetic
            },
            "translations": translations,
            "examples": examples,
            "question": question,
            "choices":choices,
            "explain":  explain,
            "answer":answer
        }

        return result

    def getWordList(self,filename):
        wordList=[]
        with open(filename,'r',encoding='utf-8') as f:
            for line in f:
                try:
                    word_data=json.loads(line.strip())
                    word=self.get_word_info(word_data)
                    wordList.append(word)
                except error as e:
                    print(f"解析失败{e}")
                    continue
        return wordList

    def getUsers(self):
        try:
            self.cursor.execute('SELECT name FROM users ')
            row = self.cursor.fetchall()  # 获取单条数据
            return row
        except:
            print("验证失败")
            return 0


    def checkUser(self,uname,upassword):
        try:
            self.cursor.execute('SELECT * FROM users WHERE name = ? and password = ?', (uname,upassword))
            row = self.cursor.fetchone()  # 获取单条数据
            return row[0] if row else 0
        except:
            print("验证失败")
            return 0


    def addUser(self,uname,upassword):
        try:
            self. cursor.execute('''
        INSERT INTO users (name, password)
        VALUES (?, ?)
    ''', (uname,upassword))
            self.cursor.execute('''
            INSERT OR IGNORE INTO OwnBook (bookID,uname,CN)
            VALUES (?,?,?)
                       ''', ("CET4luan_2",uname,"大学英语四级"))
            self.conn.commit()
            return True
        except error as e:
            print(e)
            print("注册失败")
            self.conn.rollback()
            return False

    def getNames(self,uname):
        query = """
               SELECT 
                  bookID,CN
               FROM OwnBook
               WHERE uname = ? 
               """
        self.cursor.execute(query, (uname,))
        rows = self.cursor.fetchall()
        Name=[row[0] for row in rows]
        Name_Chinese={row[0]:row[1] for row in rows}
        return Name,Name_Chinese


    def userAddbook(self,bookID,uname,CN):
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO OwnBook (bookID,uname,CN)
                VALUES (?,?,?)
                           ''', (bookID, uname, CN))
            self.conn.commit()
            return True
        except error as e:
            print(e)
            print(f"{uname}添加{CN}失败")
            self.conn.rollback()
            return False

    def check_credentials(self, uname, upassword):
            return self.checkUser(uname, upassword)


        # ---加入用户----
    def insert_credentials(self, uname, upassword):
            return self.addUser(uname, upassword)


    def wordBook(self,filename):
        wordList=self.getWordList(filename)
        for jsonData in wordList:
            word=jsonData["word"]
            bookid=jsonData["bookid"]
            us_pho=jsonData['phonetics']['us']
            uk_pho=jsonData['phonetics']['uk']
            if jsonData['question'] is not None:
                question=jsonData['question']
                choice_1,choice_2,choice_3,choice_4=jsonData['choices']
                answer=jsonData['answer']
                explain=jsonData['explain']
                try:
                    self.cursor.execute('''
                             INSERT OR IGNORE INTO Question (bookID,question,choice_1,choice_2,choice_3,choice_4,answer, explain)
                             VALUES (?,?,?,?,?,?,?,?)
                         ''', (bookid,question,choice_1,choice_2,choice_3,choice_4,answer, explain))
                    self.conn.commit()
                except error as e:
                    print(e)
                    print(f"问题{question}插入失败")
                    self.conn.rollback()
                    return False

            try:
                self.cursor.execute('''
                INSERT OR IGNORE INTO Words (word, bookID,us_pho,uk_pho)
                VALUES (?,?,?,?)
            ''', (word,bookid,us_pho,uk_pho))
                self.conn.commit()
            except error as e:
                print(e)
                print(f"单词{word}插入失败")
                self.conn.rollback()
                return False
            for trans in jsonData['translations']:
                pos=trans['part_of_speech']
                mean=trans['chinese_meaning']
                try:
                    self.cursor.execute('''
                    INSERT OR IGNORE INTO Message (word, bookID,pos,mean)
                    VALUES (?,?,?,?)
                ''', (word, bookid, pos, mean))
                    self.conn.commit()
                except error as e:
                    print(e)
                    print(f"单词{word}的词性与释意插入失败")
                    self.conn.rollback()
                    return False

            for example in jsonData['examples']:
                exp_English=example['english']
                exp_Chinese=example['chinese']
                try:
                    self.cursor.execute('''
                    INSERT OR IGNORE INTO Example (word, bookID,exp_English,exp_Chinese)
                    VALUES (?,?,?,?)
                ''', (word, bookid, exp_English, exp_Chinese))
                    self.conn.commit()
                except error as e:
                    print(e)
                    print(f"单词{word}的词性与释意插入失败")
                    self.conn.rollback()
                    return False
        return True


    def getBook(self,Book):
            bookList=[]
            query = """
            SELECT 
                w.word, w.bookID, w.us_pho, w.uk_pho,
                m.pos, m.mean, 
                e.exp_English, e.exp_Chinese
            FROM Words w
            JOIN Message m ON w.bookID = m.bookID AND w.word = m.word
            JOIN Example e ON w.bookID = e.bookID AND w.word = e.word
            WHERE w.bookID = ?
            """
            self.cursor.execute(query, (Book,))
            rows = self.cursor.fetchall()

            result = {}
            for row in rows:
                word = row[0]
                if word not in result:
                    result[word] = {
                        "bookID": row[1],
                        "us_pho": row[2],
                        "uk_pho": row[3],
                        "pos_mean": [],
                        "english_chinese": []
                    }
                if row[4]:
                    result[word]["pos_mean"].append((row[4], row[5]))
                if row[6] and (row[6], row[7]) not in  result[word]["english_chinese"]:
                    result[word]["english_chinese"].append((row[6], row[7]))
            for key,values in result.items():
                bookList.append({key:values})

            return bookList
    def addPlan(self,uname,uyear,umonth,uday,wordCount,morning,afternoon,night,bookID):
        try:
            self.cursor.execute('''
                INSERT INTO Plan (uname, uyear, umonth, uday, wordCount, morning, afternoon, night, bookID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(uname, uyear, umonth, uday) DO UPDATE SET
                    wordCount = excluded.wordCount,
                    morning = excluded.morning,
                    afternoon = excluded.afternoon,
                    night = excluded.night,
                    bookID = excluded.bookID
            ''', (uname, uyear, umonth, uday, wordCount, morning, afternoon, night, bookID))
            self.conn.commit()
        except error as e:
            print(e)
            print(f"{uname}的学习计划设置失败")
            self.conn.rollback()
            return False
    def getQuestion(self,bookID):
        query = """
        SELECT 
           *
        FROM Question
        WHERE question is not null 
        ORDER BY RANDOM()
        LIMIT 100
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        questions=[]
        for row in rows:
            question_dict = {}
            question_dict['question']=row[2]
            question_dict['choice_1']=row[3]
            question_dict['choice_2']=row[4]
            question_dict['choice_3']=row[5]
            question_dict['choice_4']=row[6]
            question_dict['answer']=row[7]
            question_dict['explain']=row[8]
            questions.append(question_dict)
        return questions

    def EN_CN(self,bookID):
        query = """
                SELECT 
                DISTINCT  word
                FROM Words
                WHERE bookID = ? 
                """
        self.cursor.execute(query,(bookID,))
        words=self.cursor.fetchall()
        for i in range(len(words)):
            word=words[i][0]
            query1 = """
                            SELECT 
                            DISTINCT  word,mean,pos
                            FROM Message
                            WHERE bookID = ? and word = ?
                            """
            self.cursor.execute(query1, (bookID,word))
            wordmessage=self.cursor.fetchall()
            wordmean=wordmessage[0][1]
            wordpos=wordmessage[0][2]
            query2='''
            SELECT DISTINCT word,mean,pos FROM Message
            WHERE bookID=? and word!=?
            ORDER BY RANDOM()
            LIMIT 3
            '''
            self.cursor.execute(query2,(bookID,word))
            disturbs=self.cursor.fetchall()
            num=random.randint(0,3)
            ranks=[]
            for i in range(4):
                if i==num:
                    ranks.append(wordpos+'.'+wordmean)
                else:
                    ranks.append(disturbs[0][2]+'.'+disturbs[0][1])
                    disturbs.pop(0)
            try:
                choice1,choice2,choice3,choice4=ranks
                answer=wordpos+'.'+wordmean
                self.cursor.execute('''
                                    INSERT OR IGNORE INTO EN_CN (bookID,word,choice1,choice2,choice3,choice4,answer)
                                    VALUES (?,?,?,?,?,?,?)
                                ''', (bookID,word,choice1,choice2,choice3,choice4,answer))
                self.conn.commit()
            except error as e:
                print(f'{word}的EN_CN题目插入失败')
                print(e)
                self.conn.rollback()

    def getEN_CN(self,bookID):
        query = """
                SELECT 
                 *
                FROM EN_CN
                ORDER BY RANDOM()
                LIMIT 100
                """
        self.cursor.execute(query)
        Records=self.cursor.fetchall()
        EN_CN_question=[]
        for Record in Records:
            EN_CN_question.append(
                {
                    "word":Record[2],
                    "choice1":Record[3],
                    "choice2":Record[4],
                    "choice3":Record[5],
                    "choice4":Record[6],
                    "answer":Record[7]
                }
            )
        random.shuffle(EN_CN_question)
        return EN_CN_question

    def CN_EN(self,bookID):
        query = """
                        SELECT 
                        DISTINCT  word
                        FROM Words
                        ORDER BY RANDOM()
                        LIMIT 100
                """
        self.cursor.execute(query)
        words = self.cursor.fetchall()
        for i in range(len(words)):
            word = words[i][0]
            query1 = """
                                        SELECT 
                                        DISTINCT  word,mean,pos
                                        FROM Message
                                        WHERE bookID = ? and word = ?
                     """
            self.cursor.execute(query1, (bookID, word))
            wordmessage = self.cursor.fetchall()
            wordmean = wordmessage[0][1]
            wordpos = wordmessage[0][2]
            query2 = '''
                        SELECT DISTINCT word,mean,pos FROM Message
                        WHERE bookID=? and word!=?
                        ORDER BY RANDOM()
                        LIMIT 3
                        '''
            self.cursor.execute(query2, (bookID, word))
            disturbs = self.cursor.fetchall()
            num = random.randint(0, 3)
            ranks = []
            for i in range(4):
                if i == num:
                    ranks.append(word)
                else:
                    ranks.append(disturbs[0][0])
                    disturbs.pop(0)
            try:
                choice1, choice2, choice3, choice4 = ranks
                answer = word
                CN=wordpos+'.'+wordmean
                self.cursor.execute('''
                                                INSERT OR IGNORE INTO CN_EN (bookID,CN,choice1,choice2,choice3,choice4,answer)
                                                VALUES (?,?,?,?,?,?,?)
                                            ''', (bookID, CN, choice1, choice2, choice3, choice4, answer))
                self.conn.commit()
            except error as e:
                print(f'{word}的EN_CN题目插入失败')
                print(e)
                self.conn.rollback()

    def getCN_EN(self,bookID):
        query = """
                    SELECT 
                     *
                    FROM CN_EN
                    ORDER BY RANDOM()
                    LIMIT 100
                    """
        self.cursor.execute(query)
        Records = self.cursor.fetchall()
        CN_EN_question = []
        for Record in Records:
            CN_EN_question.append(
                {
                    "CN": Record[2],
                    "choice1": Record[3],
                    "choice2": Record[4],
                    "choice3": Record[5],
                    "choice4": Record[6],
                    "answer": Record[7]
                }
            )
        random.shuffle(CN_EN_question)
        return CN_EN_question

    def changeState(self,word,bookID,state):
        try:
            query = """
                           UPDATE Words
                           set wordStudy=?
                           WHERE word=? and bookID=?
                    """
            self.cursor.execute(query,(state,word,bookID))
            self.conn.commit()
        except error as e:
            print(f"单词{word}的状态更改失败")
            print(e)
            self.conn.rollback()

    def Nums(self,bookID):
        query = """
                select  wordStudy,count(wordStudy)  
                from Words 
                where bookID=?group by wordStudy;
                """
        self.cursor.execute(query,(bookID,))
        numkinds=self.cursor.fetchall()
        kinds={}
        for kind in numkinds:
            kinds[kind[0]]=kind[1]
        return kinds

    def addAnswer(self,user_name,bookID,questionID,questionType,circ):
        query='''
           INSERT INTO Answers (user_name,bookID,questionID,questionType,circ)
           VALUES (?,?,?,?,?)
           ON CONFLICT(user_name,bookID,questionID,questionType) DO UPDATE SET
                circ=excluded.circ
        '''
        try:
            self.cursor.execute(query,(user_name,bookID,questionID,questionType,circ))
            self.conn.commit()
        except error as e:
            print(f'当前{bookID}的第{questionID}道题目信息插入/更新失败')
            print(e)
            self.conn.rollback()

    def getText(self,user,bookID):
        query = '''
                  select questionType ,avg(circ),count(*) 
                  from Answers 
                  where user_name=? and bookID=?
                  group by  questionType
                '''
        self.cursor.execute(query,(user,bookID))
        ans=self.cursor.fetchall()
        Rate={}
        for item in ans:
            Rate[item[0]]=[item[1],item[2]]
        print(Rate)
        return Rate

    def getMessage(self,uname):
        query = '''
                         select *
                         from users 
                         where name=? 
                '''
        self.cursor.execute(query,(uname,))
        message=self.cursor.fetchone()
        img=message[3]
        birthday=message[4]
        return (img,birthday)

    def PutCard(self,user,year,month,day):
        query='''
        INSERT INTO  Checkin(user,year,month,day)
        VALUES (?,?,?,?)
        '''
        try:
            self.cursor.execute(query,(user,year,month,day))
            self.conn.commit()
        except error as e:
            print(f'{year}-{month}-{day}日期插入失败')
            print(e)
            self.conn.rollback()

    def Checkin(self,year,month,day):
        query = '''
                select count(*)
                from Checkin
                where year=? and month=? and day=?
                '''
        self.cursor.execute(query,(year,month,day))
        count=self.cursor.fetchone()[0]
        return count

    def getPlan(self,uname,uyear,umonth,uday):
        query = '''
                    select *
                    from Plan
                    where uname=? and uyear=? and umonth=? and uday=?
                '''
        self.cursor.execute(query,(uname,uyear,umonth,uday))
        count=self.cursor.fetchone()
        if count is None:
            return {}
        else:
            return {
                'count':count[5],
                 'morning':count[6],
                 'afternoon':count[7],
                 'night':count[8],
                 'bookID':count[9]
            }
    def allPlan(self,user):
        query = '''
                           select *
                           from Plan
                           where uname=?
                       '''
        self.cursor.execute(query, (user,))
        count = self.cursor.fetchall()

        event=[]
        for plan in count:
            myList = []
            if plan[6]:
                myList.append('(8:00-11:30)')
            if plan[7]:
                myList.append('(14:00-17:30)')
            if plan[8]:
                myList.append('(19:00-21:30)')
            dic={
                '计划日期':str(plan[2])+'-'+str(plan[3])+'-'+str(plan[4]),
                 '学习时间':','.join(myList),
                '单词数目': plan[5],
                '词书名称':plan[9]
            }
            event.append(dic)

        return  event

    def changeMessage(self,oldname,newName,newPass,head,birthday):
        updateFile=[]
        if newName!='':
            updateFile.append(f'name="{newName}"')
        if newPass!='':
            updateFile.append(f'password={newPass}')
        if head!='':
            updateFile.append(f'head="{head}"')
        if birthday!='':
            updateFile.append(f'birthday="{birthday}"')
        query=f'''
        update users
        set {','.join(updateFile)}
        where name=?
        '''
        print(query)
        try:
            self.cursor.execute(query,(oldname,))
            self.conn.commit()
        except error as e:
            print(f'{oldname}信息更新失败')
            print(e)
            self.conn.rollback()











if __name__=='__main__':
    sql=Sql()
    print('输出完成')





