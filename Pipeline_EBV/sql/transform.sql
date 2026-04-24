-- 1. Aseguramos que la tabla de destino existe (si no la creaste antes)
-- 2. Transformación e Inserción Idempotente
MERGE `project-d71b673a-2834-4ee2-bd8.INTEGRATION.integration_prueba_tecnica` T
USING (
  SELECT DISTINCT
    id,
    client_name,
    phone,
    email,
    city,
    consumption_mb,
    CURRENT_TIMESTAMP() as transformation_at -- Columna de fecha de ejecución
  FROM `project-d71b673a-2834-4ee2-bd8.SANDBOX_data.clientes`
) S
ON T.id = S.id
WHEN MATCHED THEN
  UPDATE SET 
    client_name = S.client_name,
    phone = S.phone,
    email = S.email,
    city = S.city,
    consumption_mb = S.consumption_mb,
    transformation_at = S.transformation_at
WHEN NOT MATCHED THEN
  INSERT (id, client_name, phone, email, city, consumption_mb, transformation_at)
  VALUES (id, client_name, phone, email, city, consumption_mb, transformation_at);