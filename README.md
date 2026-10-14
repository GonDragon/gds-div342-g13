# TP - Arquitectura Full-Stack Contenedorizada con Docker

## Integrantes - Grupo 13
- Gonzalo Romero
- Gómez Facundo
- Facundo Morales
- Mateo Corbetto

## Estructura de Carpetas
A continuación se detalla la estructura del proyecto utilizada para organizar los contenedores, configuraciones y variables de entorno:

```text
gds-div342-g13/
├── backend/
│   ├── Dockerfile          # Configuración de la imagen para FastAPI
│   ├── requirements.txt    # Dependencias de Python
│   └── main.py             # Lógica del servidor backend
├── frontend/
│   ├── Dockerfile          # Configuración de la imagen para Nginx
│   ├── default.conf        # Configuración de Nginx (Proxy y CORS)
│   └── index.html          # Interfaz web principal
├── .env.example            # Plantilla de variables de entorno (BD, credenciales)
├── docker-compose.yml      # Orquestación de servicios (Redes, Volúmenes, Healthchecks)
└── README.md               # Documentación e integrantes del proyecto
