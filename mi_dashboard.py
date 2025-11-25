# mi_dashboard.py ← Dashboard William Andrey Chaves - Jhon Jairo Mateus - Cesar Luis Correa
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as make_subplots
import os
from collections import Counter
import numpy as np

# =================================== CONFIGURACIÓN ===================================
st.set_page_config(page_title="Impacto de Tormenta - Ecosistema Desértico", layout="wide", page_icon="🌵")
st.title("🌵🌪️ Impacto de la Tormenta en el Ecosistema Desértico")
st.markdown("### Comparación ANTES y DESPUÉS de la tormenta de arena - Datos 100% reales del JSON")

# =================================== UTILIDADES DE IMAGEN ===================================
def encontrar_imagen(candidatos):
    for nombre in candidatos:
        if os.path.exists(nombre):
            return nombre
    try:
        for fname in os.listdir("."):
            low = fname.lower()
            if ("minecraft" in low or "minecraf" in low) and (low.endswith(".jpg") or low.endswith(".jpeg") or low.endswith(".png")):
                return fname
    except Exception:
        pass
    return None

# =================================== IMÁGENES ===================================
imagen_minecraft = encontrar_imagen(["minecraft.jpg", "minecraft.png", "minecraf.jpg", "minecraf.png"])

if imagen_minecraft:
    st.image(imagen_minecraft, caption="Bioma Desértico - Minecraft", use_column_width=True)
else:
    st.warning("⚠️ Imagen de Minecraft no encontrada. Renombra tu archivo a 'minecraft.jpg' y colócalo en esta carpeta.")

st.markdown("---")

# =================================== TRADUCCIONES Y CATEGORÍAS ===================================
traducciones = {
    'kangaroo_mouse': 'Ratón Canguro',
    'desert_viper': 'Víbora del Desierto',
    'desert_tortoise': 'Tortuga del Desierto',
    'roadrunner': 'Correcaminos',
    'chuckwalla': 'Chacahualas',
    'coyote': 'Coyote',
    'coral_snake': 'Serpiente de Coral',
    'green_lizard': 'Lagartija Verde',
    'collared_lizard': 'Lagartija de Collar',
    'desert_fox': 'Zorro del Desierto',
    'baby_coyote': 'Cachorro de Coyote',
    'desert_iguana': 'Iguana del Desierto',
    'baby_desert_fox': 'Cachorro de Zorro del Desierto',
    'banded_snake': 'Serpiente bandada',
}

categorias_ecologicas = {
    'herbívoros': ['Ratón Canguro', 'Tortuga del Desierto', 'Chacahualas', 'Iguana del Desierto'],
    'carnívoros': ['Víbora del Desierto', 'Coyote', 'Zorro del Desierto', 'Serpiente de Coral', 'Serpiente bandada'],
    'omnívoros': ['Correcaminos', 'Lagartija Verde', 'Lagartija de Collar'],
    'crías': ['Cachorro de Coyote', 'Cachorro de Zorro del Desierto']
}

# =================================== SUBIDA DE ARCHIVOS ===================================
col1, col2 = st.columns(2)

with col1:
    uploaded_antes = st.file_uploader("📂 Sube JSON ANTES de la tormenta", type=["json"])

with col2:
    uploaded_despues = st.file_uploader("📂 Sube JSON DESPUÉS de la tormenta", type=["json"])

if not uploaded_antes or not uploaded_despues:
    st.warning("⚠️ Por favor sube AMBOS archivos JSON para el análisis comparativo")
    st.stop()

# Procesar archivos
try:
    json_antes = json.load(uploaded_antes)
    json_despues = json.load(uploaded_despues)
    
    entidades_antes = json_antes['entidades']
    entidades_despues = json_despues['entidades']
    
    st.success(f"✅ Archivos cargados correctamente\n"
               f"• ANTES: {len(entidades_antes)} entidades\n"
               f"• DESPUÉS: {len(entidades_despues)} entidades")
except:
    st.error("Error procesando los archivos JSON")
    st.stop()

