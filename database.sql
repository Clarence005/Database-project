set echo on;
clear screen;
drop table patient;
drop table doctor;
drop table check_datas;
create table patient(pat_id varchar(50),name varchar(50),personal_details varchar(50),phone varchar(50),disease varchar(50),Treatment varchar(50),department varchar(50),doctor_id varchar(50),primary key(pat_id));
create table doctor(doctor_id varchar(50),name varchar(50),phone varchar(50),department varchar(50),patient_id varchar(50) primary key(doctor_id));
create table chec_datas(doctor_id varchar(50),pat_id varchar(50));
alter table check_datas
add constraint ck_fk foreign key (doctor_id) references doctor(doct_id);
alter table check_datas
add constraint pk_fk foreign key (pat_id) references patient(pat_id);
