CREATE SCHEMA case_three AUTHORIZATION opg;
-- case_three.departments definition

-- Drop table

-- DROP TABLE case_three.departments;

CREATE TABLE case_three.departments (
	dep_id uuid NOT NULL,
	dep_name text NULL
);


-- case_three.employees definition

-- Drop table

-- DROP TABLE case_three.employees;

CREATE TABLE case_three.employees (
	emp_id uuid NOT NULL,
	f_dep_id uuid NOT NULL,
	f_pos_id uuid NOT NULL,
	emp_number int4 NOT NULL,
	employee text NOT NULL,
	birthdate text NULL,
	personal_phone varchar NULL
);


-- case_three.employees_hours definition

-- Drop table

-- DROP TABLE case_three.employees_hours;

CREATE TABLE case_three.employees_hours (
	emp_id uuid NULL,
	month_ int2 NULL,
	hours int2 NULL,
	begindate timestamp NULL DEFAULT now(),
	enddate timestamp NULL
);


-- case_three.positions definition

-- Drop table

-- DROP TABLE case_three.positions;

CREATE TABLE case_three.positions (
	pos_id uuid NOT NULL,
	pos_name text NULL
);


-- case_three.working_phones definition

-- Drop table

-- DROP TABLE case_three.working_phones;

CREATE TABLE case_three.working_phones (
	emp_id uuid NOT NULL,
	working_phone varchar(10) NULL,
	personal_phone varchar(10) NOT NULL
);