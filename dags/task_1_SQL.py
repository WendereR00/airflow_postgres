from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


insert_hours_sql = """
INSERT INTO case_one.employees_hours 
SELECT
	md5(employee_name)::uuid,
	tmp_date,
	hour_count
FROM t_employees
;

"""

insert_departments_sql = """
INSERT INTO case_one.departments 
SELECT 
	md5(department)::uuid,
	department
FROM t_employees GROUP BY department
;
"""

insert_positions_sql = """
INSERT INTO case_one.positions 
SELECT 
	md5(position_name)::uuid,
	position_name 
FROM t_employees GROUP BY position_name 
;
"""

insert_working_phones_sql = """
INSERT INTO case_one.working_phones
SELECT
	md5(employee_name)::uuid,
	working_phone, 
    personal_phone
    FROM t_employees 
;
"""

insert_employees_sql =  """
 INSERT INTO case_one.employees 
 SELECT 
 	md5(employee_name)::uuid,
 	md5(department)::uuid,
 	md5(position_name)::uuid,
 	staff_number,
 	employee_name,
 	to_date(birthdate, 'dd.mm.yyyy') AS birthdate,
 	personal_phone
    FROM t_employees ;
 """

#md5 Hash diff от полей
#в хранилищах foreign key может быть не использован
drop_temp_tables_sql = """
DROP TABLE IF EXISTS t_employees CASCADE;
"""

def import_meta():
    # conn = AlchemyConnector(login = 'Lazarev.AAle',
    #                         pass = ${USER_PASSWORD},
    #                         elif format = def
                            
    #                         ')
    pass

def load_data_foo():
    data = pd.read_csv("/opt/airflow/dags/case1.csv", sep=';')
    engine = create_engine(
        "postgresql+psycopg2://admin:admin@172.28.112.1:5432/postgres")
    data.columns = ['department', 'position_name', 'staff_number', 'employee_name',
                    'birthdate', 'personal_phone', 'working_phone', 'tmp_date', 'hour_count']
    data.to_sql('t_employees', engine, index=False, if_exists='replace')


with DAG(dag_id="task_1_SQL", start_date=datetime.now() , tags=["task_1", "SQL", "python"]) as dag:
    load_data = PythonOperator(
        task_id="load_data",
        python_callable=load_data_foo
    )

    update_hours = PostgresOperator(
        task_id="update_hours",
        postgres_conn_id="postgres_id",
        sql=insert_hours_sql
    )
    update_departments = PostgresOperator(
        task_id="update_departments",
        postgres_conn_id="postgres_id",
        sql=insert_departments_sql
    )

    update_positions = PostgresOperator(
        task_id="update_positions",
        postgres_conn_id="postgres_id",
        sql=insert_positions_sql
    )

    update_working_phones = PostgresOperator(
        task_id="update_working_phones",
        postgres_conn_id="postgres_id",
        sql=insert_working_phones_sql
    )

    update_employees = PostgresOperator(
        task_id="update_employees",
        postgres_conn_id="postgres_id",
        sql=insert_employees_sql
    )

    drop_temp_tables = PostgresOperator(
        task_id="drop_temp_tables",
        postgres_conn_id="postgres_id",
        sql=drop_temp_tables_sql
    )

    
    load_data >> update_departments
    load_data >> update_positions
    
    update_departments >> update_employees
    update_positions >> update_employees

    update_employees >> update_hours
    update_employees >> update_working_phones
    
    update_hours >> drop_temp_tables
    update_working_phones >> drop_temp_tables