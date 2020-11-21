from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from dags.naver_blog_to_notion.src.rss_to_dataframe import rss_to_dataframe

with DAG(default_args={
    "author": "humphrey",
}, dag_id="naver_blog_to_notion", schedule_interval="0 0 * * *") as dag:
    rss_to_file_storage = PythonOperator(
        python_callable=rss_to_dataframe,
        task_id="rsS_to_file_storage"
    )
