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

1. Clone este repositorio o descarga el código.  
2. Coloque el archivo `contabilidad.db` en la misma carpeta del archivo `caja_asociadosQQA.py`.  
3. Abra una terminal o consola y navega a la carpeta del proyecto.  
4. Ejecute el dashboard con:

streamlit run caja_asociadosQQA.py


5. Interactúe con los formularios para seleccionar fechas, socios u otros filtros deseados.  
6. Visualice los gráficos y tablas según la consulta seleccionada en cada pestaña.

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



