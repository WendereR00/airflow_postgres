-- DROP SCHEMA case_one;

CREATE SCHEMA case_one AUTHORIZATION opg;
-- case_one.departments definition

-- Drop table

-- DROP TABLE case_one.departments;

CREATE TABLE case_one.departments (
	dep_id uuid NOT NULL,
	dep_name text NULL,
	CONSTRAINT department_pkey PRIMARY KEY (dep_id)
);


-- case_one.positions definition

-- Drop table

-- DROP TABLE case_one.positions;

CREATE TABLE case_one.positions (
	pos_id uuid NOT NULL,
	pos_name text NULL,
	CONSTRAINT position_pkey PRIMARY KEY (pos_id)
);


-- case_one.employees definition

-- Drop table

-- DROP TABLE case_one.employees;

CREATE TABLE case_one.employees (
	emp_id uuid NOT NULL,
	f_dep_id uuid NOT NULL,
	f_pos_id uuid NOT NULL,
	emp_number int4 NOT NULL,
	employee text NOT NULL,
	birthdate text NULL,
	personal_phone varchar NULL,
	CONSTRAINT employee_pkey PRIMARY KEY (emp_id),
	CONSTRAINT fd_employee_position FOREIGN KEY (f_pos_id) REFERENCES case_one.positions(pos_id),
	CONSTRAINT fk_employee_department FOREIGN KEY (f_dep_id) REFERENCES case_one.departments(dep_id)
);


-- case_one.employees_hours definition

-- Drop table

-- DROP TABLE case_one.employees_hours;

CREATE TABLE case_one.employees_hours (
	emp_id uuid NULL,
	month_ int2 NULL,
	hours int2 NULL,
	begindate timestamp NULL DEFAULT now(),
	enddate timestamp NULL,
	CONSTRAINT fk_timesheet_employee FOREIGN KEY (emp_id) REFERENCES case_one.employees(emp_id)
);


-- case_one.working_phones definition

-- Drop table

-- DROP TABLE case_one.working_phones;

CREATE TABLE case_one.working_phones (
	emp_id uuid NOT NULL,
	working_phone varchar(10) NULL,
	personal_phone varchar(10) NOT NULL,
	CONSTRAINT fk_phones_employee FOREIGN KEY (emp_id) REFERENCES case_one.employees(emp_id)
);