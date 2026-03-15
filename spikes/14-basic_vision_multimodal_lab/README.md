# Practica 14 Basic Vision Multimodal Lab

## Leyenda

1. Vision querying: Consulta una imagen con texto y obtiene una respuesta contextual.
2. Vision messages: Crea mensajes con texto e imagen usando el formato multimodal mas comun.
3. Object detection por pregunta: Responde conteos atributos y lectura simple de texto visual.
4. Similaridad visual ligera: Compara una imagen con un catalogo mediante embeddings deterministas.
5. Prompts especializados: Demuestra un flujo de moda y otro de nutricion sin servicios remotos.
6. Variantes reales con Ollama: Ejemplos separados para `llava` `llama3.2-vision` y `qwen2.5vl`.

## Adaptacion

Esta practica toma ideas de querying visual object detection por prompt y similitud visual y las adapta a una version local y reproducible del repositorio. En lugar de depender de un modelo de vision remoto o de `ResNet50` con pesos externos el spike usa un `VisionDemoModel` y muestras visuales locales codificadas como payloads base64. Esto permite practicar el flujo completo de mensajes multimodales sin costes de infraestructura ni descargas pesadas.

La practica base se mantiene determinista para tests. Ademas incluye tres variantes reales pensadas para `Ollama` que permiten ejecutar el mismo patron con modelos de vision disponibles hoy en su libreria oficial: `llava_vision_querying` `llama3_2_vision_querying` y `qwen2_5vl_vision_querying`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/vision_multimodal_config.py`: URLs locales consultas y parametros del laboratorio.
- `config/vision_real_provider_config.py`: Rutas de imagenes reales prompts y modelos de `Ollama`.
- `data/vision_sample_dataset.py`: Imagenes de muestra y catalogo de moda del ejercicio.
- `assets`: Imagenes locales reales para las variantes con `Ollama`.
- `models/vision_demo_model.py`: Modelo local que responde preguntas visuales de forma determinista.
- `models/vision_ollama_gateway.py`: Cliente HTTP minimo para `Ollama` con imagenes reales.
- `orchestration/vision_image_orchestration.py`: Codificacion de imagenes y construccion de mensajes.
- `orchestration/vision_query_orchestration.py`: Consultas generales nutricion y moda.
- `orchestration/vision_real_variants_orchestration.py`: Flujo compartido para las variantes reales.
- `orchestration/vision_similarity_orchestration.py`: Embeddings deterministas y matching por coseno.
- `orchestration/vision_lab_runner.py`: Ejecucion guiada del laboratorio.
- `llava_vision_querying`: Variante real con `llava`.
- `llama3_2_vision_querying`: Variante real con `llama3.2-vision`.
- `qwen2_5vl_vision_querying`: Variante real con `qwen2.5vl:3b`.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias ya cubiertas por el repo: `numpy`.
3. Para variantes reales: `ollama serve`.
4. Modelos reales opcionales: `ollama pull llava` `ollama pull llama3.2-vision` y `ollama pull qwen2.5vl:3b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\14-basic_vision_multimodal_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_14_basic_vision_multimodal.py`.
4. Variante `llava`: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\llava_vision_querying\main.py`.
5. Variante `llama3.2-vision`: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\llama3_2_vision_querying\main.py`.
6. Variante `qwen2.5vl`: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\qwen2_5vl_vision_querying\main.py`.

## Cobertura

1. `create_vision_message`: Estructura de texto e imagen para un modelo multimodal.
2. `generate_model_response`: Consulta basica sobre una imagen.
3. `generate_nutrition_response`: Analisis de una etiqueta nutricional.
4. `generate_fashion_response`: Analisis orientado a retail con items similares.
5. `find_closest_match`: Matching por similitud coseno sobre embeddings visuales ligeros.
6. `run_llava_example`: Ejemplo real con `llava`.
7. `run_llama32_vision_example`: Ejemplo real con `llama3.2-vision`.
8. `run_qwen25_vl_example`: Ejemplo real con `qwen2.5vl`.
