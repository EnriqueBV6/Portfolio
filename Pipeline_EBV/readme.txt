PROYECTO ETL: API A GOOGLE BIGQUERY + ORQUESTACION AIRFLOW
DESCRIPCION:
Este proyecto automatiza la extraccion de datos desde una API publica y su
carga en Google Cloud Platform. Incluye la orquestacion del flujo mediante
un DAG de Airflow, asegurando integridad con procesos SQL idempotentes.

ESTRUCTURA DE ARCHIVOS:

extractor.py: Script Python con clases para extraccion y carga.

sql/transform.sql: Consulta MERGE para la capa de integracion.

dags/airflow_test.py: Definicion del DAG, operadores y dependencias.

captura_sandbox.png: Captura de pantalla de la tabla en BigQuery.

.gitignore: Archivo para excluir las credenciales JSON del repositorio.

TECNOLOGIAS:

Lenguaje: Python 3

Data Warehouse: Google BigQuery

Orquestador: Apache Airflow

Librerias: Requests, Google Cloud SDK

FLUJO DE DATOS Y ORQUESTACION:

EXTRACCION: Obtencion de 100 registros desde randomuser.me.

SANDBOX: Carga de datos crudos en el dataset SANDBOX_data.

INTEGRACION: Transformacion mediante SQL MERGE (idempotente).

AIRFLOW:

DAG "test" programado a las 3:00 UTC.

Implementacion de dependencias complejas (tareas pares vs impares).

Operador personalizado "TimeDiff" para calculo de fechas.

Incluye la respuesta teórica

SEGURIDAD:
Las credenciales de acceso (archivo .json) han sido excluidas del
repositorio mediante .gitignore por seguridad.

Realizado por: Enrique Bodero
Fecha: 24/04/2026