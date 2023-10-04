import pymysql


class Animals:

    def __init__(self, query=''):
        self.animal_type = ''
        self.animal_id = ''
        self.name_animal = ''
        self.commands = ''
        if query != '':
            self.con = pymysql.connect(host='localhost', user='root', password='123456789', database='peoplefriends')
            with self.con:
                cur = self.con.cursor()
                cur.execute(query)
                try:
                    self.answer = cur.fetchone()
                    self.animal_id = self.answer[0]
                    self.name_animal = self.answer[1]
                    self.commands = self.answer[2]
                    cur.close()
                except:
                    cur.close()

    def new_commands(self, query):
        self.con = pymysql.connect(host='localhost', user='root', password='123456789', database='peoplefriends')
        with self.con:
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()