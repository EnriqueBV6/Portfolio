from airflow import DAG
from airflow.operators.dummy import DummyOperator # O EmptyOperator según versión
from airflow.models import BaseOperator
from datetime import datetime, timedelta
import logging

# 1) Definición del DAG y argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(1900, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# 4) Operador personalizado TimeDiff
class TimeDiffOperator(BaseOperator):
    """
    Operador que recibe una fecha y muestra la diferencia con la actual.
    """
    def __init__(self, diff_date: datetime, **kwargs):
        super().__init__(**kwargs)
        self.diff_date = diff_date

    def execute(self, context):
        now = datetime.now()
        diff = now - self.diff_date
        print(f"Diferencia calculada: {diff}")
        return diff

# 5) RESPUESTA A PREGUNTA TEÓRICA:
# Un Hook es lo  que facilita la interacción con una plataforma como BQ.
# Una Conexión son las credenciales (user, pass, host) almacenadas en Airflow.
# La conexión es como el ADN que el Hook necesita para funcionar, mientras que el Hook es la maquinaria que hace el trabajo.

with DAG(
    'test',
    default_args=default_args,
    description='DAG para prueba tecnica',
    schedule_interval='0 3 * * *', # Ejecución diaria a las 03:00 UTC
    catchup=False
) as dag:

    # 2) Tareas start y end
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # 3) Lista de tareas task_n (Ejemplo con N=5)
    # Requisito: Cada tarea par depende de TODAS las impares
    n_total = 5
    tasks = [DummyOperator(task_id=f'task_{i}') for i in range(1, n_total + 1)]
    
    impares = [t for i, t in enumerate(tasks, 1) if i % 2 != 0]
    pares = [t for i, t in enumerate(tasks, 1) if i % 2 == 0]

    # Establecer dependencias de pares respecto a todas las impares
    for p in pares:
        impares >> p

    # 4) Tarea con el nuevo operador TimeDiff
    tarea_diff = TimeDiffOperator(
        task_id='tarea_time_diff',
        diff_date=datetime(2023, 1, 1)
    )

    # Flujo completo
    start >> impares
    pares >> tarea_diff >> end