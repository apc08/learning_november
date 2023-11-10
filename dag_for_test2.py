
from datetime import timedelta
from textwrap import dedent
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

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
    dag_id = 'auto_ML_pipeline',
    default_args=default_args,
    description='beta ver',
    start_date=datetime(2023, 10, 23),
    schedule_interval=timedelta(days=2),
    catchup=True,
    tags=['transform_csv_and_learn_model']
    ) as dag:
    
    exp_site_pack = 'export {{var.value.mlflow_site_package}}'
    prjct_path = 'cd {{var.value.project_path_drom_auto}}'
    
    
    command_1 = 'python transform_csv.py'
    command_2 = 'python learning_drom_auto.py'
    command_3 = 'python best_model_selection.py'
    environment_var = {'PYTHONPATH':'/home/slava/anaconda3/envs/mlflowenv23/lib/python3.9/site-packages'}
    #command2 = f'{exp_site_pack} && {prjct_path} && python transform_csv.py '
    #command3 = f'{exp_site_pack} && {prjct_path} && python learning_drom_auto.py '
    #command4 = f'{exp_site_pack} && {prjct_path} && python best_model_selection.py '
    
    
    working_dir = '/home/projects/autoapr'
    
    transform_parsed_CSV = BashOperator(
            task_id='drom_auto_pipeline',
            bash_command=command_1,
            env=environment_var,
            append_env=True,
            cwd=working_dir
            )
    learn_drom_model_last_data = BashOperator(
            task_id='learn_drom_model_last_data',
            bash_command=command_2,
            env=environment_var,
            append_env=True,
            cwd=working_dir
            )
    best_model_selection = BashOperator(
            task_id='best_model_selection',
            bash_command=command_3,
            env=environment_var,
            append_env=True,
            cwd=working_dir
            )

    transform_parsed_CSV >> learn_drom_model_last_data >> best_model_selection
