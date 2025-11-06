---

```markdown
# ☕ Proyecto Integrador PI5 – Café de Especialidad  
### Integración de un LLM Open Source con un Grafo de Conocimiento (Neo4j + LangChain + FastAPI)

---

## 📘 Descripción general

Este proyecto implementa un **sistema inteligente de consulta sobre café de especialidad**, integrando:

- **Neo4j AuraDB** (grafo de conocimiento del dominio “café de especialidad”)  
- **LangChain + Ollama** con un modelo **LLM open source (`gpt-oss:120b-cloud`)**  
- **FastAPI + HTML minimalista** como interfaz web de chat

El objetivo es responder preguntas contextualizadas sobre cafés, métodos de preparación, molienda, recetas, perfiles sensoriales y procesos de tueste, combinando **razonamiento semántico del LLM** con **recuperación estructurada desde el grafo**.

---

## 🎯 Objetivo de la actividad

> Actividad PI5 – Unidad 4  
> “Integración de un LLM Open Source con Grafo de Conocimiento”

El propósito es integrar un modelo de lenguaje open source con un grafo de conocimiento Neo4j para responder preguntas en lenguaje natural sobre un dominio definido por el estudiante.

Este dominio seleccionado es **Café de Especialidad**, abarcando entidades como cafés, orígenes, variedades, procesos, métodos de preparación, molienda y recetas.

---

## 🧩 Arquitectura general

```

```
    ┌──────────────────┐
    │  Interfaz HTML   │
    │ (index.html)     │
    └────────┬─────────┘
             │ (POST /chat)
             ▼
    ┌──────────────────┐
    │  FastAPI (main)  │
    └────────┬─────────┘
             │
             ▼
    ┌───────────────────────────────────────────┐
    │ LLM Chain (LangChain + OllamaLLM)         │
    │  - Interpreta pregunta en lenguaje natural │
    │  - Genera consulta Cypher                 │
    │  - Fusiona respuesta del grafo y del LLM  │
    └────────┬──────────────────────────────────┘
             │
             ▼
    ┌──────────────────┐
    │  Neo4j AuraDB    │
    │ (grafo del café) │
    └──────────────────┘
```

```

---

## 📂 Estructura del proyecto

```

pi5-cafe/
├─ .env                     # credenciales y configuración local
├─ requirements.txt         # dependencias
│
├─ neo4j/
│  ├─ seed.cypher           # script para poblar el grafo
│  └─ graph_service.py      # conexión y utilidades para Neo4j
│
├─ llm/
│  ├─ llm_service.py        # configuración del modelo Ollama LLM
│  └─ graph_qa.py           # cadena LLM ↔ Neo4j (GraphCypherQAChain)
│
├─ api/
│  ├─ main.py               # API FastAPI + endpoint /chat
│  └─ templates/
│     └─ index.html         # interfaz web de chat
│
└─ README.md

````

---

## ⚙️ Configuración del entorno

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tuusuario/pi5-cafe.git
cd pi5-cafe
````

### 2️⃣ Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz con tus credenciales:

```bash
# Neo4j AuraDB
NEO4J_URI=neo4j+s://<tu-uri>.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<tu_password>

# Ollama LLM
CLOUD_OLLAMA_URL=http://localhost:11434
LLM_MODEL=gpt-oss:120b-cloud
TEMPERATURE=0.2

# Token simple para la API
API_TOKEN=changeme
```

> 🔒 No subas el `.env` al repositorio si incluye contraseñas reales.

---

## ☁️ Cargar el grafo en Neo4j AuraDB

1. Entrá al **Neo4j Aura Console** o **Neo4j Browser**.
2. Copiá el contenido de `neo4j/seed.cypher`.
3. Ejecutá todo el script (crea nodos, relaciones y constraints).

Para verificar:

```cypher
MATCH (n) RETURN labels(n) AS etiquetas, count(*) AS cantidad ORDER BY cantidad DESC;
```

Deberías ver al menos 10 tipos de nodos con relaciones.

---

## 🤖 Probar el servicio LLM

Antes de la integración completa, probá la comunicación con el modelo:

```bash
python llm/llm_service.py
```

Deberías obtener una respuesta corta como:

```
El pour-over es un método manual de filtrado de café.
```

---

## 🔗 Ejecutar la API

Iniciá la aplicación:

```bash
uvicorn api.main:app --reload
```

Luego abrí en el navegador:

👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 💬 Interfaz web

