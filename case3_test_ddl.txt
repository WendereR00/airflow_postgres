CREATE SCHEMA case_test AUTHORIZATION opg;
-- case_test.departments definition

-- Drop table

-- DROP TABLE case_test.departments;

CREATE TABLE case_test.departments (
	dep_id uuid NOT NULL,
	dep_name text NULL
);


-- case_test.employees definition

-- Drop table

-- DROP TABLE case_test.employees;

CREATE TABLE case_test.employees (
	emp_id uuid NOT NULL,
	f_dep_id uuid NOT NULL,
	f_pos_id uuid NOT NULL,
	emp_number int4 NOT NULL,
	employee text NOT NULL,
	birthdate text NULL,
	personal_phone varchar NULL
);


-- case_test.employees_hours definition

-- Drop table

-- DROP TABLE case_test.employees_hours;

CREATE TABLE case_test.employees_hours (
	emp_id uuid NULL,
	month_ int2 NULL,
	hours int2 NULL,
	begindate timestamp NULL DEFAULT now(),
	enddate timestamp NULL
);


-- case_test.positions definition

-- Drop table

-- DROP TABLE case_test.positions;

CREATE TABLE case_test.positions (
	pos_id uuid NOT NULL,
	pos_name text NULL
);


-- case_test.working_phones definition

-- Drop table

-- DROP TABLE case_test.working_phones;

CREATE TABLE case_test.working_phones (
	emp_id uuid NOT NULL,
	working_phone varchar(10) NULL,
	personal_phone varchar(10) NOT NULL
);