# Procesar y traducir entidades
def procesar_entidades(entidades):
    for e in entidades:
        nombre_esp = traducciones.get(e['nombre'], e['nombre'])
        e['nombre_es'] = nombre_esp
        e['categoria'] = 'otros'
        for cat, lista in categorias_ecologicas.items():
            if nombre_esp in lista:
                e['categoria'] = cat
                break
        # Extraer coordenadas
        if 'position' in e:
            e['x'] = e['position'].get('x', 0)
            e['y'] = e['position'].get('y', 0)
            e['z'] = e['position'].get('z', 0)
    return entidades

entidades_antes = procesar_entidades(entidades_antes)
entidades_despues = procesar_entidades(entidades_despues)

# DataFrames
df_antes = pd.DataFrame(entidades_antes)
df_despues = pd.DataFrame(entidades_despues)
df_antes['periodo'] = 'Antes'
df_despues['periodo'] = 'Después'
df_combinado = pd.concat([df_antes, df_despues], ignore_index=True)

# =================================== PESTAÑAS ===================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Cambios Poblacionales",
    "🗺️ Distribución 3D",
    "❤️ Salud del Ecosistema",
    "🛡️ Supervivencia",
    "🏷️ Por Categorías"
])

with tab1:
    st.header("📊 Cambios Poblacionales por Especie - Antes vs Después de la Tormenta")
    cambios = df_combinado.groupby(['nombre_es', 'periodo']).size().unstack(fill_value=0)
    cambios['Cambio'] = cambios['Después'] - cambios['Antes']
    cambios['% Cambio'] = ((cambios['Cambio'] / cambios['Antes']) * 100).round(1).replace([np.inf, -np.inf], np.nan)
    
    st.dataframe(cambios.style.background_gradient(cmap='RdYlGn', subset=['Cambio']))
    
    fig_cambios = px.bar(cambios.reset_index(), x='nombre_es', y=['Antes', 'Después'], 
                         barmode='group', title="Cambios Poblacionales por Especie - Antes vs Después de la Tormenta",
                         color_discrete_sequence=['#ADD8E6', '#FFA07A'])
    fig_cambios.update_layout(xaxis_title="Especie", yaxis_title="Cantidad de Individuos", xaxis_tickangle=-45)
    st.plotly_chart(fig_cambios, use_container_width=True)

with tab2:
    st.header("🗺️ Distribución 3D del Ecosistema - Antes y Después de la Tormenta")
    col3d1, col3d2 = st.columns(2)
    
    with col3d1:
        st.subheader("🌵 Antes de la Tormenta")
        fig_3d_antes = px.scatter_3d(df_antes, x='x', y='y', z='z', color='categoria',
                                     hover_data=['nombre_es'], title="Distribución Antes de la Tormenta")
        fig_3d_antes.update_layout(scene_aspectmode='cube')
        st.plotly_chart(fig_3d_antes, use_container_width=True)
    
    with col3d2:
        st.subheader("🌧️ Después de la Tormenta")
        fig_3d_despues = px.scatter_3d(df_despues, x='x', y='y', z='z', color='categoria',
                                       hover_data=['nombre_es'], title="Distribución Después de la Tormenta")
        fig_3d_despues.update_layout(scene_aspectmode='cube')
        st.plotly_chart(fig_3d_despues, use_container_width=True)

