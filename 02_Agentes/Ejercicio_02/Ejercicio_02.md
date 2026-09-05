# Ejercicio 2 — Descripción PEAS de agentes inteligentes
## Objetivo

Para cada una de las **8 aplicaciones** listadas abajo, redacta una descripción
PEAS completa y coherente. Debes pensar como diseñador del agente: qué optimiza,
dónde actúa, con qué puede mover o modificar el mundo, y qué puede observar.

## Aplicaciones a analizar

Describe PEAS para cada una de estas aplicaciones:

1. **Asistente virtual de voz** (p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente).

- **Performance:** Tasa de coincidencia entre palabras mencionadas y palabras identificadas, tiempo de respuesta entre consulta y entrega de resultado.
- **Environment:** Casa, trabajo, en general la habitación donde esté colocado y escuchando cuando se escuche el comando de activación (Ej: Alexa, haz esto...), interactúa con ruidos, distintas voces al usuario, sonidos ambientales.
- **Actuators:** Respuesta por voz, prender o apagar las luces o dispositivos en el ecosistema, reproducción de contenido multimedia, entre otras funciones dentro de su catálogo. 
- **Sensors:** Micrófono, Lector de texto(cuando la solicitud es escrita), botón de activación(como el de bloqueo en algunos celulares)

2. **Robot aspirador doméstico** (p. ej. Roomba u otro robot que limpia pisos de un departamento).

- **Performance:** Metros cuadrados de superficie limpiada, porcentaje de superficie con limpieza con respecto a la superficie total, porcentaje de batería, veces que choca contra algun mueble o pared.
- **Environment:** Piso de la casa habitación, se enfrenta a mascotas, movimiento de muebles después de su primer escaneo. 
- **Actuators:** motores de las ruedas, motor de la aspiradora que realiza la succión, motores de cepillos, punto de "anclaje" a la base de carga. 
- **Sensors:** sensores de colisión(para cuando choque contra un mueble o persona), sensores infrarrojos para determinar distancias, nivel de batería(para no quedarse a medio camino de la base de carga)

3. **Sistema de recomendación de streaming** (p. ej. Netflix o Spotify que sugiere películas o canciones).

- **Performance:** Cantidad de clicks que recibe la recomendación, tiempo que consume el contenido el usuario(% en base al total del contenido), númmero de recomendaciones ofrecidas, likes o dedos arriba que reciben las recomendaciones.
- **Environment:** Plataforma de streaming
- **Actuators:** Generar listado de recomendaciones, envío de notificaciones de recomendación, orden de contenido desde recomendado hasta menos consumido por el usuario
- **Sensors:** Historiales, Calificaciones(positivas o negativas), Tiempo de consumo del usuario.

4. **Vehículo autónomo en ciudad** (conducción sin conductor en calles urbanas con tráfico y peatones).

- **Performance:** Número de choques del auto, tiempo de llegada a destino vs tiempo de ruta promedio, Número de infracciones cometidas(según ley de tránsito local), eficiencia de gasolina x km.
- **Environment:** Calles de la ciudad, con tráfico elevado o normal, peaton, semaforos, altos, glorietas, etc.
- **Actuators:** Dirección(por el volante), acelerador, freno, palancas direccionales, cláxon, palanca luces, (probablemente limpiaparabrisas para visibilidad del usuario a bordo)
- **Sensors:** cámaras espaciales, GPS, sensores de velocidad

5. **Agente de trading algorítmico en bolsa** (compra y venta automática de acciones en mercados financieros).

- **Performance:** Ganancia menos impuestos, tasa de retorno, pérdida más costos de trade, velocidad de trading
- **Environment:** Mercado financiero global/nacional
- **Actuators:** Órdenes de compra y venta, cancelación de órdenes(en caso de encontrar un mejor precio durante la compra o venta), límites de precio o pérdida. 
- **Sensors:** cotizador en tiempo real, volumen de transacciones del activo, tendencias o noticias, indicadores económicos(TIR, alphas, betas)

6. **Sistema de diagnóstico médico asistido por IA** (apoya a un médico a interpretar síntomas e imágenes clínicas).

- **Performance:** Tasa de falso positivo o negativos, tiempos de diagnóstico, impacto en la mejoría del paciente.
- **Environment:** Hospitales, consultorios
- **Actuators:** Generador de texto para diagnóstico, herramienta de selección de imagenes por palabras clave de diagnostico( agregar alguna referencia de la bdd), Alertas(en caso de casos graves)
- **Sensors:** Escaner de imagenes(para los rayos x o resonancias), análista de resultados de laboratorio, micrófono para escuchar al doctor y paciente

7. **Dron de inspección de infraestructura** (revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas).

- **Performance:** Tasa de desperfectos identificados, metros cuadrados o cúbicos analizados, precisión de localización de zona con desperfectos.
- **Environment:** Edificios, casas, zonas abiertas de infraestructura(como puentes o zonas al aire libre)
- **Actuators:** Motores de vuelo, cámaras para fotografear zonas(en específico la función de tomar foto).
- **Sensors:** Sensores infrarrojos, gps, cámara (como sensor óptico) 

8. **Agente jugador de ajedrez** (programa que compite contra un humano u otro agente en partidas completas).

- **Performance:** Número de movimientos, tasa de victorias, ELO(medida de ranking como el Magnus Carlsen), puntuación de jugada óptima(este tipo de puntuación la tienen páginas como chess), tiempo por movimiento(especialmente importante en modos de juegos como blitz)
- **Environment:** Tablero de ajedrez(físico o virtual)
- **Actuators:** Mover piezas según sus características y situación( ej el rey no se puede mover en la primer jugada), captura de piezas, enroque, hacer declaración de Jaque Mate, tablas o Derrota, volver a peon una ficha superior.
- **Sensors:** estado del tablero(mediante alguna matriz), reloj de turno, notificación para saber si el oponente hizo un movimiento.  
