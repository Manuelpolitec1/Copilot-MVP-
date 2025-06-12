import streamlit as st
import openai

# --- Configuración segura de la API ---
openai.api_key = st.secrets["openai"]["api_key"]  # o pon tu clave directamente aquí si es local

# --- Función para generar la recomendación ---
def generar_recomendacion(pregunta_gerente, tono_hospitalidad=True):
    """
    Genera una recomendación usando un LLM de OpenAI, con o sin tono de hospitalidad.
    """
    system_message = """
    Eres un Co-Piloto de gestión enfocado en la industria de la hospitalidad.
    Tu objetivo es proporcionar recomendaciones prácticas, procesables y alineadas con
    los estándares operativos (SOPs) y las mejores prácticas del sector.
    Mantén un tono profesional, cortés y positivo.
    Las recomendaciones deben ser claras, concisas y orientadas a resultados.
    """ if tono_hospitalidad else """
    Eres un asistente de gestión general que proporciona recomendaciones prácticas y procesables.
    Mantén un tono profesional y objetivo.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Cambia a gpt-3.5-turbo si no tienes acceso a GPT-4
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": pregunta_gerente}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"Error de la API: {e}")
        return "Lo siento, hubo un error al comunicarse con OpenAI."
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        return "Lo siento, no se pudo generar la recomendación."

# --- Interfaz Streamlit ---
st.set_page_config(page_title="Co-Piloto de Gestión de Hospitalidad", layout="centered")

st.image(
    "https://images.unsplash.com/photo-1549646549-3a3c2b8b9b8b?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    width=100
)

st.title("🤝 Co-Piloto de Gestión de Hospitalidad")
st.markdown("Bienvenido, gerente. Estoy aquí para ayudarte a tomar mejores decisiones en tus operaciones.")

# Entrada de usuario
pregunta = st.text_area(
    "¿En qué puedo ayudarte hoy?",
    height=100,
    placeholder="Ej: ¿Cómo puedo aumentar los ingresos de alimentos y bebidas?"
)

# Tono
tono_hospitalidad_activado = st.checkbox("Activar tono de hospitalidad/SOP", value=True)

# Botón de acción
if st.button("Obtener Recomendación"):
    if pregunta.strip():
        with st.spinner("Generando recomendación..."):
            recomendacion = generar_recomendacion(pregunta, tono_hospitalidad_activado)
            st.subheader("💡 Recomendación:")
            st.write(recomendacion)
    else:
        st.warning("Por favor, escribe una pregunta.")

# Footer
st.markdown("---")
st.markdown("Desarrollado con ❤️ para líderes de hospitalidad. Potenciado por OpenAI.")
