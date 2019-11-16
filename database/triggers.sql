create or replace function remove_application()
returns trigger as
$$
begin
if new.leave_status='a'or new.leave_status='r' then
insert into leave_database(leave_id,eid,leave_day,reason,leave_status,comments)
values(new.leave_id,new.applicant_id,new.leave_day,new.reason,new.leave_status,new.comment);
delete from leave_application
where leave_id=new.leave_id;
end if;
return new;
end $$ language plpgsql;

create trigger insert_into_database
after update
on leave_application
for each row
execute procedure remove_application();

create or replace function default_eid()
returns trigger as
$$
declare
l int;
i int;
begin
select into l leaves_left from const where id<>0;
select into i id from const where id<>0;
update employees set leaves_left=l,eid=i where eid=0 ;
update const set id=id+1;
return new;
end $$ language plpgsql;

create trigger insert_into_employees
before insert
on employees
for each statement
execute procedure default_eid();

create or replace function check_passwd(id int,passwd varchar(30))
returns varchar(1) as 
$$
declare
flag int; 
p varchar(30); 
t varchar(1);
begin 
select into flag count(*) from employees where eid=id;
t='n';
if flag=1 then
select into p pwd from employees where eid=id;
if p=passwd then
t='y';
end if;
end if;
return t;
end $$ language plpgsql;

create or replace function get_id(id int,pos int)
returns int as
$$
declare
i int;
t varchar(15);
d varchar(5);
begin
select into t type_of_faculty from ranks where rank=pos;
if t='hod' then
select into d dept from employees where eid=id;
select into i hod_id from hod where dept_name=d;
end if;
if t='dean' then
select into i dean_id from dean where dean_type='faculty';
end if;
return i;
end $$ language plpgsql;

create or replace function create_leave(id int,reasons varchar(200),days_required int)
returns int as
$$
declare
t int;
c int;
l int;
flag1 int;
flag2 int;
i int;
pos int;
begin
select into c count(*) from leave_application where applicant_id=id;
t=0;
if c=0 then
select into l leave_id from const where leave_id<>0;
select into flag1 count(*) from hod where hod_id=id;
select into flag2 count(*) from dean where dean_id=id;
if flag1<>0 or flag2<>0 then
select into i director_id from director where director_id<>0;
select into pos rank from ranks where type_of_faculty='director';
insert into leave_application(leave_id,applicant_id,reason,position,administrate_id,leave_day) values(l,id,reasons,pos,i,days_required);
t=1;
end if;
if flag1=0 and flag2=0 then
i=get_id(id,1);
insert into leave_application(leave_id,applicant_id,reason,position,administrate_id,leave_day) values(l,id,reasons,1,i,days_required);
t=1;
end if;
update const set leave_id=leave_id+1;
end if;
return t;
end $$ language plpgsql;


