# Arquitectura Comparativa: Modelo OSI y Protocolo TCP/IP

## El Modelo de Referencia OSI
El modelo OSI (Open Systems Interconnection) es un marco conceptual de 7 capas desarrollado por la ISO para estandarizar las funciones de un sistema de comunicaciones:
1. Capa Física: Transmisión de bits crudos sobre el medio físico.
2. Capa de Enlace de Datos: Direccionamiento físico (MAC) y detección de errores de trama.
3. Capa de Red: Direccionamiento lógico (IP) y enrutamiento entre redes.
4. Capa de Transporte: Control de flujo, multiplexación y transferencia confiable (TCP) o no confiable (UDP).
5. Capa de Sesión: Gestión y control de diálogos entre aplicaciones.
6. Capa de Presentación: Formateo, cifrado y compresión de datos.
7. Capa de Aplicación: Interfaz directa con los procesos del usuario final.

## El Modelo Práctico TCP/IP
A diferencia del modelo OSI, la pila TCP/IP se estructura en 4 capas operativas:
- Capa de Acceso a la Red: Combina las funciones física y de enlace.
- Capa de Internet: Corresponde a la capa de red del OSI. Define los protocolos IP (IPv4 e IPv6).
- Capa de Transporte: Implementa TCP (Transmission Control Protocol) y UDP (User Datagram Protocol). TCP ofrece control de errores, acuses de recibo (ACK) y retransmisión, mientras que UDP prioriza la baja latencia sin garantías de entrega.
- Capa de Aplicación: Engloba las capas de sesión, presentación y aplicación de OSI (HTTP, SMTP, SSH, DNS).
