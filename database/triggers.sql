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

