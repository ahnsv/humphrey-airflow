from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

with DAG(dag_id="first_dag", start_date=days_ago(2), schedule_interval="@once") as dag:
    first_Dag_task = DummyOperator(task_id="first_dag_task")
