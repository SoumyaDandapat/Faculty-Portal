create table id(
    id int default 0
);

create table leave_id(
    leave_id int default 0
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
    dept_name varchar(5),
    foreign key(hod_id) references employees(eid) 
);

create table dean(
    dean_id int,
    dean_type varchar(15),
    foreign key(dean_id) references employees(eid)
);

create table hod_status(
    hod_dept_name varchar(15),
    start_time time,
    end_time time 
);

create table dean_status(
    dtype varchar(15),
    start_time time,
    end_time time
);

create table leave_application(
    leave_id int primary key,
    leave_status varchar(1) default "n",
)
create table applicant(
    leave_id int,
    applicant_id int,
    reason varchar(200),
    day int,
    foreign key(leave_id) references leave_application(leave_id),
    foreign key(applicant_id) references employees(eid)
);

create table administrate(
    administrate_id int,
    comment varchar(200),
    leave_id int,
    foreign key(administrate_id) references employees(eid),
    foreign key(leave_id) references leave_application(leave_id)
);

create table ranks(
    rank int unique,
    type_of_faculty varchar(15) primary key
);

create table leave_database(
    leave_id int,
    eid int,
    reason varchar(200),
    status varchar(1),
    comments varchar(200),
    foreign key(leave_id) references leave_application(leave_id),
    foreign key(eid) references employees(eid)
);


