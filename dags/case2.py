from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import BaseOperatorMeta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import datetime , timedelta 
import requests

import psycopg2
import json



default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() 
    }
dag = DAG(
        dag_id='case2',
        default_args=default_args,
        user_defined_macros={
        'json': json
    }
    )
        
        
           
def create_table():
        
            connection = psycopg2.connect(
                user="admin",
                password="admin",
                host="172.28.112.1",
                port="5432",
                database="postgres")
            cursor = connection.cursor()
            create_table_query = '''
        DROP TABLE case2.api;
        CREATE TABLE IF NOT EXISTS case2.api (
        pageid integer PRIMARY KEY,
	    ns integer NOT NULL,
	    title varchar (100) NULL
    );'''
            cursor.execute(create_table_query)
            connection.commit()
 

def load_data():
        connection = psycopg2.connect(
                user="admin",
                password="admin",
                host="172.28.112.1",
                port="5432",
                database="postgres")
        cursor = connection.cursor()
        response = requests.get('https://ru.wikipedia.org/w/api.php?action=query&list=allpages&aplimit=500&apfrom=A&format=json').json()
        data = response
        #data_dict = dict()
        #dict = data["pageid"]["ns"]["title"] 
        for page in data["query"]["allpages"]:
            
            cursor.execute(f"""INSERT INTO case2.api (pageid, ns, title) VALUES (%s,%s,%s)""", (page["pageid"],page["ns"],f"{page['title']}")
    
    
    )
            connection.commit()
       
      

create_table = PythonOperator(
    task_id='create',
    python_callable=create_table,
    provide_context=True,
    dag=dag)


load_data = PythonOperator(
    task_id='load',
    python_callable=load_data,
    provide_context=True,
    dag=dag)
 
    


create_table>>load_data
