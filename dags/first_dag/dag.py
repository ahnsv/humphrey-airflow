from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

with DAG(dag_id="first_dag", start_date=days_ago(2), schedule_interval="@once") as dag:
    first_dag_task_1 = DummyOperator(task_id="first_dag_task")
    first_dag_task_2 = BashOperator(task_id="first_dag_task_2", bash_command="sleep 5")
    first_dag_task_1 >> first_dag_task_2
