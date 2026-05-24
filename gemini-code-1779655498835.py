import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página para dispositivos móviles
st.set_page_config(page_title="Formato de Auditoría", page_icon="📋", layout="centered")

st.title("📋 Formato Digital de Auditoría")
st.write("Complete los campos para generar el registro y el informe final.")

# ==========================================
# 1. DATOS GENERALES Y CONFIGURACIÓN
# ==========================================
st.subheader("1. Datos Generales")
col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input("Empresa auditada", "Empresa Alfa S.A.")
    auditor = st.text_input("Auditor responsable", "Ing. Carlos Mendoza")
with col2:
    tipo_auditoria = st.selectbox("Tipo de auditoría", ["Interna", "Externa", "De Certificación", "De Seguimiento"])
    fecha = st.date_input("Fecha de auditoría", datetime.now())

objetivo = st.text_area("Objetivo de la auditoría", "Evaluar la eficacia del proceso bajo los estándares establecidos.")
alcance = st.text_area("Alcance", "Procesos, áreas o sistemas evaluados.")
criterios = st.text_area("Criterios de evaluación", "Normas, procedimientos o requisitos aplicables.")

st.markdown("---")

# ==========================================
# 2. LISTA DE VERIFICACIÓN (CHECKLIST)
# ==========================================
st.subheader("2. Lista de Verificación y Hallazgos")
st.info("Evalúe cada punto de control, registre la evidencia y determine el hallazgo.")

# Definición de preguntas base
preguntas = [
    "¿El personal conoce la política y los objetivos del área?",
    "¿Se encuentran actualizados los procedimientos y documentos del proceso?",
    "¿Existen registros que evidencien la ejecución de las actividades obligatorias?",
    "¿Se realiza el seguimiento a los indicadores de gestión definidos?"
]

resultados = []

for i, pregunta in enumerate(preguntas, 1):
    st.markdown(f"**Punto {i}: {pregunta}**")
    
    # Parámetros de selección de hallazgos
    estado = sk = st.radio(
        f"Resultado Punto {i}",
        ["Cumple", "No Conformidad", "Observación", "Oportunidad de Mejora"],
        key=f"estado_{i}",
        horizontal=True
    )
    
    evidencia = st.text_input(f"Evidencias / Registros revisados (Punto {i})", key=f"evidencia_{i}", placeholder="Ej. Registro REG-01, entrevista con...")
    
    resultados.append({
        "Punto de Control": pregunta,
        "Estado/Hallazgo": estado,
        "Evidencia": evidencia
    })
    st.markdown(" ")

# Convertir resultados a un DataFrame para procesar datos
df_resultados = pd.DataFrame(resultados)

st.markdown("---")

# ==========================================
# 3. CONCLUSIONES Y RECOMENDACIONES (AUTOMÁTICAS)
# ==========================================
st.subheader("3. Resumen Ejecutivo y Conclusiones")

# Cálculos de métricas en tiempo real
total_puntos = len(df_resultados)
cumpleaños = len(df_resultados[df_resultados["Estado/Hallazgo"] == "Cumple"])
no_conformidades = len(df_resultados[df_resultados["Estado/Hallazgo"] == "No Conformidad"])
porcentaje_cumplimiento = (cumpleaños / total_puntos) * 100

# Mostrar indicadores visuales
c_m1, c_m2 = st.columns(2)
c_m1.metric("Porcentaje de Cumplimiento", f"{porcentaje_cumplimiento:.1f}%")
c_m2.metric("No Conformidades Detectadas", no_conformidades)

# Generación automática de texto de conclusiones
st.markdown("**Conclusiones Generales:**")
if no_conformidades > 0:
    conclusion_automatica = f"La auditoría en **{empresa}** concluye con un **{porcentaje_cumplimiento:.1f}%** de cumplimiento. Se identificaron {no_conformidades} No Conformidades que requieren atención inmediata para evitar desviaciones críticas en el sistema."
else:
    conclusion_automatica = f"La auditoría en **{empresa}** concluye de manera satisfactoria con un **100%** de cumplimiento de los puntos evaluados. El sistema se muestra maduro y operativo."

conclusiones = st.text_area("Conclusiones finales (Editable)", value=conclusion_automatica)
recomendaciones = st.text_area("Recomendaciones / Acciones sugeridas", "Se sugiere implementar planes de acción correctiva para las No Conformidades y realizar seguimiento en un plazo de 30 días.")

# ==========================================
# 4. EXPORTAR RESULTADOS
# ==========================================
st.markdown("---")
if st.button("💾 Guardar y preparar reporte para descarga"):
    st.success("¡Reporte procesado exitosamente!")
    
    # Crear un archivo de texto plano simulando el informe final terminado
    reporte_txt = f"""INFORME DE AUDITORÍA
Empresa: {empresa}
Tipo: {tipo_auditoria}
Fecha: {fecha}
Auditor: {auditor}
-------------------------------------------
Objetivo: {objetivo}
Alcance: {alcance}
Criterios: {criterios}
-------------------------------------------
CONCLUSIONES:
{conclusiones}

RECOMENDACIONES:
{recomendaciones}
"""
    st.download_button(
        label="⬇️ Descargar Reporte (.TXT)",
        data=reporte_txt,
        file_name=f"Auditoria_{empresa}_{fecha}.txt",
        mime="text/plain"
    )