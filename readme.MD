  1. Aplicación REST en Python/FastAPI, construida localmente en un contenedor.                                                                                                                
      • Endpoint: POST /records
      • Cuerpo JSON:                                                                                                                                                                             
                                                                                                                                                                                                 
      ─ json                                      
           {"usuario": "nombre", "version": "1.0"}
                                                                
      • Guardará usuario, version y la fecha/hora actual en UTC.       
	  
	    API creada, desplegada y verificada correctamente.                                                                                                                                            
                                                                                                                                                                                                  
    • URL base: http://172.20.1.104:8088                                                                                                                                                          
    • Salud: GET http://172.20.1.104:8088/health                                                                                                                                                  
    • Insertar registro: POST http://172.20.1.104:8088/records                                                                                                                                    
    • Listar registros: GET http://172.20.1.104:8088/records
    • Consultar existencia: GET http://172.20.1.104:8088/records/exists?usuario=<usuario>&version=<version>
    • Documentación interactiva: http://172.20.1.104:8088/docs                                                                                                                                   
                                                                                                                                                                                                 
    Ejemplo de inserción:                                                                                                                                                                        
                                                                                                                                                                                                 
      ─ bash                                                                                                                                                                                     
      curl -X POST http://172.20.1.104:8088/records \                                                                                                                                            
        -H 'Content-Type: application/json' \                                                                                                                                                    
        -d '{"usuario":"juan","version":"1.0"}'                                                                                                                                                  
                                                                                                                                                                                                 
    La respuesta de prueba fue:                                                                                                                                                                  
                                                                                                                                                                                                 
      ─ json                                                                                                                                                                                     
      {                
        "id": 1,                                                                                                                                                                                 
        "usuario": "verificacion",                                                                                                                                                               
        "version": "1.0",                                                                                                                                                                        
        "fecha": "2026-07-30T10:40:50.610123Z"
      }                                                                                                                                                                                          
                                                                                                                                                                                                 
    El GET /records devuelve el listado de registros insertados. La base de datos SQLite se persiste en:                                                                                         

      ─ text                                                                                                                                                                                     
      /mnt/normativa/data/registros.db

    ## Consulta de existencia de un registro

    El endpoint `GET /records/exists` comprueba si hay al menos una entrada guardada con una combinación exacta de `usuario` y `version`. Es una operación de solo lectura: no crea, modifica ni elimina registros.

    **Parámetros de consulta obligatorios**
    - `usuario`: texto no vacío, entre 1 y 255 caracteres.
    - `version`: texto no vacío, entre 1 y 255 caracteres.

    **Petición de ejemplo**

      ─ bash
      curl --get 'http://172.20.1.104:8088/records/exists' \
        --data-urlencode 'usuario=juan' \
        --data-urlencode 'version=1.0'

    **Si existe una entrada con ambos valores**

      ─ json
      {"exists": true}

    **Si no existe ninguna coincidencia**

      ─ json
      {"exists": false}

    Una combinación que no existe devuelve `200 OK` con `{"exists": false}`; no se considera un error. Si falta alguno de los parámetros, está vacío o supera 255 caracteres, la API devuelve `422 Unprocessable Entity`.

    La comparación es exacta: distingue mayúsculas, minúsculas y espacios.

    El contenedor normativa-api está activo y saludable, con el puerto 8088 publicado en todas las interfaces de red. La configuración y el código están en /mnt/normativa/.   