with tab3:
    st.header("❤️ Salud del Ecosistema - Comparativa Radial")
    metricas = []
    for periodo, df in [("Antes", df_antes), ("Después", df_despues)]:
        total = len(df)
        diversidad = df['nombre_es'].nunique()
        crias = len(df[df['categoria'] == 'crías'])
        carnivoros = len(df[df['categoria'] == 'carnívoros'])
        herbivoros = len(df[df['categoria'] == 'herbívoros'])
        balance = carnivoros / herbivoros if herbivoros > 0 else 0
        
        metricas.append({
            'Periodo': periodo,
            'Total Entidades': total,
            'Diversidad (especies)': diversidad,
            'Densidad': round(total / (df['x'].max() - df['x'].min() + 1), 2) if len(df) > 0 else 0,
            'Balance (Carn/Herb)': round(balance, 2),
            'Crías (reproducción)': crias,
            'Salud General': round((diversidad + crias) / total * 100 if total > 0 else 0, 1)
        })
    
    df_salud = pd.DataFrame(metricas)
    st.dataframe(df_salud, use_container_width=True)
    
    categorias_salud = ['Total Entidades', 'Diversidad (especies)', 'Densidad', 'Balance (Carn/Herb)', 'Crías (reproducción)', 'Salud General']
    fig_radial = go.Figure()
    for i in range(len(df_salud)):
        valores = [df_salud.loc[i, cat] for cat in categorias_salud]
        max_vals = df_salud[categorias_salud].max()
        valores_norm = [v / max_vals[j] if max_vals[j] > 0 else 0 for j, v in zip(range(len(valores)), valores)]
        fig_radial.add_trace(go.Scatterpolar(
            r=valores_norm,
            theta=categorias_salud,
            fill='toself',
            name=df_salud.loc[i, 'Periodo']
        ))
    fig_radial.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                             title="Salud del Ecosistema - Comparativa Radial")
    st.plotly_chart(fig_radial, use_container_width=True)

with tab4:
    st.header("🛡️ Tasa de Supervivencia por Categoría")
    superv = df_combinado.groupby(['categoria', 'periodo']).size().unstack(fill_value=0)
    superv['Supervivencia %'] = (superv['Después'] / superv['Antes'] * 100).round(1)
    
    st.dataframe(superv.style.background_gradient(cmap='RdYlGn', subset=['Supervivencia %']))
    
    fig_superv = px.bar(superv.reset_index(), x='categoria', y='Supervivencia %',
                        color='Supervivencia %', color_continuous_scale='RdYlGn',
                        title="Tasa de Supervivencia por Categoría")
    fig_superv.update_layout(xaxis_title="Categoría Ecológica", yaxis_title="Supervivencia (%)")
    st.plotly_chart(fig_superv, use_container_width=True)

    # Pie chart para distribución Antes
    st.subheader("Distribución Antes de la Tormenta")
    dist_antes = df_antes.groupby('categoria').size().reset_index(name='Cantidad')
    fig_pie_antes = px.pie(dist_antes, values='Cantidad', names='categoria',
                           title="Distribución Antes de la Tormenta", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie_antes, use_container_width=True)

with tab5:
    st.header("🏷️ Distribución por Categorías Ecológicas - Antes y Después")
    dist = df_combinado.groupby(['categoria', 'periodo']).size().unstack(fill_value=0)
    
    st.dataframe(dist)
    
    fig_dist = px.bar(dist.reset_index(), x='categoria', y=['Antes', 'Después'],
                      title="Distribución por Categorías Ecológicas - Antes y Después", barmode='stack',
                      color_discrete_sequence=['#ADD8E6', '#FFA07A'])
    fig_dist.update_layout(xaxis_title="Categoría Ecológica", yaxis_title="Cantidad de Individuos")
    st.plotly_chart(fig_dist, use_container_width=True)

# =================================== CONCLUSIÓN FINAL ===================================
total_antes = len(entidades_antes)
total_despues = len(entidades_despues)
supervivencia_general = round((total_despues / total_antes * 100) if total_antes > 0 else 0, 1)

st.success(f"""
✅ ANÁLISIS COMPLETADO • Datos 100% reales de los JSON subidos
• Entidades antes: {total_antes}
• Entidades después: {total_despues}
• Supervivencia general: {supervivencia_general}%
""")

if supervivencia_general < 50:
    st.error("⚠️ Impacto severo: El ecosistema está en riesgo de colapso")
elif supervivencia_general < 80:
    st.warning("⚠️ Impacto moderado: Monitorear recuperación")
else:
    st.success("🟢 Buena resiliencia: El ecosistema se mantiene estable")

st.balloons()
