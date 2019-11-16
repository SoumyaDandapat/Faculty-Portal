import psycopg2

class psql:

    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = None
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(database="dbms", user = "postgres",password = "postgres", host = "127.0.0.1", port = "5432")
            self.conn.autocommit = True
            self.cur=self.conn.cursor()
            # create a cursor
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert(self,data):
        self.conn.commit()
        new_eid=self.cur.execute("SELECT id from const where id<>0;")
        new_eid =self.cur.fetchone() 
        flag=self.cur.execute("SELECT * from employees where email='%s'",data[email])
        flag=self.cur.fetchone()
        if flag==0: 
            tuple=(data[email],data["dept"],data["pass"],data["gender"],data["dob"])
            self.cur.execute("INSERT INTO employees(email,dept,pwd,gender,dob) values{};".format(tuple))
            self.conn.commit()
            return new_eid
        else:
            return new_eid-1

    def initializer(self):

        
        # self.cur.execute("DROP DATABASE dbms")
        # self.conn.commit()
        try:
            self.cur.execute("CREATE TABLE employees(eid int,name varchar(50),pass varchar(50),gender varchar(1),dob date)")
            self.conn.commit()
        #triggers and procedures for employees
        except:
            print(1)
        try:
            self.cur.execute("CREATE TABLE eidmax(num int)")
            self.conn.commit()
        except:
            print(2)

        # trigger_statement="CREATE TRIGGER increment before INSERT ON eidmax \
        #     for each row \
        #     num=num+1;"
        
        # self.cur.execute(trigger_statement)
        try:    
            self.cur.execute("INSERT INTO eidmax values(0)")
            self.conn.commit()
        except:
            print(3)

    def clear_data(self):
        self.cur.execute("delete from eidmax ")
        self.conn.commit()
        self.cur.execute("delete from employees")
        self.conn.commit()
        try:    
            self.cur.execute("INSERT INTO eidmax values(0)")
            self.conn.commit()
        except:
            print(3)


    def verify_user(self,data):
        
        ans=self.cur.execute("SELECT * FROM check_passwd(%s,%s)",(data["eid"],data["pass"]))
        ans=self.cur.fetchone()
        if ans[0] == 'y':
            return True
        return False

    def get_leaves(self,data):
        ans=self.cur.execute("select leaves_left from employees where eid=%s",data[eid])
        ans=self.cur.fetchone()
        if ans < 0
            return 0
        else
            return ans
