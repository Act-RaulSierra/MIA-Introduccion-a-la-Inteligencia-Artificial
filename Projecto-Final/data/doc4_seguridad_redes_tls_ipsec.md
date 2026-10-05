# Seguridad en Redes de Datos: TLS y IPsec

## Protocolo TLS (Transport Layer Security)
TLS es un protocolo de cifrado diseñado para proporcionar seguridad en las comunicaciones sobre una red IP. Opera en la capa de transporte/aplicación, ubicándose principalmente sobre TCP. TLS consta de dos capas principales:
- Protocolo TLS Handshake: Permite la autenticación mutua entre cliente y servidor mediante certificados digitales X.509, así como la negociación de algoritmos criptográficos (ciphersuites) y la generación de claves de sesión simétricas.
- Protocolo TLS Record: Encapsula los datos de la aplicación y garantiza la confidencialidad mediante cifrado simétrico (como AES-GCM) y la integridad mediante códigos de autenticación de mensajes (MAC).

## Suite de Seguridad IPsec
IPsec (Internet Protocol Security) es una suite de protocolos que asegura las comunicaciones a nivel de capa de Red (Capa 3 de OSI). A diferencia de TLS, IPsec protege todo el tráfico IP que pasa entre dos puntos finales sin necesidad de modificar las aplicaciones.

IPsec consta de dos protocolos fundamentales:
1. AH (Authentication Header): Proporciona autenticación de origen e integridad de datos, pero no ofrece confidencialidad (no cifra la carga útil).
2. ESP (Encapsulating Security Payload): Ofrece confidencialidad mediante cifrado, autenticación de datos e integridad.

IPsec puede operar en modo Transporte (cifra solo el payload del paquete IP) o en modo Túnel (cifra el paquete IP completo, añadiendo un nuevo encabezado IP para redes privadas VPN).
