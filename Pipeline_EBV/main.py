import requests
import os
from google.cloud import bigquery

# ==========================================================
# CONFIGURACIÓN DE CREDENCIALES
# ==========================================================
# Asegúrate de que el archivo JSON esté en la misma carpeta
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "clave_bq.json"

# --- CLASE 1: EXTRACCIÓN (API) ---
class TelcoAPIExtractor:
    """Clase para extraer datos de clientes desde una API pública."""
    
    def __init__(self):
        self.url = "https://randomuser.me/api/?results=100&nat=es"

    def get_data(self):
        print("📡 Extrayendo datos de la API...")
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            raw_data = response.json()['results']
            
            # Limpieza y transformación a formato BigQuery
            cleaned_data = [
                {
                    'id': i + 1,  # Genera IDs del 1 al 100
                    'client_name': f"{u['name']['first']} {u['name']['last']}",
                    'phone': u['phone'],
                    'email': u['email'],
                    'city': u['location']['city'],
                    'consumption_mb': 500  # Valor simulado
                } for i, u in enumerate(raw_data)
            ]
            return cleaned_data
        except Exception as e:
            print(f"❌ Error en la extracción: {e}")
            return []

# --- CLASE 2: CARGA (BigQuery) ---
class BigQueryLoader:
    """Clase para cargar datos limpios en una tabla de BigQuery."""
    
    def __init__(self, project_id):
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id

    def load(self, data, dataset_id, table_id):
        table_ref = f"{self.project_id}.{dataset_id}.{table_id}"
        print(f"📦 Cargando {len(data)} registros en {table_ref}...")
        
        # insert_rows_json es el método recomendado para inserciones rápidas
        errors = self.client.insert_rows_json(table_ref, data)
        
        if not errors:
            print("✅ ¡Éxito! Datos subidos correctamente.")
        else:
            print(f"❌ Errores encontrados al insertar: {errors}")
        return errors

# --- BLOQUE PRINCIPAL (Orquestación) ---
if __name__ == "__main__":
    # Sustituye con tu ID de proyecto real
    ID_PROYECTO = "project-d71b673a-2834-4ee2-bd8"
    DATASET = "SANDBOX_data"
    TABLA = "clientes"

    # 1. Extraer
    extractor = TelcoAPIExtractor()
    datos_para_subir = extractor.get_data()

    if datos_para_subir:
        # 2. Cargar
        loader = BigQueryLoader(ID_PROYECTO)
        loader.load(datos_para_subir, DATASET, TABLA)