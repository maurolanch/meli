from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importa la función que ya definiste
from dags.ml_token_refresh_dag import refresh_token

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='mercadolibre_token_refresh',
    default_args=default_args,
    description='Renueva access_token y refresh_token de MercadoLibre',
    schedule_interval='0 */6 * * *',  # Cada 6 horas
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['mercadolibre', 'token', 'auth'],
) as dag:

    refresh_token_task = PythonOperator(
        task_id='refresh_mercadolibre_token',
        python_callable=refresh_token,
    )

    refresh_token_task
