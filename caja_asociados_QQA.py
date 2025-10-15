# -*- coding: utf-8 -*-
"""
Created on Mon 13 13:40:19 2025

author: 
    Sebastián Atehortúa
    satehortuh@eafit.edu.co
"""

# Importamos las liberías necesarias:
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


# Configuramos la página principal
st.set_page_config(
    page_title="Dashboard Financiero - QuimQuinAgro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal logo incrustado en Imgur:
col_logo, col_title = st.columns([1, 4])
with col_logo:
        st.image("https://i.imgur.com/0ltt70t.png",
                 width=175)
with col_title:
    st.title("📊 Dashboard Financiero - Asociación QuimQuinAgro")

st.markdown("---")

# Declaramos la función para ejecutar las consultas
@st.cache_data
def run_query(query, params=()):
    try:
        with sqlite3.connect('contabilidad.db') as conn:  # abre y cierra automáticamente
            df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Error en la consulta: {e}")
        return pd.DataFrame()


# Consulta 1: Caja mensual
def query_caja_mensual(fecha_inicio, fecha_fin):
    query = """
    WITH caja_unificada AS (
        -- caja2020
        SELECT 
            date(substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2020
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2022
        SELECT 
            date(fecha) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2022
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2023
        SELECT 
            date(fecha) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2023
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2024
        SELECT 
            date(fecha) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2024
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2025
        SELECT 
            date(fecha) as fecha,
            abono as ingreso,
            prestamo as egreso,
            detalle
        FROM caja2025
        WHERE fecha IS NOT NULL
    )
    
    SELECT 
        strftime('%Y-%m', fecha) as mes,
        SUM(COALESCE(ingreso, 0)) as total_ingresos,
        SUM(COALESCE(egreso, 0)) as total_egresos,
        SUM(COALESCE(ingreso, 0) - COALESCE(egreso, 0)) as neto
    FROM caja_unificada
    WHERE fecha BETWEEN ? AND ?
    GROUP BY mes
    ORDER BY mes
    """
    
    return run_query(query, (fecha_inicio, fecha_fin))

# Consulta 2: Top 10 egresos
def query_top_egresos(fecha_inicio, fecha_fin):
    query = """
    WITH caja_unificada AS (
        -- caja2020
        SELECT 
            date(substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2020
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2022
        SELECT 
            date(fecha) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2022
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2023
        SELECT 
            date(fecha) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2023
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2024
        SELECT 
            date(fecha) as fecha,
            entrada as ingreso,
            salida as egreso,
            detalle
        FROM caja2024
        WHERE fecha IS NOT NULL
        
        UNION ALL
        
        -- caja2025
        SELECT 
            date(fecha) as fecha,
            abono as ingreso,
            prestamo as egreso,
            detalle
        FROM caja2025
        WHERE fecha IS NOT NULL
    )
    
    SELECT 
        detalle,
        SUM(COALESCE(egreso, 0)) as total_egreso
    FROM caja_unificada
    WHERE fecha BETWEEN ? AND ?
        AND egreso > 0
    GROUP BY detalle
    ORDER BY total_egreso DESC
    LIMIT 10
    """
    
    return run_query(query, (fecha_inicio, fecha_fin))

# Consulta 3: Ingresos por socio
def query_ingresos_socio(fecha_inicio, fecha_fin, socio_codigo=None):
    if socio_codigo == "Todos" or socio_codigo is None:
        query = """
        WITH ingresos_socios AS (
            -- cxc2024
            SELECT 
                c.socio as codigo_socio,
                s.nombre,
                SUM(c.entrada) as total_ingresos
            FROM cxc2024 c
            LEFT JOIN socios2024 s ON c.socio = s.codigo
            WHERE c.fecha BETWEEN ? AND ?
                AND c.entrada > 0
            GROUP BY c.socio, s.nombre
            
            UNION ALL
            
            -- cxc2025
            SELECT 
                c.codigo_cliente as codigo_socio,
                s.nombre,
                SUM(c.entrada) as total_ingresos
            FROM cxc2025 c
            LEFT JOIN socios2024 s ON c.codigo_cliente = s.codigo
            WHERE c.fecha BETWEEN ? AND ?
                AND c.entrada > 0
            GROUP BY c.codigo_cliente, s.nombre
        )
        
        SELECT 
            COALESCE(nombre, 'Socio ' || codigo_socio) as socio,
            SUM(total_ingresos) as total_ingresos
        FROM ingresos_socios
        GROUP BY codigo_socio, socio
        ORDER BY total_ingresos DESC
        """
        return run_query(query, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
    else:
        query = """
        WITH ingresos_temporales AS (
            -- cxc2024
            SELECT 
                date(c.fecha) as fecha,
                c.entrada as ingreso
            FROM cxc2024 c
            WHERE c.socio = ? 
                AND c.fecha BETWEEN ? AND ?
                AND c.entrada > 0
            
            UNION ALL
            
            -- cxc2025
            SELECT 
                date(c.fecha) as fecha,
                c.entrada as ingreso
            FROM cxc2025 c
            WHERE c.codigo_cliente = ? 
                AND c.fecha BETWEEN ? AND ?
                AND c.entrada > 0
        )
        
        SELECT 
            strftime('%Y-%m-%d', fecha) as fecha,
            SUM(ingreso) as total_ingreso
        FROM ingresos_temporales
        GROUP BY fecha
        ORDER BY fecha
        """
        return run_query(query, (socio_codigo, fecha_inicio, fecha_fin, socio_codigo, fecha_inicio, fecha_fin))

# Obtener lista de socios
@st.cache_data
def get_socios():
    query = """
    SELECT codigo, nombre 
    FROM socios2024 
    WHERE nombre IS NOT NULL 
    ORDER BY nombre
    """
    return run_query(query)

# Creamos las pestañas del tablero interactivo
tab1, tab2, tab3 = st.tabs([
    "Caja mensual", 
    "Top de 10 egresos", 
    "Ingresos por asociado (CxC)"
])

# Pestaña 1: Caja Mensual
with tab1:
    st.header("Análisis de Caja Mensual")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Parámetros de Consulta")
        fecha_actual = datetime.now()
        
        # Selector de rango de fechas
        fecha_inicio = st.date_input(
            "Fecha de inicio",
            value=fecha_actual - timedelta(days=365),
            max_value=fecha_actual
        )
        
        fecha_fin = st.date_input(
            "Fecha de fin",
            value=fecha_actual,
            max_value=fecha_actual
        )
        
        # Validar fechas
        if fecha_inicio > fecha_fin:
            st.error("La fecha de inicio debe ser anterior a la fecha de fin")
        else:
            st.success(f"Período seleccionado: {fecha_inicio} a {fecha_fin}")
    
    with col2:
        if fecha_inicio <= fecha_fin:
            # Ejecutar consulta
            df_caja = query_caja_mensual(fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d'))
            
            if not df_caja.empty:
                # Mostrar métricas principales
                st.subheader("Resumen Ejecutivo")
                total_ingresos = df_caja['total_ingresos'].sum()
                total_egresos = df_caja['total_egresos'].sum()
                neto_total = total_ingresos - total_egresos
                
                col_met1, col_met2, col_met3 = st.columns(3)
                with col_met1:
                    st.metric("Total Ingresos", f"${total_ingresos:,.0f}")
                with col_met2:
                    st.metric("Total Egresos", f"${total_egresos:,.0f}")
                with col_met3:
                    st.metric("Neto", f"${neto_total:,.0f}", 
                             delta=f"{((neto_total/total_ingresos)*100 if total_ingresos > 0 else 0):.1f}%")
                
                # Gráfico de barras agrupadas
                st.subheader("Flujo de Caja Mensual")
                
                # Preparar datos para el gráfico
                df_melted = df_caja.melt(id_vars=['mes'], 
                                        value_vars=['total_ingresos', 'total_egresos'],
                                        var_name='tipo', 
                                        value_name='monto')
                
                df_melted['tipo'] = df_melted['tipo'].replace({
                    'total_ingresos': 'Ingresos',
                    'total_egresos': 'Egresos'
                })
                
                fig = px.bar(df_melted, 
                            x='mes', 
                            y='monto', 
                            color='tipo',
                            barmode='group',
                            title='Ingresos vs Egresos por Mes',
                            labels={'mes': 'Mes', 'monto': 'Monto ($)', 'tipo': 'Tipo'},
                            color_discrete_map={'Ingresos': '#2E8B57', 'Egresos': '#DC143C'})
                
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.subheader("Detalle por Mes")
                df_display = df_caja.copy()
                df_display['total_ingresos'] = df_display['total_ingresos'].apply(lambda x: f"${x:,.0f}")
                df_display['total_egresos'] = df_display['total_egresos'].apply(lambda x: f"${x:,.0f}")
                df_display['neto'] = df_display['neto'].apply(lambda x: f"${x:,.0f}")
                
                st.dataframe(df_display, use_container_width=True)
                
                # Conclusiones
                st.subheader("📈 Conclusiones")
                mes_max_ingresos = df_caja.loc[df_caja['total_ingresos'].idxmax(), 'mes']
                mes_max_egresos = df_caja.loc[df_caja['total_egresos'].idxmax(), 'mes']
                
                st.write(f"""
                - **Tendencia general**: {'Positiva' if neto_total > 0 else 'Negativa'} con un neto de ${neto_total:,.0f}
                - **Mejor mes en ingresos**: {mes_max_ingresos} con ${df_caja['total_ingresos'].max():,.0f}
                - **Mes con mayor egresos**: {mes_max_egresos} con ${df_caja['total_egresos'].max():,.0f}
                - **Relación ingresos/egresos**: {(total_ingresos/total_egresos if total_egresos > 0 else float('inf')):.2f}:1
                """)
            else:
                st.warning("No se encontraron datos para el período seleccionado")

# Pestaña 2: Top 10 Egresos
with tab2:
    st.header("Top 10 Conceptos de Egresos")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Parámetros de Consulta")
        fecha_actual = datetime.now()
        
        fecha_inicio = st.date_input(
            "Fecha de inicio",
            value=fecha_actual - timedelta(days=180),
            max_value=fecha_actual,
            key="egresos_start"
        )
        
        fecha_fin = st.date_input(
            "Fecha de fin",
            value=fecha_actual,
            max_value=fecha_actual,
            key="egresos_end"
        )
    
    with col2:
        if fecha_inicio <= fecha_fin:
            df_egresos = query_top_egresos(fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d'))
            
            if not df_egresos.empty:
                # Métricas
                st.subheader("Resumen de Egresos")
                total_egresos = df_egresos['total_egreso'].sum()
                egreso_promedio = df_egresos['total_egreso'].mean()
                max_egreso = df_egresos['total_egreso'].max()
                
                col_met1, col_met2, col_met3 = st.columns(3)
                with col_met1:
                    st.metric("Total Egresos Top 10", f"${total_egresos:,.0f}")
                with col_met2:
                    st.metric("Egreso Promedio", f"${egreso_promedio:,.0f}")
                with col_met3:
                    st.metric("Mayor Egreso", f"${max_egreso:,.0f}")
                
                # Gráfico de barras horizontales
                st.subheader("Distribución de Egresos")
                
                fig = px.bar(df_egresos,
                            x='total_egreso',
                            y='detalle',
                            orientation='h',
                            title='Top 10 Conceptos con Mayor Egreso',
                            labels={'total_egreso': 'Monto ($)', 'detalle': 'Concepto'},
                            color='total_egreso',
                            color_continuous_scale='Reds')
                
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.subheader("Detalle de Egresos")
                df_display = df_egresos.copy()
                df_display['total_egreso'] = df_display['total_egreso'].apply(lambda x: f"${x:,.0f}")
                df_display['porcentaje'] = (df_egresos['total_egreso'] / total_egresos * 100).apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(df_display, use_container_width=True)
                
                # Análisis de concentración
                st.subheader("📊 Análisis de Concentración")
                top3_total = df_egresos.head(3)['total_egreso'].sum()
                porcentaje_top3 = (top3_total / total_egresos) * 100
                
                st.write(f"""
                - **Concentración en top 3**: {porcentaje_top3:.1f}% del total de egresos
                - **Concepto principal**: {df_egresos.iloc[0]['detalle']} representa {(df_egresos.iloc[0]['total_egreso']/total_egresos*100):.1f}%
                - **Diversificación**: {'Alta' if len(df_egresos) >= 8 else 'Media' if len(df_egresos) >= 5 else 'Baja'} diversificación de gastos
                """)
            else:
                st.warning("No se encontraron egresos para el período seleccionado")

# Pestaña 3: Ingresos por Socio
with tab3:
    st.header("Análisis de Ingresos por Socio")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Parámetros de Consulta")
        fecha_actual = datetime.now()
        
        fecha_inicio = st.date_input(
            "Fecha de inicio",
            value=fecha_actual - timedelta(days=365),
            max_value=fecha_actual,
            key="socios_start"
        )
        
        fecha_fin = st.date_input(
            "Fecha de fin",
            value=fecha_actual,
            max_value=fecha_actual,
            key="socios_end"
        )
        
        # Selector de socio
        socios_df = get_socios()
        opciones_socios = ["Todos"] + [f"{row['codigo']} - {row['nombre']}" for _, row in socios_df.iterrows()]
        
        socio_seleccionado = st.selectbox(
            "Seleccionar Socio",
            options=opciones_socios,
            index=0
        )
        
        if socio_seleccionado != "Todos":
            socio_codigo = int(socio_seleccionado.split(" - ")[0])
        else:
            socio_codigo = "Todos"
    
    with col2:
        if fecha_inicio <= fecha_fin:
            df_ingresos_socio = query_ingresos_socio(
                fecha_inicio.strftime('%Y-%m-%d'), 
                fecha_fin.strftime('%Y-%m-%d'),
                socio_codigo
            )
            
            if not df_ingresos_socio.empty:
                if socio_codigo == "Todos":
                    # Gráfico de barras para todos los socios
                    st.subheader("Distribución de Ingresos por Socio")
                    
                    total_ingresos = df_ingresos_socio['total_ingresos'].sum()
                    
                    fig = px.bar(df_ingresos_socio,
                                x='total_ingresos',
                                y='socio',
                                orientation='h',
                                title='Ingresos por Socio (Todos)',
                                labels={'total_ingresos': 'Ingresos ($)', 'socio': 'Socio'},
                                color='total_ingresos',
                                color_continuous_scale='Greens')
                    
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Métricas
                    st.subheader("Métricas de Concentración")
                    top_socio = df_ingresos_socio.iloc[0]
                    top3_ingresos = df_ingresos_socio.head(3)['total_ingresos'].sum()
                    porcentaje_top3 = (top3_ingresos / total_ingresos) * 100
                    
                    col_met1, col_met2, col_met3 = st.columns(3)
                    with col_met1:
                        st.metric("Total Ingresos", f"${total_ingresos:,.0f}")
                    with col_met2:
                        st.metric("Socio Principal", f"${top_socio['total_ingresos']:,.0f}")
                    with col_met3:
                        st.metric("Concentración Top 3", f"{porcentaje_top3:.1f}%")
                    
                    # Tabla de datos
                    st.subheader("Detalle por Socio")
                    df_display = df_ingresos_socio.copy()
                    df_display['total_ingresos'] = df_display['total_ingresos'].apply(lambda x: f"${x:,.0f}")
                    df_display['porcentaje'] = (df_ingresos_socio['total_ingresos'] / total_ingresos * 100).apply(lambda x: f"{x:.1f}%")
                    
                    st.dataframe(df_display, use_container_width=True)
                    
                    # Conclusiones
                    st.subheader("👥 Conclusiones - Todos los Socios")
                    st.write(f"""
                    - **Socio líder**: {top_socio['socio']} con {(top_socio['total_ingresos']/total_ingresos*100):.1f}% del total
                    - **Distribución**: {'Concentrada' if porcentaje_top3 > 60 else 'Balanceada' if porcentaje_top3 > 40 else 'Diversificada'}
                    - **Número de socios activos**: {len(df_ingresos_socio)} socios generaron ingresos
                    - **Ingreso promedio por socio**: ${(total_ingresos/len(df_ingresos_socio)):,.0f}
                    """)
                    
                else:
                    # Gráfico de línea para un socio específico
                    st.subheader(f"Evolución Temporal de Ingresos - {socio_seleccionado}")
                    
                    # Convertir fecha a datetime para ordenamiento
                    df_ingresos_socio['fecha'] = pd.to_datetime(df_ingresos_socio['fecha'])
                    df_ingresos_socio = df_ingresos_socio.sort_values('fecha')
                    
                    total_ingresos = df_ingresos_socio['total_ingreso'].sum()
                    ingreso_promedio = df_ingresos_socio['total_ingreso'].mean()
                    max_ingreso = df_ingresos_socio['total_ingreso'].max()
                    
                    col_met1, col_met2, col_met3 = st.columns(3)
                    with col_met1:
                        st.metric("Total Período", f"${total_ingresos:,.0f}")
                    with col_met2:
                        st.metric("Promedio Diario", f"${ingreso_promedio:,.0f}")
                    with col_met3:
                        st.metric("Máximo Diario", f"${max_ingreso:,.0f}")
                    
                    # Gráfico de línea
                    fig = px.line(df_ingresos_socio,
                                x='fecha',
                                y='total_ingreso',
                                title=f'Ingresos Diarios - {socio_seleccionado}',
                                labels={'fecha': 'Fecha', 'total_ingreso': 'Ingreso ($)'},
                                markers=True)
                    
                    fig.update_traces(line=dict(color='#2E8B57', width=3),
                                    marker=dict(size=6, color='#228B22'))
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tabla de datos
                    st.subheader("Detalle por Fecha")
                    df_display = df_ingresos_socio.copy()
                    df_display['total_ingreso'] = df_display['total_ingreso'].apply(lambda x: f"${x:,.0f}")
                    df_display['fecha'] = df_display['fecha'].dt.strftime('%Y-%m-%d')
                    
                    st.dataframe(df_display, use_container_width=True)
                    
                    # Análisis de tendencia
                    st.subheader("📈 Análisis de Tendencia")
                    if len(df_ingresos_socio) > 1:
                        crecimiento = ((df_ingresos_socio['total_ingreso'].iloc[-1] - df_ingresos_socio['total_ingreso'].iloc[0]) / 
                                     df_ingresos_socio['total_ingreso'].iloc[0] * 100)
                        
                        st.write(f"""
                        - **Tendencia**: {'Positiva' if crecimiento > 0 else 'Negativa'} ({crecimiento:.1f}%)
                        - **Consistencia**: {'Alta' if df_ingresos_socio['total_ingreso'].std() < ingreso_promedio else 'Media'}
                        - **Frecuencia**: {len(df_ingresos_socio)} días con ingresos en el período
                        - **Perfil**: {'Frecuente' if len(df_ingresos_socio) > (len(pd.date_range(fecha_inicio, fecha_fin)) * 0.3) else 'Esporádico'}
                        """)
            else:
                st.warning("No se encontraron ingresos para los parámetros seleccionados")

# Pie de página
st.markdown("---")
st.markdown(
    "**Elaboró: Sebastián Atehortúa - satehortuh** • Asociación de Piscicultores QuimQuinAgro • "
    "Desarrollado en conjunto por las áreas de BI 💻 y Financiera 💹"
)

