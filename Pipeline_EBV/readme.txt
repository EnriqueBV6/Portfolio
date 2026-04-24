PROYECTO ETL: API A GOOGLE BIGQUERY
DESCRIPCION:
Este proyecto automatiza la extraccion de datos desde una API publica y su
carga en Google Cloud Platform. Se enfoca en la limpieza de datos y la
integridad mediante procesos SQL idempotentes.

ESTRUCTURA DE ARCHIVOS:

extractor.py: Script Python con clases para extraccion y carga.

sql/transform.sql: Consulta MERGE para la capa de integracion.

captura_sandbox.png: Captura de pantalla de la tabla en BigQuery.

.gitignore: Archivo para excluir las credenciales JSON del repositorio.

TECNOLOGIAS:

Lenguaje: Python 3

Data Warehouse: Google BigQuery

Librerias: Requests, Google Cloud SDK

FLUJO DE DATOS:

EXTRACCION: Obtencion de 100 registros desde randomuser.me.

SANDBOX: Carga de datos crudos en el dataset SANDBOX_data.

INTEGRACION: Transformacion y carga final en INTEGRATION mediante
un script SQL que evita duplicados (idempotencia).

SEGURIDAD:
Las credenciales de acceso (archivo .json) han sido excluidas del
repositorio mediante .gitignore por seguridad.

Realizado por: Enrique Bodero
Fecha: 24/04/2026