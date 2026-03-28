# Practica 14 Basic Vision Multimodal Lab

## Leyenda

1. Vision querying: Consulta una imagen con texto y obtiene una respuesta contextual.
2. Vision messages: Crea mensajes con texto e imagen usando el formato multimodal mas comun.
3. Object detection por pregunta: Responde conteos atributos y lectura simple de texto visual.
4. Similaridad visual ligera: Compara una imagen con un catalogo mediante embeddings visuales locales.
5. Prompts especializados: Demuestra un flujo de moda y otro de nutricion sin servicios remotos.
6. Variantes reales con Ollama: Ejemplos separados para `llava` `llama3.2-vision` y `qwen2.5vl`.
7. Style Finder avanzado: App de moda con retrieval visual dataset estructurado y analisis catalogado con `Gradio`.
8. Nutrition Coach visual: App `Flask` para estimar calorias y desglosar nutrientes desde una foto.

## Adaptacion

Esta practica toma ideas de querying visual object detection por prompt y similitud visual y las adapta a una version local y reproducible del repositorio. La ejecucion base usa un modelo real de vision en `Ollama` con imagenes locales y mensajes multimodales reales.

Las variantes incluidas permiten ejecutar el mismo patron con distintos modelos de vision disponibles hoy en `Ollama`: `llava_vision_querying` `llama3_2_vision_querying` y `qwen2_5vl_vision_querying`.

Esta practica absorbe la parte de la cheat sheet centrada en vision multimodal. Aqui viven `Image Captioning` `Image Encoding` `Message Formatting` `Model Invocation` `Object Detection` por pregunta consultas visuales con mensajes de texto e imagen y captioning en lote sobre varias imagenes.

La extension `Style Finder` lleva la practica al siguiente nivel con un flujo `multimodal RAG` aplicado a moda. Construye ejemplos locales de outfits calcula embeddings visuales gratuitos con backend automatico genera retrieval sobre un dataset estructurado y permite analisis con `llama3.2-vision` `llava` o `qwen2.5vl` a traves de `Ollama`.

