# Ejercicio 2 — Descripción PEAS de agentes inteligentes

## Contexto

En el capítulo 2 de *Artificial Intelligence: A Modern Approach* (Russell & Norvig),
un agente se entiende mejor cuando se especifica su **entorno de tarea**. Una forma
estándar de hacerlo es la descripción **PEAS**:

| Letra | Significado | Pregunta guía |
|---|---|---|
| **P** | *Performance* (medida de desempeño) | ¿Cómo se evalúa el éxito del agente? |
| **E** | *Environment* (entorno) | ¿En qué mundo opera? ¿Quién más actúa ahí? |
| **A** | *Actuators* (actuadores) | ¿Qué acciones puede ejecutar? |
| **S** | *Sensors* (sensores) | ¿Qué información puede percibir? |

Este ejercicio **no requiere programar**. Consiste en analizar distintos tipos de
aplicaciones reales y describir cada una con el esquema PEAS.

## Objetivo

Para cada una de las **8 aplicaciones** listadas abajo, redacta una descripción
PEAS completa y coherente. Debes pensar como diseñador del agente: qué optimiza,
dónde actúa, con qué puede mover o modificar el mundo, y qué puede observar.

## Aplicaciones a analizar

Describe PEAS para cada una de estas aplicaciones:

1. **Asistente virtual de voz** (p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente).
**P**:
**E**:
**A**:
**S**:

2. **Robot aspirador doméstico** (p. ej. Roomba u otro robot que limpia pisos de un departamento).
3. **Sistema de recomendación de streaming** (p. ej. Netflix o Spotify que sugiere películas o canciones).
4. **Vehículo autónomo en ciudad** (conducción sin conductor en calles urbanas con tráfico y peatones).
5. **Agente de trading algorítmico en bolsa** (compra y venta automática de acciones en mercados financieros).
6. **Sistema de diagnóstico médico asistido por IA** (apoya a un médico a interpretar síntomas e imágenes clínicas).
7. **Dron de inspección de infraestructura** (revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas).
8. **Agente jugador de ajedrez** (programa que compite contra un humano u otro agente en partidas completas).

## Instrucciones

Para **cada** aplicación entrega una sección con este formato:

```markdown
### N. Nombre de la aplicación

- **Performance:** ...
- **Environment:** ...
- **Actuators:** ...
- **Sensors:** ...
```

### Criterios de calidad

- **Performance:** incluye métricas concretas (precisión, tiempo, costo, satisfacción del usuario, ganancia, seguridad, etc.), no solo “hacerlo bien”.
- **Environment:** menciona si es parcialmente observable o totalmente observable, si es estocástico o determinista, episódico o secuencial, estático o dinámico, y discreto o continuo (según aplique).
- **Actuators:** lista acciones reales que el agente puede ejecutar, no capacidades vagas.
- **Sensors:** lista percepciones concretas (cámara, micrófono, API, historial de usuario, cotizaciones de mercado, etc.).

### Ejemplo breve (solo como referencia de formato)

**Aplicación:** termostato inteligente de una casa.

- **Performance:** mantener la temperatura deseada con mínimo consumo de energía y máxima comodidad del habitante.
- **Environment:** interior de una vivienda; cambia con clima exterior, ventanas abiertas y presencia de personas.
- **Actuators:** encender/apagar calefacción o aire acondicionado; ajustar temperatura objetivo; enviar alertas al usuario.
- **Sensors:** termómetro interior, horario, presencia (movimiento), lectura de clima exterior vía internet.

> El termostato **no** está en la lista de las 8 aplicaciones: es solo un ejemplo.
> Debes completar las ocho aplicaciones indicadas arriba.

## Entrega

Un documento (Markdown o PDF) con las **8 descripciones PEAS**, numeradas y con título
claro para cada aplicación.

Opcional pero recomendado: al final de cada descripción, añade **2–3 líneas** que
justifiquen por qué clasificaste el entorno como observable/estocástico/secuencial/etc.

## Criterios de aceptación

- No usar IA para generar las respuestas de este ejercicio.
- Hay exactamente **8** descripciones PEAS, una por cada aplicación de la lista.
- Cada descripción tiene los cuatro componentes (**P**, **E**, **A**, **S**) claramente identificados.
- Las respuestas son específicas de la aplicación (evita copiar la misma descripción genérica para todas).
- El entorno (**E**) incluye al menos una clasificación AIMA (p. ej. parcialmente observable, estocástico, secuencial).
- Redacción clara, en español, sin ambigüedades evidentes.

## Pistas

- Un mismo tipo de agente puede tener **distintos PEAS** según el contexto: un dron de inspección en un túnel no es igual que uno en un campo abierto.
- **Performance** y **Environment** suelen confundirse: la medida de desempeño dice *qué optimizas*; el entorno dice *dónde ocurre la tarea y qué condiciones enfrentas*.
- Si dudas entre dos sensores o actuadores, pregúntate: *¿esto lo usa el agente para decidir, o solo el humano que lo supervisa?* Solo cuenta lo que el **agente** percibe o controla.