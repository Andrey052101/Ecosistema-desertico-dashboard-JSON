
# 🌵 Ecosistema Desértico Dinámico – Dashboard en Streamlit

Este proyecto es un **dashboard interactivo** desarrollado en [Streamlit](https://streamlit.io) que analiza los resultados de una **simulación desértica**.  
El sistema carga un archivo **JSON** generado por la simulación y presenta tablas, gráficas y conclusiones sobre fauna, flora y condiciones ambientales.

---

## 📂 Estructura del proyecto

```
mi_dashboard/
│── mi_dashboard.py      # Código principal del dashboard
│── requirements.txt     # Dependencias necesarias
│── data/
│    └── simulacion.json # Archivo JSON de ejemplo (opcional)
```

---

## ⚙️ Instalación local

1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/mi_dashboard.git
   cd mi_dashboard
   ```

2. Crea un entorno virtual e instala dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/Mac
   venv\Scripts\activate      # En Windows
   pip install -r requirements.txt
   ```

---

## ▶️ Ejecución local

Ejecuta el dashboard con:
```bash
streamlit run mi_dashboard.py
```

Esto abrirá la aplicación en tu navegador en `http://localhost:8501`.

---

## 🌐 Despliegue en Streamlit Cloud

1. Sube tu proyecto a **GitHub**.  
2. Ve a [Streamlit Cloud](https://streamlit.io/cloud).  
3. Conecta tu repositorio y despliega la app.  
4. Obtendrás un enlace público como:

```
https://mi-dashboard.streamlit.app
```

👉 Si quieres **otro link público**, simplemente crea **otro repositorio en GitHub** (por ejemplo `mi_dashboard_v2`) o despliega otra rama distinta. Cada despliegue tendrá su propio enlace independiente.

---

## 🔄 Actualización del dashboard

Cada vez que modifiques tu código o el archivo `simulacion.json`:

```bash
git add .
git commit -m "Actualización de datos de simulación"
git push origin main
```

Streamlit Cloud reconstruirá la aplicación automáticamente.  
El **link público no cambia**, pero los usuarios verán la versión más reciente.

---

## 📊 Funcionalidades principales

- Lectura automática del archivo `simulacion.json`.  
- Tablas dinámicas con nombres traducidos al español.  
- Gráficas comparativas de valores iniciales vs finales.  
- Pestañas para separar ambiente, fauna, flora, eventos y equilibrio ecológico.  
- Conclusiones automáticas basadas en los datos.  

---

## 📦 Dependencias

Incluidas en `requirements.txt`:

```
streamlit
pandas
plotly
```

---

## 👨‍💻 Autores

Proyecto desarrollado por:
- William Andrey Chaves  
- Jhon Mateus  
- Cesar Villalba  

Con enfoque en accesibilidad, claridad y estética narrativa para que cualquier usuario pueda comprender los resultados de la simulación desértica.
  