La extension `Nutrition Coach` aplica el mismo patron a imagenes de comida con una interfaz `Flask`. Genera ejemplos locales de platos hace retrieval visual sobre un dataset nutricional estructurado y produce una respuesta multimodal real sobre `Ollama`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/vision_multimodal_config.py`: URLs locales consultas y parametros del laboratorio.
- `config/vision_real_provider_config.py`: Rutas de imagenes reales prompts y modelos de `Ollama`.
- `data/vision_sample_dataset.py`: Imagenes de muestra y catalogo de moda del ejercicio.
- `assets`: Imagenes locales reales para las variantes con `Ollama`.
- `models/vision_ollama_gateway.py`: Cliente HTTP minimo para `Ollama` con imagenes reales.
- `orchestration/vision_image_orchestration.py`: Codificacion de imagenes y construccion de mensajes.
- `orchestration/vision_query_orchestration.py`: Consultas generales nutricion y moda.
- `orchestration/vision_real_variants_orchestration.py`: Flujo compartido para las variantes reales.
- `orchestration/vision_similarity_orchestration.py`: Embeddings visuales locales y matching por coseno.
- `orchestration/vision_lab_runner.py`: Ejecucion guiada del laboratorio.
- `config/style_finder_fashion_config.py`: Configuracion de la extension avanzada Style Finder.
- `config/nutrition_coach_config.py`: Configuracion de la extension Nutrition Coach.
- `data/nutrition_coach_dataset.py`: Dataset estructurado de platos y nutrientes.
- `data/style_finder_fashion_dataset.py`: Dataset estructurado de looks y prendas para moda.
- `models/nutrition_coach_image_processor.py`: Procesador visual reutilizable para la app de nutricion.
- `models/nutrition_coach_llm_service.py`: Servicio de nutricion sobre modelos de vision en `Ollama`.
- `models/style_finder_image_processor.py`: Codificacion de imagen y embeddings visuales con backend automatico.
- `models/style_finder_llm_service.py`: Servicio de analisis de moda sobre modelos de vision en `Ollama`.
- `orchestration/nutrition_coach_asset_orchestration.py`: Generacion de platos de ejemplo para la app.
- `orchestration/nutrition_coach_dataset_orchestration.py`: Construccion del dataset nutricional con embeddings.
- `orchestration/nutrition_coach_helpers.py`: Helpers de formateo y contexto nutricional.
- `orchestration/nutrition_coach_app_orchestration.py`: Orquestacion principal de la app Flask.
- `orchestration/nutrition_coach_lab_runner.py`: Runner de consola para el flujo Nutrition Coach.
- `orchestration/style_finder_asset_orchestration.py`: Generacion de imagenes de ejemplo para la app.
- `orchestration/style_finder_dataset_orchestration.py`: Construccion del dataset enriquecido con embeddings.
- `orchestration/style_finder_helpers.py`: Helpers de retrieval alternativas y postproceso.
- `orchestration/style_finder_app_orchestration.py`: Orquestacion principal de la app Style Finder.
- `orchestration/style_finder_lab_runner.py`: Runner de consola para el flujo Style Finder.
- `ui/style_finder_ui.py`: Interfaz `Gradio` de la extension avanzada.
- `llava_vision_querying`: Variante real con `llava`.
- `llama3_2_vision_querying`: Variante real con `llama3.2-vision`.
- `qwen2_5vl_vision_querying`: Variante real con `qwen2.5vl:3b`.
- `nutrition_coach_flask_app`: Extension avanzada principal para nutricion.
- `nutrition_coach_llama3_2_vision_app`: Variante del Nutrition Coach con `llama3.2-vision`.
- `nutrition_coach_llava_app`: Variante del Nutrition Coach con `llava`.
- `nutrition_coach_qwen2_5vl_app`: Variante del Nutrition Coach con `qwen2.5vl:3b`.
- `style_finder_fashion_rag_app`: Extension avanzada principal.
- `style_finder_llama3_2_vision_app`: Variante del Style Finder con `llama3.2-vision`.
- `style_finder_llava_app`: Variante del Style Finder con `llava`.
- `style_finder_qwen2_5vl_app`: Variante del Style Finder con `qwen2.5vl:3b`.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias ya cubiertas por el repo: `numpy` `pandas` `pillow` `gradio` y `flask`.
3. Arrancar `Ollama`: `ollama serve`.
4. Modelo base recomendado: `ollama pull qwen2.5vl:3b`.
5. Modelos alternativos: `ollama pull llava` y `ollama pull llama3.2-vision`.
6. Backend visual opcional para parecerse mas al laboratorio original: `pip install torch torchvision`.
7. `Gradio` ya esta disponible para Style Finder y `Flask` para Nutrition Coach.

## Verificacion

1. Compilacion: `python -m compileall spikes\14-vision_multimodal`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_14_vision_multimodal.py`.
4. Variante `llava`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\llava_vision_querying\main.py`.
5. Variante `llama3.2-vision`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\llama3_2_vision_querying\main.py`.
6. Variante `qwen2.5vl`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\qwen2_5vl_vision_querying\main.py`.
7. Style Finder principal: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\style_finder_fashion_rag_app\main.py`.
8. Style Finder con `llama3.2-vision`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\style_finder_llama3_2_vision_app\main.py`.
9. Style Finder con `llava`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\style_finder_llava_app\main.py`.
10. Style Finder con `qwen2.5vl`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\style_finder_qwen2_5vl_app\main.py`.
11. Nutrition Coach principal: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_flask_app\main.py`.
12. Nutrition Coach con `llama3.2-vision`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_llama3_2_vision_app\main.py`.
13. Nutrition Coach con `llava`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_llava_app\main.py`.
14. Nutrition Coach con `qwen2.5vl`: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_qwen2_5vl_app\main.py`.
15. Tras validar compilacion y tests puedes lanzar la app Flask: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_flask_app\app.py`.

## Cobertura

1. `create_vision_message`: Estructura de texto e imagen para un modelo multimodal.
2. `generate_model_response`: Consulta basica sobre una imagen.
3. `generate_image_captions`: Captioning en lote para varias imagenes.
4. `generate_nutrition_response`: Analisis de una etiqueta nutricional.
5. `generate_fashion_response`: Analisis orientado a retail con items similares.
6. `find_closest_match`: Matching por similitud coseno sobre embeddings visuales ligeros.
7. `run_llava_example`: Ejemplo real con `llava`.
8. `run_llama32_vision_example`: Ejemplo real con `llama3.2-vision`.
9. `run_qwen25_vl_example`: Ejemplo real con `qwen2.5vl`.
10. `StyleFinderApp`: App avanzada con retrieval visual y analisis contextual.
11. `build_style_finder_interface`: UI `Gradio` para la extension de moda.
12. `run_style_finder_fashion_rag_app`: Runner de consola para probar el pipeline completo.
13. `create_nutrition_coach_app`: Fabrica Flask para el analisis nutricional.
14. `NutritionCoachVisionService`: Servicio multimodal real con contexto nutricional recuperado.
15. `run_nutrition_coach_lab`: Runner de consola para probar la extension nutricional.
