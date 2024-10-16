# Sistema de Detección de PPE
**Integrantes:**
- Chiara, Agostina - [agosschiara25@gmail.com](mailto:agosschiara25@gmail.com)
- Matteucci, Andrea - [andymatteucci2003@gmail.com](mailto:andymatteucci2003@gmail.com)
- Tulian, Laura - [lau.tulian01@gmail.com](mailto:lau.tulian01@gmail.com)

## Descripción del Proyecto

En ámbitos laborales como la construcción y la industria manufacturera, el uso adecuado de equipos de protección personal (EPP) es crucial para minimizar los riesgos de accidentes. Este proyecto se centra en desarrollar un sistema automatizado que utiliza técnicas de visión por computadora con OpenCV y el modelo de detección de objetos YOLO para monitorear el uso correcto de EPP, específicamente cascos, chalecos, orejeras, lentes de seguridad y botas.

## Objetivo

El objetivo principal de este proyecto es implementar un sistema que pueda analizar imágenes y videos en tiempo real para detectar si los trabajadores están usando el equipo de protección requerido. Esto permitirá mejorar la supervisión de las normas de seguridad, reducir los incidentes y asegurar un ambiente de trabajo más seguro.

## Metodología

El sistema utiliza el modelo YOLO, entrenado para reconocer clases específicas de EPP. La detección se realiza en tiempo real mediante OpenCV, permitiendo la captura y procesamiento continuo de imágenes y videos de las zonas de trabajo.

1. **Entrenamiento del Modelo:**
   - Se utilizó Grounding DINO para generar etiquetas de alta calidad y localizar de manera precisa los elementos de EPP en las imágenes.
   - Roboflow facilitó la gestión, aumento y preprocesamiento del conjunto de datos.

2. **Implementación del Sistema:**
   - El sistema permite la detección en imágenes en vivo y vídeos previamente grabados.
   - Se activa una alarma si se detecta que un trabajador no lleva algún elemento de seguridad.

3. **Resultados y Beneficios:**
   - Proporciona un monitoreo continuo y automatizado.
   - Mejora el cumplimiento de las normas de seguridad.
   - Genera reportes y estadísticas sobre el uso del EPP.

## Requerimientos

### Funcionales
- Autenticación de usuarios.
- Detección de objetos de seguridad en tiempo real.
- Carga de imágenes y vídeos para procesamiento.

### No Funcionales
- Seguridad en el manejo de contraseñas.
- Integración con diferentes cámaras.
- Interfaz intuitiva y compatible con varios sistemas operativos.

## Stack Tecnológico


- **cryptography**: `43.0.1`
- **opencv-python**: `4.10.0.84`
- **pillow**: `10.4.0`
- **PyMuPDF**: `1.24.10`
- **SQLAlchemy**: `2.0.35`
- **tkfontawesome**: `0.2.0`
- **ultralytics**: `8.2.100`
- **zipp**: `3.20.2`


## Imagenes
![image](https://github.com/user-attachments/assets/7aea45b6-1fcf-45c2-91c3-26b85bd11075)

![image](https://github.com/user-attachments/assets/4ce4d841-f95c-4a9d-bd80-a5a875b051ad)

![image](https://github.com/user-attachments/assets/bc88d4e4-ce32-49a0-a407-aa77cbf7e7af)
