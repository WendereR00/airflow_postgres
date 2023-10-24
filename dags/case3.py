from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


delete_rows1_sql = """

DELETE FROM case_three.employees_hours;
DELETE FROM case_three.employees;
DELETE FROM case_three.positions;
DELETE FROM case_three.departments;
DELETE FROM case_three.working_phones;

"""
delete_rows2_sql = """

DELETE FROM case_test.employees_hours;
DELETE FROM case_test.employees;
DELETE FROM case_test.positions;
DELETE FROM case_test.departments;
DELETE FROM case_test.working_phones;

"""

insert_all_to_case3_sql = """
INSERT INTO case_three.departments
SELECT *
FROM case_test.departments;


INSERT INTO case_three.positions
SELECT *
FROM case_test.positions;


INSERT INTO case_three.employees
SELECT *
FROM case_test.employees;


INSERT INTO case_three.employees_hours
SELECT *
FROM case_test.employees_hours;


INSERT INTO case_three.working_phones
SELECT *
FROM case_test.working_phones

;

"""




def load_data_departments():
    engine1 = create_engine(
        "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgres")
    df1 = pd.read_sql("SELECT * FROM case_one.departments", engine1)
    engine2 = create_engine(
    "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgre")
    data=df1
    
    data.to_sql('departments', engine2, schema='case_test',index=False, if_exists='append')
    
    

def load_data_positions():
    engine3 = create_engine(
        "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgres")
    df2 = pd.read_sql("SELECT * FROM case_one.positions", engine3)
    engine4 = create_engine(
    "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgre")
    df2.to_sql('positions', engine4, schema='case_test',index=False, if_exists='append')

def load_data_employees():
    engine5 = create_engine(
        "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgres")
    df3 = pd.read_sql("SELECT * FROM case_one.employees", engine5)
    engine6 = create_engine(
    "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgre")
    df3.to_sql('employees', engine6, schema='case_test',index=False, if_exists='append')

def load_data_employees_hours():
    engine7 = create_engine(
        "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgres")
    df4 = pd.read_sql("SELECT * FROM case_one.employees_hours", engine7)
    engine8 = create_engine(
    "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgre")
    df4.to_sql('employees_hours', engine8, schema='case_test',index=False, if_exists='append')

def load_data_working_phones():
    engine9 = create_engine(
        "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgres")
    df5 = pd.read_sql("SELECT * FROM case_one.working_phones", engine9) 
    engine10 = create_engine(
    "postgresql+psycopg2://pols1:pols1@172.28.112.1:5432/postgre")
    df5.to_sql('working_phones', engine10, schema='case_test',index=False, if_exists='append')





with DAG(dag_id="case3", start_date=datetime.now() , tags=["task_3", "SQL", "python"]) as dag:    
     insert_all = PostgresOperator(
        task_id="insert_all",
        postgres_conn_id="pols2",
        sql=insert_all_to_case3_sql
     )
     
     delete_rows1 = PostgresOperator(
        task_id="delete_rows1",
        postgres_conn_id="pols2",
        sql=delete_rows1_sql
    )
     delete_rows2 = PostgresOperator(
        task_id="delete_rows2",
        postgres_conn_id="pols1",
        sql=delete_rows1_sql
    )
     load_departments = PythonOperator(
        task_id="load_departments",
        python_callable=load_data_departments
     )
     load_positions = PythonOperator(
        task_id="load_positions",
        python_callable=load_data_positions
     )
     load_employees = PythonOperator(
        task_id="load_employees",
        python_callable=load_data_employees
     )
     load_employees_hours = PythonOperator(
        task_id="load_employees_hours",
        python_callable=load_data_employees_hours
     )
     load_working_phones = PythonOperator(
        task_id="load_working_phones",
        python_callable=load_data_working_phones
     )
     
     load_departments >> delete_rows1
     load_positions >> delete_rows1
     load_employees_hours >> delete_rows1
     load_employees >> delete_rows1
     load_working_phones >> delete_rows1



     delete_rows1 >> delete_rows2
     delete_rows2 >> insert_all