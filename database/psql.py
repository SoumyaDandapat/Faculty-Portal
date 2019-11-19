import psycopg2
from datetime import datetime
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

        try:
            self.cur.execute("CREATE TABLE employees(eid int,name varchar(50),pass varchar(50),gender varchar(1),dob date)")
            self.conn.commit()
        except:
            print(1)
        try:
            self.cur.execute("CREATE TABLE eidmax(num int)")
            self.conn.commit()
        except:
            print(2)

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
        # print(ans)
        if ans[0] == 'y':
            return True
        return False

    def get_leaves(self,data):
        ans=self.cur.execute("select leaves_left from employees where eid={}".format(data))
        ans=self.cur.fetchone()[0]
        if ans < 0:
            return 0
        else:
            return ans
    
    def apply_leave(self,data):
        self.conn.commit()
        new_lid=self.cur.execute("SELECT leave_id from const where id<>0;")
        new_lid =self.cur.fetchone() [0]
        leaves=self.cur.execute("SELECT leaves_left from const where id<>0;")
        leaves =self.cur.fetchone() [0]
        leaves_left=self.cur.execute("SELECT leaves_left from employees where eid={};".format(data["eid"]))
        leaves_left=self.cur.fetchone()[0]
        flag=self.cur.execute("SELECT count(*) from leave_application where applicant_id={}".format(data["eid"]))
        flag=self.cur.fetchone()[0]
        #t=self.cur.execute("select {}-{};".format(data["edate"]),data["sdate"])
        data["edate"]=str(data["edate"])
        data["sdate"]=str(data["sdate"])
        date_format = "%Y-%m-%d"
        a = datetime.strptime(data["edate"], date_format)
        b = datetime.strptime(data["sdate"], date_format)
        # fecha_2 = datetime.strptime('22/01/2019 17:00', '%d/%m/%Y %H:%M')
        # end_date=datetime.strptime(data["edate"], ' %Y-%m-%d')
        # start_date=datetime.strptime(data["sdate"], ' %Y-%m-%d')
        # temp=end_date-start_date
        temp=b-a
        if leaves_left- temp.days < -leaves or flag==1:
            return -1
        else :
            flag2=self.cur.execute("select count(*) from hod where hod_id={}".format(data["eid"]))
            flag2=self.cur.fetchone()[0]
            flag3=self.cur.execute("select count(*) from dean where dean_id={}".format(data["eid"]))
            flag3=self.cur.fetchone()[0]
            if flag2==0 and flag3==0:
                self.cur.execute("insert into leave_application values({},{},'{}','{}','{}',{})".format(new_lid,data["eid"],data["reason"],data["edate"],data["sdate"],1))
                check1=self.cur.execute("select type_of_faculty from ranks where rank = 1; ")
                check1=self.cur.fetchone()[0]
                if check1 =='HOD':
                    self.cur.execute("update hod set leave_array=leave_array||{} where dept={}".format(data["leave_id"],data["dept"]))
                if check1 =='DFA':
                    self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='DFA'".format(data["leave_id"]))
                if check1 =='ADFA':
                    self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='ADFA'".format(data["leave_id"]))
            else:
                self.cur.execute("insert into leave_application values({},{},'{}','{}','{}',{})".format(new_lid,data["eid"],data["reason"],data["edate"],data["sdate"],10))
                self.cur.execute("update director set leave_array=leave_array||{}".format(data["leave_id"]))
            self.cur.execute("update const set leave_id=leave_id+1;")
            return new_lid
    
    def change_leaves(self,data):
        self.conn.commit()
        self.cur.execute("UPDATE const set leaves_left= {}".format(data["leaves"]))

    def add_comment(self,data):
        self.conn.commit()
        comment=self.cur.execute("SELECT comment from leave_application where leave_id=%s".format(data["leave_id"]))
        comment=self.cur.fetchone()[0]
        employee_name=self.cur.execute("SELECT name from employees where eid=%s",data["eid"])
        employee_name=self.cur.fetchone()[0]
        comment=comment+'&'+employee_name+data["new_comment"]
        self.cur.execute("update leave_application set comment=%s where leave_id=%s",comment,data["leave_id"])

    def change_route(self,data):
        return True

    def act_on_leave(self,eid,leave_id,state):
        self.conn.commit()
        time=self.cur.execute("select current_date;")
        time=self.cur.fetchone()[0]
        check_hod=self.cur.execute("select count(*) from hod where hod_id={}".format(eid))
        check_hod=self.cur.fectchone()[0]
        check_dean=self.cur.execute("select count(*) from dean where dean_id={}".format(eid))
        check_dean=self.cur.fectchone()[0]
        check_director=self.cur.execute("select count(*) from director where director_id={}".format(eid))
        check_director=self.cur.fectchone()[0]
        if state==1:
            action='y'
        else:
            action='n'
        if state==2:
            self.cur.execute("update leave_application set requested_state='y';")
        else:
            if check_hod == 1 or check_dean==1:
                temporary=self.cur.execute("select position from leave_application where leave_id={}".format(leave_id))
                temporary=self.cur.fetchone()[0]
                self.cur.execute("INSERT into paper_trail(action_taken,time_stamp,position,id,lid) values('{}','{}',{},{},{})".format(action,time,temporary,eid,leave_id))
                check=self.cur.execute("select count(*) from ranks where rank={}".format(temporary+1))
                check=self.cur.fetchone()[0]
                if check == 1 and state==1:
                    self.cur.execute("update leave_application set position ={} where leave_id={}".format(temporary+1,leave_id))
                    ftype=self.cur.execute("select type_of_faculty from ranks where rank= {}".format(temporary+1))
                    ftype=self.cur.fetchone()[0]
                    dept=self.cur.execute("select dept from employees where eid={}".format(eid))
                    dept=self.cur.fetchone()[0]
                    if ftype =='HOD':
                        self.cur.execute("update hod set leave_array=leave_array||{} where dept='{}'".format(leave_id,dept))
                    if ftype =='DFA':
                        self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='DFA' ".format(leave_id))
                    if ftype =='ADFA':
                        self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='ADFA' ".format(leave_id))


                if check == 0 and state==1:
                    start_date=self.cur.execute("select start_leave from leave_application where leave_id={}".format(leave_id))
                    start_date=self.cur.fetchone()[0]
                    end_date=self.cur.execute("select end_leave from leave_application where leave_id={}".format(leave_id))
                    end_date=self.cur.fetchone()[0]
                    start_date=str(start_date)
                    end_date=str(end_date)
                    date_format = "%Y-%m-%d"
                    a = datetime.strptime(start_date, date_format)
                    b = datetime.strptime(end_date, date_format)
                    diff=b-a
                    self.cur.execute("update leave_application set leave_status='a';")
                    self.cur.execute("update employees set leaves_left=leaves_left-{}".format(diff.days))
                if state ==0:
                    self.cur.execute("update leave_application set leave_status='r'")

            if check_director ==1:
                temp='DR'
                self.cur.execute("INSERT into paper_trail(action_taken,time_stamp,position,id,lid) values(%s,%s,%s,%s,%s)",action,time,temp,eid,leave_id)

    def promote(self,data):
        self.conn.commit()
        department=self.cur.execute("select dept from employees where eid={};".format(data["eid"]))
        department=self.cur.fetchone()[0]

        time=self.cur.execute("select current_date;")
        time=self.cur.fetchone()[0]

        if data["dept"] in ["CSE",'EE','ME']: # hod condition
            if(data["dept"]!=department):
                return False
            replace_cond=self.cur.execute("select count(*) from hod where dept='{}';".format(data["dept"]))
            replace_cond=self.cur.fetchone()[0]

            if(replace_cond==1):
                attributes=self.cur.execute("select * from hod where dept='{}';".format(data["dept"]))
                attributes=self.cur.fetchone()
                self.cur.execute("insert into hod_database values({},'{}','{}','{}');".format(attributes[0],attributes[1],attributes[2],time))
                self.cur.execute("update hod set hod_id={},start_time='{}',end_time='{}' where dept='{}';".format(data["eid"],data["start_time"],data["end_time"],data["dept"]))
                
            else:
                self.cur.execute("insert into hod values({},'{}','{}','{}');".format(data["eid"],data["dept"],data["start_time"],data["end_time"]))
                
            return True

        if data["dept"]=='DR':
            flag=self.cur.execute("select count(*) from director;")
            flag=self.cur.fectchone()[0]
            if flag==1:#replace condition
                attributes=self.cur.execute("select * from director;")
                attributes=self.cur.fetchone()
                self.cur.execute("insert into director_database values({},'{}','{}');".format(attributes[0],attributes[1],time))
                self.cur.execute("update director set director_id={},start_time='{}',end_time='{}';".format(data["eid"],data["start_time"],data["end_time"]))
            else:
                self.cur.execute("insert into director values({},'{}','{}');".format(data["eid"],data["start_time"],data["end_time"]))
            return True
        if data["dept"]=='DFA':
            flag=self.cur.execute("select count(*) from dean where dean_type='DFA';")
            flag=self.cur.fetchone()[0]
            if flag==1:
                attributes=self.cur.execute("select * from dean where dean_type='DFA'; ")
                attributes=self.cur.fetchone()
                self.cur.execute("insert into dean_database values({},'{}','{}','{}');".format(attributes[0],attributes[1],attributes[2],time))
                self.cur.execute("update dean set dean_id={},start_time='{}',end_time='{}' where dean_type='DFA';",data["eid"],data["start_time"],data["end_time"])
            else:
                self.cur.execute("insert into dean values({},'{}','{}','{}');".format(data["eid"],data["dept"],data["start_time"],data["end_time"]))
            return True
        if data["dept"]=='ADFA':
            flag=self.cur.execute("select count(*) from dean where dean_type='ADFA';")
            flag=self.cur.fetchone()[0]
            if flag==1:
                attributes=self.cur.execute("select * from dean where dean_type='ADFA'; ")
                attributes=self.cur.fetchone()
                self.cur.execute("insert into dean_database values({},'{}','{}','{}');".format(attributes[0],attributes[1],attributes[2],time))
                self.cur.execute("update dean set dean_id={},start_time='{}',end_time='{}' where dean_type='ADFA';".format(data["eid"],data["start_time"],data["end_time"]))
            else:        
                self.cur.execute("insert into dean values({},'{}','{}','{}');".format(data["eid"],data["dept"],data["start_time"],data["end_time"]))
            return True

    def change_route(self,first,second):
        self.conn.commit()
        self.cur.execute("delete from ranks where rank<>10;")
        print (first,second)
        if first=='HOD':
            self.cur.execute("insert into ranks values(1,'HOD');")
        if first=='DFA':
            self.cur.execute("insert into ranks values(1,'DFA');")
        if first=='ADFA':
            self.cur.execute("insert into ranks values(1,'ADFA');")
        if second=='HOD':
            self.cur.execute("insert into ranks values(2,'HOD');")
        if second=='DFA':
            self.cur.execute("insert into ranks values(2,'DFA');")
        if second=='ADFA':
            self.cur.execute("insert into ranks values(2,'ADFA');")

    # def leave_next_year(self,data):