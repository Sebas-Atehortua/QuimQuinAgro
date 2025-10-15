# Dashboard Financiero - Asociación QuimQuinAgro

Este proyecto contiene un tablero interactivo desarrollado con Streamlit para la Asociación de Piscicultores QuimQuinAgro, que le permite consultar y visualizar información financiera basada en su base de datos SQLite `contabilidad.db`.

## Funcionalidades

- **Consulta 1: Caja mensual**  
  Consulta y visualización de totales de ingresos y egresos agrupados por mes en un rango de fechas seleccionado por el usuario.

- **Consulta 2: Top 10 egresos**  
  Identificación de los conceptos con mayores egresos en un rango de fechas para optimizar costos.

- **Consulta 3: Ingresos por socio**  
  Análisis de la concentración y evolución de ingresos por parte de los socios, con filtros por fechas y por socio específico.

## Requisitos

- Python 3.8+
- Streamlit
- Pandas
- Plotly

Usted puede instalar las dependencias con:

pip install streamlit pandas plotly

## Instrucciones para ejecutar

Observaciones del paso a paso

1.	Descargar los archivos y almacenarlos en una carpeta:

![1](https://i.ibb.co/k68q9mGS/Captura-de-pantalla-2025-10-15-113451.png)

![https://i.ibb.co/jvMdR0zs/Captura-de-pantalla-2025-10-15-075309.png](https://i.ibb.co/V0qW7Jh3/Captura-de-pantalla-2025-10-15-113523.png)

2.	Usando el programa Anaconda y Spyder, visualice el código caja_asociados_QQA.py y ejecute el Streamlit usando su comando mediante la ventana de prompt.

![3](https://i.ibb.co/0VmvBG0x/Captura-de-pantalla-2025-10-15-064842.png)

3.	Se generará un enlace local que le permitirá visualizar el tablero:

![4](https://i.ibb.co/5hgpLXDX/Captura-de-pantalla-2025-10-15-113907.png)

4.	El tablero es interactivo en sus tres pestañas, y le permitirá obtener un panorama financiero de la caja, de los socios y su comportamiento. Usted debe filtrar la información usando los parámetros de consulta al lado izquierdo y esta conexión permanente con la base de datos le permitirá realizar cuanta consulta requiera.

![5](https://i.ibb.co/fYTcr677/Captura-de-pantalla-2025-10-15-114103.png)

5.	Cada sección del tablero incluye conclusiones dinámicas del comportamiento para el periodo y asociado seleccionado, por ejemplo:

![6](https://i.ibb.co/fVwz5VWn/Captura-de-pantalla-2025-10-15-114127.png)

6.	Como adicional, es posible conectarse al tablero por medio de una conexión del repositorio y Streamlit Cloud. Para ello, debe ingresar a https://share.streamlit.io/deploy, iniciar la conexión y generar una aplicación con destino a la aplicación, como aparece en el ejemplo.
 
![7](https://i.ibb.co/NgSbF6Dn/Captura-de-pantalla-2025-10-15-114425.png)

---

## Archivos incluidos

- `caja_asociadosQQA.py` — código fuente de la aplicación Streamlit.  
- `contabilidad.db` — base de datos SQLite con la información consolidada.  
- `README.md` — documentación del proyecto.  
- Carpeta `/assets` (opcional) — imágenes, capturas de pantalla o video demostrativo.

---

## Conclusiones

Cada pestaña del dashboard incluye un análisis específico para apoyar la toma de decisiones. Se observa una tendencia positiva o negativa en los flujos de caja, concentración en costos y aportes de los socios, que sirven para recomendar estrategias financieras.

---




