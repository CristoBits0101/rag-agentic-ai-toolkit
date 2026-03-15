# --- LEYENDA ---
# 1. Gradio: Componentes para construir la interfaz.
# 2. Ollama Llama: Modelo local para responder desde la practica.
# 3. Practica: Suma formulario y Llama en una sola interfaz.

# --- INSTALACION ---
# 1. Ollama: irm https://ollama.com/install.ps1 | iex.
# 2. Llama 3.2 3B: ollama pull llama3.2:3b.
# 3. Gradio: pip install -U gradio.
# 4. LangChain Ollama: pip install -U langchain-ollama.

# --- VERIFICACION ---
# 1. Ollama: ollama --version.
# 2. Ollama Servidor: ollama serve.
# 3. Ollama Modelos: ollama list.
# 4. Gradio: pip show gradio.

# --- DEPENDENCIAS ---
# 1. Gradio: Para construir la interfaz visual.
import gradio as gr

# --- CONFIGURACION ---
# 1. Modelo: Llama local servido por Ollama.
# 2. Host: Direccion local para lanzar Gradio.
# 3. Puerto: Puerto de la practica.
MODEL_NAME = "llama3.2:3b"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7860

# --- MODELO ---
_llama_model = None


# 1.1. Funcion para cargar el modelo solo una vez.
def get_llama_model():
    # Reutiliza la misma instancia para evitar recargar el modelo en cada llamada.
    global _llama_model

    if _llama_model is None:
        # Importa el cliente solo cuando realmente se necesita el modelo.
        from langchain_ollama import OllamaLLM

        # Crea la conexion local con Ollama usando una configuracion simple.
        _llama_model = OllamaLLM(
            model=MODEL_NAME,
            temperature=0.3,
            top_p=0.9,
            top_k=40,
            num_predict=256,
        )

    # Devuelve la instancia lista para reutilizar.
    return _llama_model


# --- PASO 1: SUMA SIMPLE ---
# 1.2. Funcion para validar una interaccion numerica minima.
def add_numbers(first_number: float, second_number: float) -> float:
    # Devuelve la suma directa de los dos valores introducidos.
    return first_number + second_number


# --- PASO 2: FORMULARIO GUIADO ---
# 2.1. Funcion para construir una frase desde varios componentes.
def build_sentence(
    quantity: int,
    role: str,
    countries: list[str],
    place: str,
    activities: list[str],
    morning: bool,
) -> str:
    # Obliga a seleccionar al menos un pais para evitar una frase incompleta.
    if not countries:
        return "Selecciona al menos un pais."

    # Obliga a seleccionar al menos una actividad para mantener sentido en la salida.
    if not activities:
        return "Selecciona al menos una actividad."

    # Convierte los valores del formulario en texto listo para mostrar.
    time_of_day = "manana" if morning else "noche"
    countries_text = " y ".join(countries)
    activities_text = " y ".join(activities)

    # Construye una sola frase final con el contenido del formulario.
    return (
        f"{quantity} {role.lower()} de {countries_text} fueron a {place} "
        f"donde {activities_text} hasta la {time_of_day}."
    )


# --- PASO 3: LLAMA LOCAL ---
# 3.1. Objetivos disponibles para el prompt final.
PROMPTS_BY_GOAL = {
    "Explicar": "Explica el contenido con lenguaje claro y directo.",
    "Resumir": "Resume el contenido en una sola frase.",
    "Traducir": "Traduce el contenido al espanol.",
}


# 3.2. Funcion para ejecutar una tarea minima con Llama.
def run_llama_step(goal: str, user_text: str) -> str:
    # Limpia espacios para evitar enviar prompts vacios al modelo.
    cleaned_text = user_text.strip()

    if not cleaned_text:
        return "Escribe una pregunta o un texto."

    # Une objetivo y contenido en un prompt corto y directo.
    prompt = (
        f"{PROMPTS_BY_GOAL[goal]}\n\n"
        f"Contenido:\n{cleaned_text}\n\n"
        "Respuesta:"
    )

    try:
        # Ejecuta el prompt contra Llama local servido por Ollama.
        response = get_llama_model().invoke(prompt)
    except Exception as exc:
        # Devuelve el error como texto para que se vea dentro de la interfaz.
        return f"No se pudo ejecutar Llama: {exc}"

    # Normaliza la salida final antes de mostrarla en Gradio.
    return str(response).strip()


