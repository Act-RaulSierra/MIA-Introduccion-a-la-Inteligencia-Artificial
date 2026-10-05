import os
import streamlit as st
import httpx

API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Sistema RAG - Panel de Control",
    layout="wide",
    initial_sidebar_state="expanded"
)


def check_api_health():
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=3.0)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def main():
    st.title("Sistema RAG: Streamlit + FastAPI + ChromaDB + Google AI")
    st.caption("Arquitectura modular de recuperación documental, embeddings vectoriales y generación anclada.")

    with st.sidebar:
        st.header("Estado del Sistema")
        health_info = check_api_health()
        
        if health_info and health_info.get("status") == "ok":
            st.success("API FastAPI: Conectada")
            st.info(f"ChromaDB: {health_info.get('chroma_status')}")
            st.metric(label="Documentos / Chunks Persistidos", value=health_info.get("total_documents", 0))
            st.caption(f"Ruta ChromaDB: {health_info.get('persist_directory')}")
        else:
            st.error("API FastAPI: No disponible (http://127.0.0.1:8000)")
            st.warning("Asegúrese de ejecutar el servidor FastAPI antes de realizar consultas.")

        st.divider()
        st.header("Configuración de Consulta")
        top_k = st.slider("Chunks a recuperar (top_k)", min_value=1, max_value=10, value=3)

    tab_ingest, tab_query = st.tabs(["Ingesta de Documentos", "Consulta RAG"])

    with tab_ingest:
        st.subheader("Cargar Documentos a la Base Vectorial")
        st.write("Soporta archivos en formato .txt, .md y .pdf.")

        upload_option = st.radio("Método de ingesta:", ["Subir Archivo Local", "Ruta de Archivo en Servidor"])

        if upload_option == "Subir Archivo Local":
            uploaded_file = st.file_uploader("Seleccione un archivo:", type=["txt", "md", "pdf"])
            if st.button("Ingestar Archivo Subido"):
                if uploaded_file is not None:
                    with st.spinner("Procesando, generando chunks y calculando embeddings..."):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                            res = httpx.post(f"{API_BASE_URL}/ingest", files=files, timeout=60.0)
                            if res.status_code == 200:
                                data = res.json()
                                st.success(f"Éxito: {data.get('message')}")
                                st.write(f"Chunks generados: {data.get('total_chunks')}")
                                st.write(f"Vectores insertados: {data.get('inserted_count')}")
                            else:
                                err_detail = res.json().get("detail", res.text)
                                st.error(f"Error HTTP {res.status_code}: {err_detail}")
                        except Exception as e:
                            st.error(f"Error de conexión con la API: {str(e)}")
                else:
                    st.warning("Por favor seleccione un archivo antes de continuar.")

        else:
            file_path_input = st.text_input("Ruta absoluta del archivo en servidor:")
            if st.button("Ingestar desde Ruta"):
                if file_path_input.strip():
                    with st.spinner("Procesando archivo desde ruta local..."):
                        try:
                            data_form = {"file_path": file_path_input.strip()}
                            res = httpx.post(f"{API_BASE_URL}/ingest", data=data_form, timeout=60.0)
                            if res.status_code == 200:
                                data = res.json()
                                st.success(f"Éxito: {data.get('message')}")
                                st.write(f"Chunks generados: {data.get('total_chunks')}")
                                st.write(f"Vectores insertados: {data.get('inserted_count')}")
                            else:
                                err_detail = res.json().get("detail", res.text)
                                st.error(f"Error HTTP {res.status_code}: {err_detail}")
                        except Exception as e:
                            st.error(f"Error de conexión con la API: {str(e)}")
                else:
                    st.warning("Por favor ingrese una ruta de archivo válida.")

    with tab_query:
        st.subheader("Consultar la Base de Conocimiento")
        question_text = st.text_area("Ingrese su pregunta:", height=100, placeholder="Ejemplo: ¿Qué función cumple el protocolo TCP en la capa de transporte?")

        if st.button("Ejecutar Consulta RAG"):
            if question_text.strip():
                with st.spinner("Generando vector de pregunta, buscando evidencia y orquestando respuesta..."):
                    try:
                        payload = {
                            "question": question_text.strip(),
                            "top_k": top_k
                        }
                        res = httpx.post(f"{API_BASE_URL}/query", json=payload, timeout=45.0)
                        
                        if res.status_code == 200:
                            data = res.json()
                            answered = data.get("answered", False)
                            answer = data.get("answer", "")
                            reason = data.get("reason", "")
                            citations = data.get("citations", [])
                            chunks = data.get("retrieved_chunks", [])

                            st.markdown("### Respuesta Generada")
                            if answered:
                                st.success("Estado: Respuesta Respondida y Anclada")
                            else:
                                st.warning(f"Estado: Abstención Activada - {reason}")

                            st.markdown(f"> {answer}")

                            if citations:
                                st.markdown("### Citas y Fuentes")
                                for c in citations:
                                    st.write(f"- Cita {c.get('citation_id')}: Archivo '{c.get('source')}', Chunk #{c.get('chunk_index')} (Distancia: {c.get('distance'):.4f})")

                            st.divider()
                            st.markdown("### Chunks Recuperados de ChromaDB")
                            if chunks:
                                for i, chunk in enumerate(chunks, start=1):
                                    with st.expander(f"Chunk [{i}] - {chunk.get('source')} (Chunk Index: {chunk.get('chunk_index')}, Distancia: {chunk.get('distance'):.4f})"):
                                        st.text_area(f"Texto Chunk [{i}]", value=chunk.get("text"), height=150, key=f"chunk_{i}")
                            else:
                                st.info("No se recuperaron chunks para esta consulta.")

                        else:
                            err_detail = res.json().get("detail", res.text)
                            st.error(f"Error en la consulta HTTP {res.status_code}: {err_detail}")
                    except Exception as e:
                        st.error(f"Error de conexión con el servidor FastAPI: {str(e)}")
            else:
                st.warning("Ingrese una pregunta antes de consultar.")


if __name__ == "__main__":
    main()
