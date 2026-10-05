# Sistema RAG Production-Ready (Streamlit + FastAPI + ChromaDB + Google AI)

Este proyecto implementa un sistema de Recuperación y Generación Aumentada por Inteligencia Artificial (RAG) con arquitectura desacoplada, almacenamiento vectorial persistente y mecanismos estrictos de citación y abstención.

## Requisitos del Sistema
- Sistema Operativo: Windows 10 / 11 (PowerShell o CMD)
- Python: versión 3.10 o superior
- Clave de API de Google AI (Gemini API Key)

---

## Guía de Instalación y Ejecución Paso a Paso

### Paso 1: Navegar al Directorio Raíz del Proyecto
Abra Windows PowerShell o el Símbolo del sistema (CMD) y diríjase a la ruta base:
```powershell
cd C:\Users\Raul\Projecto-Final
```

### Paso 2: Crear y Activar el Entorno Virtual Python
Creación del entorno virtual:
```powershell
python -m venv venv
```

Activación en PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

Activación en CMD:
```cmd
venv\Scripts\activate.bat
```

### Paso 3: Instalar Dependencias
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno
Cree el archivo `.env` a partir de la plantilla provista:
```powershell
copy .env.example .env
```

Edite el archivo `.env` para asignar su clave de API de Google AI:
```env
GOOGLE_API_KEY=tu_clave_de_api_real_aqui
CHROMA_PATH=C:\Users\Raul\Projecto-Final\chroma
API_HOST=127.0.0.1
API_PORT=8000
EMBEDDING_MODEL=text-embedding-004
GENERATION_MODEL=gemini-2.5-flash
ABSTENTION_DISTANCE_THRESHOLD=0.65
```

---

## Ejecución del Sistema

### Opción A: Iniciar el Servidor API FastAPI (Puerto 8000)
En una ventana de terminal con el entorno virtual activado:
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
La documentación interactiva OpenAPI estará disponible en `http://127.0.0.1:8000/docs`.

### Opción B: Iniciar la Interfaz de Usuario Streamlit (Puerto 8501)
En una segunda ventana de terminal con el entorno virtual activado:
```powershell
cd C:\Users\Raul\Projecto-Final
.\venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py --server.port 8501
```
La interfaz web abrirá automáticamente en `http://localhost:8501`.

---

## Pruebas de Funcionamiento

### 1. Ingesta Inicial del Corpus de Ejemplo
Desde la pestaña "Ingesta de Documentos" en Streamlit, o mediante sintaxis cURL en PowerShell:
```powershell
curl -X POST "http://127.0.0.1:8000/ingest" -F "file_path=C:\Users\Raul\Projecto-Final\data\doc1_introduccion_redes.txt"
curl -X POST "http://127.0.0.1:8000/ingest" -F "file_path=C:\Users\Raul\Projecto-Final\data\doc2_modelo_osi_tcpip.md"
curl -X POST "http://127.0.0.1:8000/ingest" -F "file_path=C:\Users\Raul\Projecto-Final\data\doc3_protocolos_enrutamiento.txt"
curl -X POST "http://127.0.0.1:8000/ingest" -F "file_path=C:\Users\Raul\Projecto-Final\data\doc4_seguridad_redes_tls_ipsec.md"
curl -X POST "http://127.0.0.1:8000/ingest" -F "file_path=C:\Users\Raul\Projecto-Final\data\doc5_dns_dhcp_servicios_red.txt"
```

### 2. Consulta en Dominio
```powershell
curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d "{\"question\": \"¿Cuáles son las diferencias entre TCP y UDP?\", \"top_k\": 3}"
```

### 3. Prueba del Criterio de Abstención (Pregunta Fuera de Dominio)
```powershell
curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d "{\"question\": \"¿Cómo preparar tacos al pastor?\", \"top_k\": 3}"
```
El sistema devolverá `answered: false` indicando la activación del mecanismo de abstención por falta de evidencia en el contexto documental.