La interfaz es un chat simple que permite ingresar preguntas sobre el dominio de café.
Ejemplo:

```
¿Qué molido recomienda el grafo para preparar pour-over?
```

El sistema:

1. Envía la pregunta al endpoint `/chat`
2. El LLM genera una consulta Cypher interna
3. Se ejecuta contra Neo4j
4. El modelo produce una respuesta contextualizada en lenguaje natural

---

## 🧠 Ejemplos de preguntas

| Pregunta                                                          | Tipo de razonamiento                   | Ejemplo de respuesta                                                         |
| ----------------------------------------------------------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| ¿Qué molido recomienda el grafo para preparar pour-over?          | Relación Método–Molido                 | “El método pour-over requiere molido medio para una extracción equilibrada.” |
| ¿Cuáles son las notas sensoriales del café Etiopía Washed Sidamo? | Consulta de propiedades y relaciones   | “Presenta notas florales y cítricas, propias de cafés etíopes de altura.”    |
| Mostrame una receta para espresso con su ratio y temperatura.     | Recuperación de nodo `Receta` y `Agua` | “Ratio 1:2, 93°C, tiempo 28 segundos, usando agua filtrada.”                 |

---

## 🧱 Modelo conceptual (simplificado)

```text
(Cafe) -[:ES_DE_ORIGEN]-> (Origen)
(Cafe) -[:ES_DE_VARIEDAD]-> (Variedad)
(Cafe) -[:PROCESADO_COMO]-> (Proceso)
(Cafe) -[:TOSTADO_POR]-> (Tostador)
(Cafe) -[:TIENE_PERFIL]-> (PerfilSensorial)
(Metodo) -[:REQUIERE_MOLIDO]-> (Molido)
(Metodo) -[:IDEAL_PARA]-> (Cafe)
(Receta) -[:PARA_METODO]-> (Metodo)
(Receta) -[:USA_AGUA]-> (Agua)
```

---

## 📊 Tecnologías utilizadas

| Componente                | Tecnología                                          | Descripción                                        |
| ------------------------- | --------------------------------------------------- | -------------------------------------------------- |
| **Grafo de conocimiento** | [Neo4j AuraDB](https://neo4j.com/cloud/aura/)       | Base de datos de grafos administrada               |
| **Modelo LLM**            | [Ollama](https://ollama.com) + `gpt-oss:120b-cloud` | Modelo open source de lenguaje natural             |
| **Integración**           | [LangChain](https://www.langchain.com)              | Framework para orquestar LLMs con datos externos   |
| **Backend API**           | [FastAPI](https://fastapi.tiangolo.com/)            | API moderna en Python                              |
| **Frontend**              | HTML + JavaScript vanilla                           | Chat minimalista para interacción con el asistente |

---

## 🧩 Flujo técnico del sistema

1. El usuario formula una pregunta en lenguaje natural.
2. El LLM interpreta la intención y genera una **consulta Cypher**.
3. La consulta se ejecuta sobre Neo4j para recuperar información.
4. El LLM integra esos resultados y genera una respuesta contextualizada.
5. FastAPI devuelve la respuesta al cliente web.

---

## 🧪 Pruebas sugeridas

1. **Consulta simple:**
   “¿Qué cafés disponibles provienen de Colombia?”
2. **Inferencia combinada:**
   “¿Qué método es ideal para un café de proceso natural?”
3. **Receta detallada:**
   “Mostrame la receta recomendada para pour-over, incluyendo el agua.”

---

## 🚀 Extensiones posibles

* Mostrar el **Cypher generado** y su resultado en la interfaz web.
* Agregar **logging** de preguntas y respuestas (historial de conversación).
* Incluir un **módulo de recomendaciones** (“¿Qué café me sugerís si me gusta el sabor floral?”).
* Entrenar un modelo más liviano local (ej. **Mistral 7B**, **Gemma 7B**) para reducir latencia.
* Desplegar con **Docker Compose** integrando Neo4j + API + UI.

---

## 📜 Licencia

Este proyecto es de carácter académico y educativo, desarrollado para la **Unidad 4 del curso de Inteligencia Artificial (PI5)**.
Su código puede reutilizarse libremente con fines de aprendizaje o demostración.

---

## 👨‍💻 Autor

**Diego Páez**
Estudiante de Ingeniería en Sistemas – Argentina
Proyecto PI5 · Unidad 4 – *Integración de LLM Open Source con Grafo de Conocimiento*
2025

---
