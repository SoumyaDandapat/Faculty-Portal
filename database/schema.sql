create table const(
    id int default 0,
	leave_id int default 0,
    leaves_left int default 10
);

create table employees
(
    eid int primary key default 0,
    name varchar(20),
    pwd varchar(30) not null,
    email varchar(50) unique,
    dept varchar(5),
    dob date,
    gender varchar(1),
    leaves_left int 
);

create table hod
(   
    hod_id int,
    dept_name varchar(5),
	start_time time,
    end_time time,
    foreign key(hod_id) references employees(eid) 
);

create table dean(
    dean_id int,
    dean_type varchar(15),
	start_time time,
    end_time time,
    foreign key(dean_id) references employees(eid)
);

create table leave_application(
    leave_id int primary key default 0,
	applicant_id int,
    reason varchar(200),
    leave_day int,
	position int,
	administrate_id int,
    comment varchar(200),
    leave_status varchar(1) default 'n',
	foreign key(administrate_id) references employees(eid),
	foreign key(applicant_id) references employees(eid)
);

create table ranks(
    rank int unique,
    type_of_faculty varchar(15) primary key
);

create table leave_database(
    leave_id int,
    eid int,
    leave_day int,
    reason varchar(200),
    leave_status varchar(1),
    comments varchar(200),
    foreign key(eid) references employees(eid)
);

create table director(
    director_id int,
	start_time time,
    end_time time,
    foreign key(director_id) references employees(eid)
);

insert into const values(2017000,1,10);
