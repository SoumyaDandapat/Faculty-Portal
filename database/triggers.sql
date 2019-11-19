create or replace function remove_application()
returns trigger as
$$
begin
if new.leave_status='a'or new.leave_status='r' then
insert into leave_database(leave_id,eid,end_leave,reason,leave_status,comments,start_leave)
values(new.leave_id,new.applicant_id,new.end_leave,new.reason,new.leave_status,new.comment,new.start_leave);
delete from leave_application
where leave_id=new.leave_id;
end if;
return new;
end $$ language plpgsql;

-- create trigger insert_into_database
-- after update
-- on leave_application
-- for each row
-- execute procedure remove_application();

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



