import psycopg2

class psql:

    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = None
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(database="dbms", user = "postgres",password = "Jon1114", host = "127.0.0.1", port = "5432")
            self.conn.autocommit = True
            self.cur=self.conn.cursor()
            # create a cursor
            print("connected")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert(self,data):
        self.conn.commit()
        new_eid=self.cur.execute("SELECT id from const where id<>0;")
        new_eid =self.cur.fetchone() [0]
        leaves=self.cur.execute("SELECT leaves_left from const where id<>0;")
        leaves =self.cur.fetchone() [0]
        print(new_eid)
        flag=self.cur.execute("SELECT COUNT(*) from employees where email='{}'".format(data["email"]))
        flag=self.cur.fetchone()[0]
        if flag==0: 
            tuple=(data["name"],new_eid,data["email"],data["dept"],data["pass"],data["gender"],data["dob"],leaves)
            print(tuple)
            self.cur.execute("INSERT INTO employees(name,eid,email,dept,pwd,gender,dob,leaves_left) values{};".format(tuple))
            self.conn.commit()
            return new_eid
        else:
            return -1

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
        self.cur.execute("delete from const ")
        self.conn.commit()
        self.cur.execute("delete from employees")
        self.conn.commit()
        try:    
            self.cur.execute("INSERT INTO const values(201700,0,10)")
            self.conn.commit()
        except:
            print(3)


    def verify_user(self,data):
        
        ans=self.cur.execute("SELECT * FROM check_passwd(%s,%s)",(data["eid"],data["pass"]))
        ans=self.cur.fetchone()
        print(ans)
        if ans[0] == 'y':
            return True
        return False

    def get_leaves(self,data):
        ans=self.cur.execute("select end_leave-start_leave from employees where eid={}".format(data))
        ans=self.cur.fetchone()[0]
        if ans < 0:
            return 0
        else:
            return ans
    
    def insert_leave(self,data):
        self.conn.commit()
        new_lid=self.cur.execute("SELECT leave_id from const where id<>0;")
        new_lid =self.cur.fetchone() [0]
        leaves=self.cur.execute("SELECT leaves_left from const where id<>0;")
        leaves =self.cur.fetchone() [0]
        leaves_left=self.cur.execute("SELECT end_leave-start_leave from employees where eid=%s",data["eid"])
        leaves_left=self.cur.fetchone()[0]
        flag=self.cur.execute("SELECT count(*) from leave_application where applicant_id=%s",data["eid"])
        flag=self.cur.fetchone()[0]

        if leaves_left-data["days"] < -leaves or flag==1:
            return -1
        else :
            flag2=self.cur.execute("select count(*) from hod where hod_id=%s",data["eid"])
            flag2=self.cur.fetchone()[0]
            flag3=self.cur.execute("select count(*) from dean where dean_id=%s",data["eid"])
            flag3=self.cur.fetchone()[0]
            if flag2==0 and flag3==0:
                self.cur.execute("insert into leave_application values(%s,%s,%s,%s,%s,%s)",new_lid,data["eid"],data["reason"],data["end_leave"],data["start_leave"],1)
            else:
                self.cur.execute("insert into leave_application values(%s,%s,%s,%s,%s,%s)",new_lid,data["eid"],data["reason"],data["end_leave"],data["start_leave"],10)
            self.cur.execute("update const set leave_id=leave_id+1;")
            return new_lid
    
    def set_leaves(self,data):
        self.conn.commit()
        self.cur.execute("UPDATE const set leaves_left= %s where id<>0",data["leaves"])

    def add_comment(self,data):
        self.conn.commit()
        comment=self.cur.execute("SELECT comment from leave_application where leave_id=%s",data["leave_id"])
        comment=self.cur.fetchone()[0]
        employee_name=self.cur.execute("SELECT name from employees where eid=%s",data["id"])
        employee_name=self.cur.fetchone()[0]
        comment=comment+'&'+employee_name+data["new_comment"]
        self.cur.execute("update leave_application set comment=%s where leave_id=%s",comment,data["leave_id"])

    def act_on_leave(self,data):
        self.conn.commit()
        time=self.cur.execute("select current_date;")
        time=self.cur.fetchone()[0]
        flag1=self.cur.execute("select count(*) from hod where hod_id=%s",data["id"])
        flag1=self.cur.fectchone()[0]
        flag2=self.cur.execute("select count(*) from dean where dean_id=%s",data["id"])
        flag2=self.cur.fectchone()[0]
        flag3=self.cur.execute("select count(*) from director where director_id=%s",data["id"])
        flag3=self.cur.fectchone()[0]
        if flag1 == 1 or flag2==1:
            self.cur.execute("INSERT into paper_trail(action_taken,time_stamp,position,id,lid) values(%s,%s,%s,%s,%s)",data["action"],time,data["position"],data["id"],data["leave_id"])
        if flag3 ==1:
            temp='director'
            self.cur.execute("INSERT into paper_trail(action_taken,time_stamp,position,id,lid) values(%s,%s,%s,%s,%s)",data["action"],time,temp,data["id"],data["leave_id"])

    def promote(self,data):
        self.conn.commit()
        department=self.cur.execute("select dept from employees where eid={};".format(data["eid"]))
        department=self.cur.fetchone()[0]
        time=self.cur.execute("select current_date;")
        time=self.cur.fetchone()[0]
        if data["dept"] in ["CSE",'EE','ME']:
            flag=self.cur.execute("select count(*) from employees where eid={} and dept='{}' ;".format(data["eid"],department))
            flag=self.cur.fetchone()[0]
            if flag==0:
                return False
            else:
                flag2=self.cur.execute("select count(*) from hod where dept_name='{}';".format(data["dept"]))
                flag2=self.cur.fetchone()[0]
                if flag2 == 1:
                    attributes=self.cur.execute("select * from hod where dept_name=%s;",data["dept"])
                    attributes=self.cur.fetchone()
                    self.cur.execute("insert into hod_database values(%s,%s,%s,%s);",attributes[0],attributes[1],attributes[2],time)
                    self.cur.execute("update hod set hod_id=%s,start_time=%s,end_time=%s where dept=%s;",data["eid"],data["start_time"],data["end_time"],data["dept"])
                else:
                    self.cur.execute("insert into hod values(%s,%s,%s,%s);",data["eid"],data["dept"],data["start_time"],data["end_time"])
                return True
        if data["dept"]=='director':
            flag=self.cur.execute("select count(*) from director;")
            if flag==1:
                attributes=self.cur.execute("select * from director;")
                attributes=self.cur.fetchone()
                self.cur.execute("insert into director_database values(%s,%s,%s);",attributes[0],attributes[1],time)
                self.cur.execute("update director set director_id=%s,start_time=%s,end_time=%s;",data["eid"],data["start_time"],data["end_time"])
            else:
                self.cur.execute("insert into director values(%s,%s,%s);",data["eid"],data["start_time"],data["end_time"])
            return True
        if data["dept"]=='faculty affairs':
            flag=self.cur.execute("select count(*) from dean where dean_type='faculty affairs';")
            flag=self.cur.fetchone()[0]
            if flag==1:
                attributes=self.cur.execute("select * from dean where dean_type='faculty affairs'; ")
                attributes=self.cur.fetchone()
                self.cur.execute("insert into dean_database values(%s,%s,%s,%s);",attributes[0],attributes[1],attributes[2],time)
                self.cur.execute("update dean set dean_id=%s,start_time=%s,end_time=%s where dean_type='faculty affairs';",data["eid"],data["start_time"],data["end_time"])
            else:
                self.cur.execute("insert into dean values(%s,%s,%s,%s);",data["eid"],data["dept"],data["start_time"],data["end_time"])
            return True
        if data["dept"]=='associate faculty affairs':
            flag=self.cur.execute("select count(*) from dean where dean_type='associate faculty affairs';")
            flag=self.cur.fetchone()[0]
            if flag==1:
                attributes=self.cur.execute("select * from dean where dean_type='associate faculty affairs'; ")
                attributes=self.cur.fetchone()
                self.cur.execute("insert into dean_database values(%s,%s,%s,%s);",attributes[0],attributes[1],attributes[2],time)
                self.cur.execute("update dean set dean_id=%s,start_time=%s,end_time=%s where dean_type=' associate faculty affairs';",data["eid"],data["start_time"],data["end_time"])
            else:        
                self.cur.execute("insert into dean values(%s,%s,%s,%s);",data["eid"],data["dept"],data["start_time"],data["end_time"])
            return True

   # def leave(self,data):
   #     self.conn.commit()