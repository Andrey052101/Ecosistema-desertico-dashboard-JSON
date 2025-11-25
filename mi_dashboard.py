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
import matplotlib.pyplot as plt

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
            if nombre_esp in lista or ' ' in nombre_esp:
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
    cambios.columns = ['Antes', 'Después']
    cambios['Cambio'] = cambios['Después'] - cambios['Antes']
    cambios['% Cambio'] = ((cambios['Cambio'] / cambios['Antes']) * 100).round(1).replace([np.inf, -np.inf], np.nan)
    
    st.dataframe(cambios.style.background_gradient(cmap='RdYlGn', subset=['Cambio']))
    
    # Gráfico con matplotlib para matching exacto
    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(cambios))
    width = 0.35
    ax.bar([i - width/2 for i in x], cambios['Antes'], width, label='Antes', color='#ADD8E6', alpha=0.7)
    ax.bar([i + width/2 for i in x], cambios['Después'], width, label='Después', color='#FFA07A', alpha=0.7)
    ax.set_xlabel('Especies')
    ax.set_ylabel('Cantidad de Individuos')
    ax.set_title('Cambios Poblacionales por Especie - Antes vs Después de la Tormenta')
    ax.set_xticks(x)
    ax.set_xticklabels(cambios.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    for i, (idx, row) in enumerate(cambios.iterrows()):
        cambio = row['Cambio']
        if cambio != 0:
            ax.annotate(f"{int(cambio):+}", (i, max(row['Antes'], row['Después']) + 0.5),
                        ha='center', va='bottom', fontweight='bold')
    st.pyplot(fig)

with tab2:
    st.header("🗺️ Distribución 3D del Ecosistema - Antes y Después de la Tormenta")
    col3d1, col3d2 = st.columns(2)
    
    with col3d1:
        st.subheader("🌵 Antes de la Tormenta")
        fig_3d_antes = px.scatter_3d(df_antes, x='x', y='y', z='z', color='categoria',
                                     hover_data=['nombre_es'], title="Distribución 3D Antes de la Tormenta")
        fig_3d_antes.update_layout(scene_aspectmode='cube')
        st.plotly_chart(fig_3d_antes, use_container_width=True)
    
    with col3d2:
        st.subheader("🌧️ Después de la Tormenta")
        fig_3d_despues = px.scatter_3d(df_despues, x='x', y='y', z='z', color='categoria',
                                       hover_data=['nombre_es'], title="Distribución 3D Después de la Tormenta")
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
            'Densidad': round(total / (df['x'].max() - df['x'].min() + 1) if len(df) > 0 else 0, 2),
            'Balance (Carn/Herb)': round(balance, 2),
            'Crías (reproducción)': crias,
            'Salud General': round((diversidad + crias) / total * 100 if total > 0 else 0, 1)
        })
    
    df_salud = pd.DataFrame(metricas)
    st.dataframe(df_salud, use_container_width=True)
    
    # Gráfico radial con matplotlib para matching
    fig_rad, ax_rad = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    theta = np.linspace(0, 2 * np.pi, len(categorias_ecologicas), endpoint=False)
    values_antes = [len(df_antes[df_antes['categoria'] == cat]) for cat in categorias_ecologicas]
    values_despues = [len(df_despues[df_despues['categoria'] == cat]) for cat in categorias_ecologicas]
    
    ax_rad.fill(theta, values_antes, color='blue', alpha=0.25)
    ax_rad.fill(theta, values_despues, color='orange', alpha=0.25)
    ax_rad.set_ylim(0, max(max(values_antes), max(values_despues)))
    ax_rad.set_title('Salud del Ecosistema - Comparativa Radial')
    
    st.pyplot(fig_rad)

with tab4:
    st.header("🛡️ Tasa de Supervivencia por Categoría")
    superv = df_combinado.groupby(['categoria', 'periodo']).size().unstack(fill_value=0)
    superv['Supervivencia %'] = (superv['Después'] / superv['Antes'] * 100).round(1)
    
    st.dataframe(superv.style.background_gradient(cmap='RdYlGn', subset=['Supervivencia %']))
    
    # Gráfico bar con pie para matching
    fig_superv, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Bar
    ax_bar.bar(superv.index, superv['Supervivencia %'], color=['green' if p > 80 else 'orange' if p > 50 else 'red' for p in superv['Supervivencia %']])
    ax_bar.set_title('Tasa de Supervivencia por Categoría')
    ax_bar.set_ylabel('Supervivencia (%)')
    ax_bar.set_xticklabels(superv.index, rotation=45)
    ax_bar.axhline(50, color='red', linestyle='--', alpha=0.5)
    
    # Pie
    sizes_antes = df_antes.groupby('categoria').size()
    ax_pie.pie(sizes_antes, labels=sizes_antes.index, autopct='%1.1f%%', colors=['green', 'red', 'orange', 'blue'])
    ax_pie.set_title('Distribución Antes de la Tormenta')
    
    st.pyplot(fig_superv)

with tab5:
    st.header("🏷️ Distribución por Categorías Ecológicas - Antes y Después")
    dist = df_combinado.groupby(['categoria', 'periodo']).size().unstack(fill_value=0)
    
    st.dataframe(dist)
    
    # Gráfico stacked bar con labels para matching
    fig_dist, ax_dist = plt.subplots(figsize=(12, 6))
    categorias = dist.index
    antes = dist['Antes']
    despues = dist['Después']
    x = range(len(categorias))
    ax_dist.bar(x, antes, label='Antes', color='#ADD8E6', alpha=0.7)
    ax_dist.bar(x, despues, bottom=antes, label='Después', color='#FFA07A', alpha=0.7)
    ax_dist.set_title('Distribución por Categorías Ecológicas - Antes y Después')
    ax_dist.set_xlabel('Categorías')
    ax_dist.set_ylabel('Cantidad de Individuos')
    ax_dist.set_xticks(x)
    ax_dist.set_xticklabels(categorias, rotation=45)
    ax_dist.legend()
    ax_dist.grid(True, alpha=0.3)
    
    for i in x:
        ax_dist.text(i, antes[i]/2, str(antes[i]), ha='center', va='center', color='black')
        ax_dist.text(i, antes[i] + despues[i]/2, str(despues[i]), ha='center', va='center', color='black')
    
    st.pyplot(fig_dist)

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
