create table id(
    id int default 0
);

create table employees(
    eid int primary key,
    employee_name varchar(30) not null,
    pwd varchar(30) not null,
    dept varchar(5),
    leaves_left int 
);

create table hod(
    hod_id int,
    dept_name varchar(5)
    foreign key(hod_id) references employees(eid) 
);
