# Reporte Técnico: Arquitectura y Evaluación del Sistema RAG

## 1. Dominio y Estadísticas del Corpus
El dominio temático seleccionado para el corpus de conocimiento abarca la Arquitectura de Redes de Computadoras y Protocolos de Internet. 
- Número de Documentos en el Corpus: 5 archivos estructurados en texto plano (.txt) y Markdown (.md).
- Cobertura de Temas: Topologías de red, modelo de referencia OSI vs TCP/IP, protocolos de enrutamiento dinámico (OSPF y BGP), seguridad en comunicaciones (TLS e IPsec), y servicios de infraestructura (DNS y DHCP).
- Modelo de Embeddings Utilizado: `text-embedding-004` (Google AI SDK), configurado uniformemente para la vectorización de chunks documentales y la codificación de consultas de búsqueda.

## 2. Justificación del Tamaño de Chunk y Overlap
Se seleccionó un esquema de segmentación (chunking) basado en palabras con los siguientes parámetros:
- Tamaño del Chunk: 300 palabras.
- Solape (Overlap): 50 palabras.

### Fundamento Técnico:
Los documentos técnicos contienen conceptos densos y relaciones causales (por ejemplo, secuencias de handshake o explicaciones paso a paso como la secuencia DORA de DHCP). Un tamaño de 300 palabras equivale aproximadamente a 400-450 tokens, lo que retiene el contexto semántico completo de una sección técnica sin fragmentar definiciones conceptuales. 

El solape de 50 palabras (aprox. 15-20% del bloque) previene la pérdida de contexto en los bordes de partición, asegurando que frases clave divididas entre chunks consecutivos mantengan continuidad al ser vectorizadas.

## 3. Criterio Matemático y Lógico de Abstención
Para garantizar la confiabilidad y prevenir alucinaciones en entornos de producción, el sistema aplica un filtro de abstención de doble capa:

### Capa 1: Criterio Matemático por Distancia Vectorial
ChromaDB calcula la distancia del coseno entre el vector de la pregunta y cada vector almacenado. La métrica de distancia de coseno se define como:
$$D_{\text{coseno}}(u, v) = 1 - \frac{u \cdot v}{\|u\| \|v\|}$$

Donde valores cercanos a 0.0 indican máxima similitud semántica. Se estableció un umbral crítico de abstención:
$$\text{Threshold} = 0.65$$

Si la distancia del chunk recuperado más cercano supera 0.65, la API interrumpe la llamada al modelo de generación y retorna inmediatamente `answered = False` con la justificación de baja similitud.

### Capa 2: Restricción Semántica en System Instruction
Si la consulta supera el filtro matemático pero el contexto recuperado carece de la evidencia requerida para responder concretamente la pregunta del usuario, la instrucción de sistema de Gemini impone la obligación estricta de responder la frase de abstención declarativa: "No dispongo de suficiente información en el contexto provisto para responder a esta pregunta.", retornando la bandera `answered = False`.

## 4. Flujo de Datos y Separación de Responsabilidades
El sistema implementa una arquitectura desacoplada donde cada componente ejecuta una función especializada:

```
[ Usuario (Streamlit UI) ]
            | (HTTP JSON)
            v
   [ FastAPI Orchestrator ]
       |            |
       | (Texto)    | (Vector Query)
       v            v
[ Google AI ]  [ ChromaDB Vector Store ]
(Embeddings)   (Persistencia en disco: C:\Users\Raul\Projecto-Final\chroma)
       |            |
       +-----+------+
             | (Contexto + Pregunta)
             v
      [ Google AI Gemini ]
      (Generación Anclada)
```

1. Google AI (`text-embedding-004`): Genera exclusivamente las representaciones vectoriales densas (768 dimensiones) para los chunks y consultas. ChromaDB no ejecuta funciones internas de embedding.
2. ChromaDB: Actúa como base de datos vectorial persistente en disco en `C:\Users\Raul\Projecto-Final\chroma\`, gestionando índices HNSW para búsqueda rápida por vecinos más cercanos (k-NN) y almacenando el texto plano y metadatos (`source`, `chunk_index`).
3. Google AI Gemini (`gemini-2.5-flash`): Recibe únicamente los chunks contextuales filtrados y formateados con etiquetas numéricas `[1]`, `[2]`, produciendo respuestas sintetizadas con citas obligatorias.
4. FastAPI & Streamlit: El backend expone endpoints REST estandarizados con Pydantic, mientras Streamlit actúa como cliente HTTP puro sin dependencias directas de la base vectorial o SDK de inteligencia artificial.