# --- INTERFAZ ---
# gr.Blocks: Crea el contenedor principal de toda la interfaz.
#     title: Nombre de la interfaz en la pestana del navegador.
#   as demo: Guarda la app en una variable para luego poder lanzarla con demo.launch().
with gr.Blocks(title="Practica 02 Gradio con Llama") as demo:
    # gr.Markdown: Muestra una guia en la parte superior de la interfaz.
    gr.Markdown(
        """
# Practica 02: Gradio con Llama.
Paso 1: Prueba una interaccion numerica simple.
Paso 2: Prueba componentes de formulario.
Paso 3: Ejecuta Llama local para una tarea concreta.
Requisito: Ejecuta `ollama serve` y descarga `llama3.2:3b`.
"""
    )

    # gr.Accordion: Crea una seccion desplegable para el primer ejercicio.
    #     label: Titulo visible de la seccion.
    #     open: Hace que la seccion aparezca abierta al cargar la pagina.
    with gr.Accordion("Paso 1: Sumadora.", open=True):
        # gr.Row: Organiza los componentes de entrada en una fila horizontal.
        with gr.Row():
            # gr.Number: Crea un campo numerico para el primer valor.
            #     label: Texto visible del campo.
            #     value: Valor inicial mostrado en la interfaz.
            first_number = gr.Number(label="Numero 1", value=1)
            # gr.Number: Crea un campo numerico para el segundo valor.
            #     label: Texto visible del campo.
            #     value: Valor inicial mostrado en la interfaz.
            second_number = gr.Number(label="Numero 2", value=2)

        # gr.Number: Muestra el resultado numerico devuelto por la suma.
        #     label: Texto visible del campo de salida.
        sum_output = gr.Number(label="Resultado")
        # gr.Button: Ejecuta la suma cuando el usuario pulsa el boton.
        #     value: Texto visible del boton.
        sum_button = gr.Button("Sumar")

        # sum_button.click: Conecta el boton con la funcion de suma.
        #     fn: Funcion que se ejecuta al pulsar el boton.
        #     inputs: Componentes cuyos valores se envian a la funcion.
        #     outputs: Componente donde se escribe el resultado devuelto.
        sum_button.click(
            fn=add_numbers,
            inputs=[first_number, second_number],
            outputs=sum_output,
        )

    # gr.Accordion: Crea una seccion desplegable para el formulario guiado.
    #     label: Titulo visible de la seccion.
    #     open: Hace que la seccion aparezca abierta al cargar la pagina.
    with gr.Accordion("Paso 2: Constructor de frase.", open=True):
        # gr.Slider: Permite elegir una cantidad dentro de un rango.
        #     minimum: Valor minimo permitido.
        #     maximum: Valor maximo permitido.
        #     value: Valor inicial mostrado en la interfaz.
        #     step: Incremento aplicado al mover el control.
        #     label: Texto visible del campo.
        quantity = gr.Slider(1, 10, value=3, step=1, label="Cantidad")
        # gr.Dropdown: Permite elegir un rol desde una lista desplegable.
        #     choices: Opciones disponibles para seleccionar.
        #     value: Valor inicial mostrado en la interfaz.
        #     label: Texto visible del campo.
        role = gr.Dropdown(
            choices=["Data Scientist", "Software Developer", "Software Engineer"],
            value="Software Developer",
            label="Rol",
        )
        # gr.CheckboxGroup: Permite seleccionar varios paises a la vez.
        #     choices: Opciones disponibles para seleccionar.
        #     value: Valores iniciales marcados en la interfaz.
        #     label: Texto visible del campo.
        countries = gr.CheckboxGroup(
            choices=["Canada", "Japan", "France"],
            value=["Canada"],
            label="Paises",
        )
        # gr.Radio: Permite elegir un lugar entre varias opciones visibles.
        #     choices: Opciones disponibles para seleccionar.
        #     value: Valor inicial marcado en la interfaz.
        #     label: Texto visible del campo.
        place = gr.Radio(
            choices=["la oficina", "el restaurante", "la sala de reunion"],
            value="la oficina",
            label="Lugar",
        )
        # gr.Dropdown: Permite elegir varias actividades desde una lista.
        #     choices: Opciones disponibles para seleccionar.
        #     value: Valores iniciales mostrados en la interfaz.
        #     multiselect: Permite seleccionar varias opciones.
        #     label: Texto visible del campo.
        activities = gr.Dropdown(
            choices=["brainstormed", "coded", "fixed bugs", "partied"],
            value=["brainstormed"],
            multiselect=True,
            label="Actividades",
        )
        # gr.Checkbox: Permite indicar si la escena ocurre por la manana.
        #     label: Texto visible del campo.
        morning = gr.Checkbox(label="Manana")

        # gr.Textbox: Muestra la frase construida por el formulario.
        #     label: Texto visible del campo de salida.
        sentence_output = gr.Textbox(label="Frase")
        # gr.Button: Ejecuta la construccion de la frase final.
        #     value: Texto visible del boton.
        sentence_button = gr.Button("Construir frase")

        # sentence_button.click: Conecta el formulario con la funcion que arma la frase final.
        #     fn: Funcion que se ejecuta al pulsar el boton.
        #     inputs: Componentes cuyos valores se envian a la funcion.
        #     outputs: Componente donde se escribe el resultado devuelto.
        sentence_button.click(
            fn=build_sentence,
            inputs=[quantity, role, countries, place, activities, morning],
            outputs=sentence_output,
        )

    # gr.Accordion: Crea una seccion desplegable para usar el modelo local.
    #     label: Titulo visible de la seccion.
    #     open: Hace que la seccion aparezca abierta al cargar la pagina.
    with gr.Accordion("Paso 3: Llama local.", open=True):
        # gr.Dropdown: Permite elegir el objetivo de la tarea del modelo.
        #     choices: Opciones disponibles para seleccionar.
        #     value: Valor inicial mostrado en la interfaz.
        #     label: Texto visible del campo.
        goal = gr.Dropdown(
            choices=["Explicar", "Resumir", "Traducir"],
            value="Explicar",
            label="Objetivo",
        )

        # gr.Textbox: Recoge el texto libre que se enviara al modelo.
        #     label: Texto visible del campo.
        #     lines: Altura inicial del cuadro de texto.
        #     placeholder: Texto de ayuda mostrado antes de escribir.
        user_text = gr.Textbox(
            label="Texto o pregunta",
            lines=6,
            placeholder="Escribe aqui el contenido para Llama.",
        )

        # gr.Textbox: Muestra la respuesta generada por el modelo local.
        #     label: Texto visible del campo de salida.
        #     lines: Altura inicial del cuadro de texto.
        llama_output = gr.Textbox(label="Respuesta", lines=10)
        # gr.Button: Ejecuta la consulta al modelo local.
        #     value: Texto visible del boton.
        llama_button = gr.Button("Ejecutar Llama")

        # llama_button.click: Conecta el boton con la funcion que ejecuta Llama.
        #     fn: Funcion que se ejecuta al pulsar el boton.
        #     inputs: Componentes cuyos valores se envian a la funcion.
        #     outputs: Componente donde se escribe el resultado devuelto.
        llama_button.click(
            fn=run_llama_step,
            inputs=[goal, user_text],
            outputs=llama_output,
        )


if __name__ == "__main__":
    # Lanza la practica en local usando la configuracion definida arriba.
    demo.launch(server_name=SERVER_HOST, server_port=SERVER_PORT)
