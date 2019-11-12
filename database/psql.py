import psycopg2

class psql:

    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = None
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(database="dbms", user = "postgres",password = "postgres", host = "127.0.0.1", port = "5432")
            cur=self.conn.cursor()
            # create a cursor
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert(self,data):
        self.cur.execute("select * from eidmax")
        row = self.cur.fetchone()
        new_eid=row[0]   
        tuple=(new_eid,data["name"],data["pass"],data["gender"],data["dob"])
        self.cur.execute("INSERT INTO employee_info values{}".format(tuple))
        self.conn.commit()

    def initializer(self):

        
        # cur.execute("DROP DATABASE dbms")
        self.cur.execute("CREATE TABLE employees(eid int,name varchar(50),pass varchar(50),gender varchar(1),dob date)")
        #triggers and procedures for employees
        self.cur.execute("CREATE TABLE eidmax(num int)")

        trigger_statement="CREATE OR REPLACE TRIGGER increment before INSERT OF num ON eidmax \
            for each row  begin num=num+1 end;"
        
        self.cur.execute(trigger_statement)
        self.cur.execute("INSERT INTO eidmax values(0)")
        self.conn.commit()

    def verify_user(self,data):
        ans=self.cur.execute("SELECT COUNT(*) FROM employees where eid={} and pass={}".format(data["eid"],data["pass"]))
        if ans[0] == 1:
            return True
        return False

