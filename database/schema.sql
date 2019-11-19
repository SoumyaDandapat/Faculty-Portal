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
    dept varchar(20),
	start_time date,
    end_time date,
    leave_array int array,
    foreign key(hod_id) references employees(eid) 
);

create table dean(
    dean_id int,
    dean_type varchar(40),
	start_time date,
    end_time date,
    leave_array int array,
    foreign key(dean_id) references employees(eid)
);

create table leave_application(
    leave_id int primary key default 0,
	applicant_id int,
    reason varchar(200),
    end_leave date,
    start_leave date, 
	position int,
	--administrate_id int,
    requested_state varchar(1) default 'n',
    --comment varchar(200),
    leave_status varchar(1) default 'p',
	--foreign key(administrate_id) references employees(eid),
	--foreign key(applicant_id) references employees(eid)
);

create table ranks(
    rank int unique,
    type_of_faculty varchar(15) primary key
);
-- dean = dean
-- associate dean = adean
-- director = director
-- hod=hod 

create table leave_database(
    leave_id int,
    eid int,
    end_leave date,
    start_leave date,
    reason varchar(200),
    leave_status varchar(1),
-- comments varchar(200),
);

create table director(
    director_id int,
	start_time date,
    end_time date,
    leave_array int array,
    foreign key(director_id) references employees(eid)
);

create table dean_database(
    dean_id int,
    dean_type varchar(15),
	start_time date,
    end_time date   
);

create table hod_database(
    hod_id int,
    dept varchar(5),
	start_time date,
    end_time date
);

create table paper_trail(
    action_taken varchar(1),
    time_stamp date,
    position varchar(20),
    id int,
    lid int
);

create table employees_database(
    eid int,
    name varchar(20),
    email varchar(50) unique,
    dept varchar(5),
    dob date,
    gender varchar(1) 
);

create table comments(
    leave_id int,
    dept varchar(10),
    eid int ,
    time_stamp TIMESTAMP,
    comments varchar(200),
    direction int
    -- o for question
    -- 1 for answer
    -- FOREIGN key("leave") REFERENCES leave_application("leave_id")
    -- FOREIGN key("eid") REFERENCES employees
);


create table director_database(
    director_id int,
	start_time date,
    end_time date
);

insert into const values(201700,1,10);
