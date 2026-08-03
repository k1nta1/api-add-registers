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
                                                                                                                                                                                                 
    El contenedor normativa-api está activo y saludable, con el puerto 8088 publicado en todas las interfaces de red. La configuración y el código están en /mnt/normativa/.   
