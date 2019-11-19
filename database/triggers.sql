
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



