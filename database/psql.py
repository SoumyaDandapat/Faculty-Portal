import psycopg2
from datetime import datetime


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
            print("connected")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_result(self,input):
        ans=self.cur.execute(input)
        ans=self.cur.fetchone()[0]
        return ans

    def insert(self,data):
        self.conn.commit()
        new_eid=self.get_result("SELECT id from const where id<>0;")
        #new_eid =self.cur.fetchone() [0]
        leaves=self.get_result("SELECT leaves_left from const where id<>0;")
        #leaves =self.cur.fetchone() [0]
        print(new_eid)
        flag=self.get_result("SELECT COUNT(*) from employees where email='{}'".format(data["email"]))
        #flag=self.cur.fetchone()[0]
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
        self.cur.execute("delete from leave_application ")
        self.conn.commit()
        self.cur.execute("delete from ranks ")
        self.conn.commit()
        self.cur.execute("delete from hod ")
        self.conn.commit()
        self.cur.execute("delete from dean ")
        self.conn.commit()
        self.cur.execute("delete from director")
        self.conn.commit()
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
        ans=self.get_result("select leaves_left from employees where eid={}".format(data))
        # ans=self.cur.fetchone()[0]
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
        flag=self.cur.execute("SELECT count(*) from leave_application where applicant_id={} and leave_status='p'".format(data["eid"]))
        flag=self.cur.fetchone()[0]
        #t=self.cur.execute("select {}-{};".format(data["edate"]),data["sdate"])
        temp=self.date_dif(data["sdate"],data["edate"])
        
        # data["edate"]=str(data["edate"])
        # data["sdate"]=str(data["sdate"])
        # date_format = "%Y-%m-%d"
        # a = datetime.strptime(data["edate"], date_format)
        # b = datetime.strptime(data["sdate"], date_format)
        # # fecha_2 = datetime.strptime('22/01/2019 17:00', '%d/%m/%Y %H:%M')
        # # end_date=datetime.strptime(data["edate"], ' %Y-%m-%d')
        # # start_date=datetime.strptime(data["sdate"], ' %Y-%m-%d')
        # # temp=end_date-start_date
        # temp=b-a
        if leaves_left- temp < -leaves or flag==1:
            return -1
        else :
            flag2=self.cur.execute("select count(*) from hod where hod_id={}".format(data["eid"]))
            flag2=self.cur.fetchone()[0]
            flag3=self.cur.execute("select count(*) from dean where dean_id={}".format(data["eid"]))
            flag3=self.cur.fetchone()[0]
            if flag2==0 and flag3==0:
                self.cur.execute("insert into leave_application values({},{},'{}','{}','{}',{})".format(new_lid,data["eid"],data["reason"],data["edate"],data["sdate"],1))
                self.cur.execute("update const set leave_id=leave_id+1;")
                faculty_type=self.cur.execute("select type_of_faculty from ranks where rank = 1; ")
                faculty_type=self.cur.fetchone()[0]
                #print (check1)
                dept=self.cur.execute("select dept from employees where eid={}".format(data["eid"]))
                dept=self.cur.fetchone()[0]
                if faculty_type =='HOD':
                    print(1)
                    self.cur.execute("update hod set leave_array=leave_array||{} where dept='{}'".format(new_lid,dept))
                if faculty_type =='DFA':
                    self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='DFA'".format(new_lid))
                if faculty_type =='ADFA':
                    self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='ADFA'".format(new_lid))
            else:
                self.cur.execute("insert into leave_application values({},{},'{}','{}','{}',{})".format(new_lid,data["eid"],data["reason"],data["edate"],data["sdate"],10))
                self.cur.execute("update const set leave_id=leave_id+1;")
                self.cur.execute("update director set leave_array=leave_array||{}".format(new_lid))
            return new_lid
    
    def change_leaves(self,data):
        self.conn.commit()
        self.cur.execute("UPDATE const set leaves_left= {}".format(data["leaves"]))

    def add_comment(self,eid,leave_id,comments):
        self.conn.commit()
        dept=self.get_position(eid)
        check_applicant=self.get_result("select count(*) from leave_application where leave_id={} and applicant_id={} ".format(leave_id,eid))
        if check_applicant==0:
            self.cur.execute("insert into comments values({},'{}',{},now(),'{}')".format(leave_id,dept,eid,comments))
            self.cur.execute("update leave_application set requested_state='y';")
        else:
            pos=self.get_result("select position from leave_application where leave_id={}".format(leave_id))
            faculty_type=self.get_result("select type_of_faculty from ranks where rank = {}; ".format(pos))
            #faculty_type=self.cur.fetchone()[0]
            #print (check1)
            if faculty_type =='HOD':
                # print(1)
                dept_type=self.get_result("select dept from employees where eid={}".format(eid))
                receiver=self.get_result("select hod_id from hod where dept={}".format(dept_type))
            if faculty_type =='DFA':
                receiver=self.get_result("select dean_id from dean where dean_type='DFA'")
            if faculty_type =='ADFA':
                receiver=self.get_result("select dean_id from dean where dean_type='ADFA'")
            if faculty_type =='DR':
                receiver=self.get_result("select director_id from director")
            self.cur.execute("update leave_application set requested_state='n';")
            self.cur.execute("insert into comments values({},'{}',{},now(),'{}')".format(leave_id,dept,receiver,comments))
        

    def get_position(self,eid):# 1 for hod, 2 for dean, 3 for director
        ishod=self.get_result("select count(*) from hod where hod_id={}".format(eid))
        if(ishod==1):
            return "HOD"
        isdean=self.get_result("select count(*) from dean where dean_id={} and dean_type='{}'".format(eid,"DFA"))
        if(isdean==1):
            return "DFA"
        isdir=self.get_result("select count(*) from director where director_id={}".format(eid))
        if(isdir==1):
            return "DR"
        isadean=self.get_result("select count(*) from dean where dean_id={} and dean_type='{}'".format(eid,"ADFA"))
        if(isdir==1):
            return "ADFA"
        return "F"

    def date_dif(self,s,e):
        start_date=str(s)
        end_date=str(e)
        date_format = "%Y-%m-%d"
        a = datetime.strptime(start_date, date_format)
        b = datetime.strptime(end_date, date_format)
        diff=b-a
        return diff.days

    def act_on_leave(self,eid,leave_id,state,comment):      
        
        position=self.get_position(eid)
        if(position=="F"):
            return False
        res=self.get_proccessed_leaves(eid)
        if leave_id not in res:
            return False

        time=self.get_result("select current_date")

        if state==1:#accepted
            next_position=self.get_result("select position from leave_application where leave_id={}".format(leave_id))+1
            done=self.get_result("select count(*) from ranks where rank={}".format(next_position))
            if(done==0):# completely accepeted
                sdate=self.get_result("select start_leave from leave_application where leave_id={}".format(leave_id))
                edate=self.get_result("select end_leave from leave_application where leave_id={}".format(leave_id))
                ndays=self.date_dif(sdate,edate)
                applicant_id=self.get_result("select applicant_id from leave_application where leave_id={}".format(leave_id))
                self.cur.execute("update employees set leaves_left=leaves_left-{} where eid={}".format(ndays,applicant_id))
                self.cur.excecute("update leave_application set value leave_status='a' where leave_id={}".format(applicant_id))
            else:# next person
                dept=self.get_result("select dept from employees where eid={}".format(eid))
                self.cur.execute("update leave_application set position ={} where leave_id={}".format(next_position,leave_id))
                ftype=self.get_result("select type_of_faculty from ranks where rank= {}".format(next_position))
                if ftype =='HOD':
                        self.cur.execute("update hod set leave_array=leave_array||{} where dept='{}'".format(leave_id,dept))
                if ftype =='DFA':
                    self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='DFA' ".format(leave_id))
                if ftype =='ADFA':
                    self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='ADFA' ".format(leave_id))

        elif state==0:# rejected
            self.cur.excecute("update leave_application set value leave_status='r' where leave_id={}".format(applicant_id))
        elif state==2:# requested comments
            time=self.get_result("SELECT now()")
            self.cur.excecute("update leave_application set value requested_state='y' where leave_id={}".format(applicant_id))
            self.cur.execute("insert into comment values({},{},{},{},'{}')".format(leave_id,position,eid,time,comment))
        return True
            
        
        # time=self.cur.execute("select current_date;")
        # time=self.cur.fetchone()[0]
        # check_hod=self.cur.execute("select count(*) from hod where hod_id={}".format(eid))
        # check_hod=self.cur.fectchone()[0]
        # check_dean=self.cur.execute("select count(*) from dean where dean_id={}".format(eid))
        # check_dean=self.cur.fectchone()[0]
        # check_director=self.cur.execute("select count(*) from director where director_id={}".format(eid))
        # check_director=self.cur.fectchone()[0]
        # if state==1:
        #     action='y'
        # else:
        #     action='n'
        # if state==2:
        #     self.cur.execute("update leave_application set requested_state='y';")
        # else:
        #     if check_hod == 1 or check_dean==1:
        #         temporary=self.cur.execute("select position from leave_application where leave_id={}".format(leave_id))
        #         temporary=self.cur.fetchone()[0]
        #         self.cur.execute("INSERT into paper_trail(action_taken,time_stamp,position,id,lid) values('{}','{}',{},{},{})".format(action,time,temporary,eid,leave_id))
        #         check=self.cur.execute("select count(*) from ranks where rank={}".format(temporary+1))
        #         check=self.cur.fetchone()[0]
        #         if check == 1 and state==1:
        #             self.cur.execute("update leave_application set position ={} where leave_id={}".format(temporary+1,leave_id))
        #             ftype=self.cur.execute("select type_of_faculty from ranks where rank= {}".format(temporary+1))
        #             ftype=self.cur.fetchone()[0]
        #             dept=self.cur.execute("select dept from employees where eid={}".format(eid))
        #             dept=self.cur.fetchone()[0]
        #             if ftype =='HOD':
        #                 self.cur.execute("update hod set leave_array=leave_array||{} where dept='{}'".format(leave_id,dept))
        #             if ftype =='DFA':
        #                 self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='DFA' ".format(leave_id))
        #             if ftype =='ADFA':
        #                 self.cur.execute("update dean set leave_array=leave_array||{} where dean_type='ADFA' ".format(leave_id))


        #         if check == 0 and state==1:
        #             start_date=self.cur.execute("select start_leave from leave_application where leave_id={}".format(leave_id))
        #             start_date=self.cur.fetchone()[0]
        #             end_date=self.cur.execute("select end_leave from leave_application where leave_id={}".format(leave_id))
        #             end_date=self.cur.fetchone()[0]
        #             start_date=str(start_date)
        #             end_date=str(end_date)
        #             date_format = "%Y-%m-%d"
        #             a = datetime.strptime(start_date, date_format)
        #             b = datetime.strptime(end_date, date_format)
        #             diff=b-a
        #             self.cur.execute("update leave_application set leave_status='a';")
        #             self.cur.execute("update employees set leaves_left=leaves_left-{}".format(diff.days))
        #         if state ==0:
        #             self.cur.execute("update leave_application set leave_status='r'")

        #     if check_director ==1:
        #         temp='DR'
        #         self.cur.execute("INSERT into paper_trail(action_taken,time_stamp,position,id,lid) values(%s,%s,%s,%s,%s)",action,time,temp,eid,leave_id)

    def promote(self,data):# promoting individuals
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
            flag=self.cur.fetchone()[0]
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
    def get_processed_leaves(self,eid):
        li=[]
        pos=self.get_position(eid)
        if pos=='HOD':
        # dept=self.get_result("select dept from employees where eid={}".format(eid))
            li=self.get_result("select leave_array from hod where hod_id={}".format(eid))
        if pos in ['DFA','ADFA'] :
        # dept=self.get_result("select dean_type from dean where dean_id={}".format(eid))
            li=self.get_result("select leave_array from dean where dean_id={}".format(eid))
        if pos=='DR':
            li=self.get_result("select leave_array from director where director_id={};".format(eid))
        return self.get_leave_list(li)

    def leaves_next_year(self,eid):
        leaves_left=self.get_result("select leaves_left from employees where eid={};".format(eid))
        leaves_per_year=self.get_result("select leaves_left from const where id<>0;")
        if leaves_left>0:
            return leaves_per_year
        else:
            return leaves_per_year+leaves_left

    def get_leave_history(self,eid):
        li=[]
        res=self.cur.execute("select leave_id,leave_status,reason,start_leave,end_leave from leave_application where applicant_id={}".format(eid))
        res=self.cur.fetchall()
        for x in res:
            li.append(x)
        print("in calles", li,res)
        return li

    def get_leave_details(self,eid,leave_id):
        out={}
        msg=[]
        res=self.cur.execute("select leave_id,leave_status,reason,start_leave,end_leave,applicant_id,requested_state from leave_application where leave_id={}".format(leave_id))
        res=self.cur.fetchone()
        ###
        if eid == res[5]:   #applier has requested
            msg=self.cur.execute("select * from comments where leave_id={} order by time_stamp;".format(leave_id))
            msg=self.cur.fetchall()
        
        else:   #participant
            output=self.cur.execute("select * from comments where leave_id={} and dept='{}' sort by time_stamp;".format(leave_id,self.get_position(eid)))
            output=self.cur.fetchall()
            for x in output:
                x[2]=self.get_result("select name from employees where eid={}".format(x[2]))
                msg.append(x)

        out["data"]=res
        out["msg"]=msg
        return out

        
    def get_leave_list(self,lids):
        li=[]
        for y in lids:
            # temp=[]
            res=self.cur.execute("select leave_id,leave_status,reason,start_leave,end_leave from leave_application where leave_id={}".format(y))
            res=self.cur.fetchone()
            # for x in res:
            #     temp.append(x)
            li.append(res)
        return li

    def iseligible(self,eid,leave_id):
        return True

