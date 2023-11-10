
from datetime import timedelta
from textwrap import dedent
from datetime import datetime, timedelta
from airflow.decorators import task

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import (BashOperator,
                                    DummyOperator)
from airflow.utils.dates import days_ago


today_date_str = datetime.today().date().strftime("%Y_%m_%d")

default_args = {
    'owner': 'slv',
    'depends_on_past': False,
    'email': ['apc0808@yandex.ru'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
    }

with DAG(
    dag_id = 'auto_model_cycle_test',
    default_args=default_args,
    description='beta ver',
    start_date=datetime(2023, 10, 9),
    schedule_interval=timedelta(days=2),
    catchup=False,
    tags=['transform_csv_and_learn_model']
    ) as dag:
    
    exp_site_pack = 'export {{var.value.mlflow_site_package}}'
    prjct_path = 'cd {{var.value.project_path_drom_auto}}'

    #command2 =f'echo "{{ti.xcom_push(key="k1", value="{start_date}" }}"'
    command2 ='echo {{execution_date}}'
    command3 = 'echo "{{ ti.xcom_pull(key="k1") }}" "{{ ti.xcom_pull(key="k2") }}"'
    
    task2 = BashOperator(
                task_id='xcom_push1',
                bash_command=command2,
                dag=dag,
                params={'transform' : 'transform_csv'}
                )
    task3 = BashOperator(
                task_id='test_xcom_pull',
                bash_command=command3,
                dag=dag
                )
    task2 >> task3
    
'''
    my_task = BashOperator(
    task_id='my_task',
    bash_command='echo $VAR1 $VAR2',
    env={
        "VAR1": '{{ ti.xcom_pull(key="var1")}}',
        "VAR2": '{{ ti.xcom_pull(key="var2")}}'
    },
    dag=dag
)
'''