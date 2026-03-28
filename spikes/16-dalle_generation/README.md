# Practica 16 DALL-E Image Generation Lab

## Leyenda

1. DALL-E 2 generation: Genera una imagen desde un prompt con `dall-e-2`.
2. DALL-E 3 generation: Genera una imagen desde un prompt con `dall-e-3`.
3. Local image export: Guarda la imagen recibida desde la API en un archivo local.
4. Version comparison: Ejecuta la misma idea con dos versiones del modelo.
5. Adaptacion para terminal: Sustituye el display de notebook por salida a archivo y rutas locales.

## Adaptacion

Esta practica adapta la guia original de generacion de imagenes con `DALL-E` a una version ejecutable dentro del repositorio. Usa los modelos del material `dall-e-2` y `dall-e-3` y mantiene dos variantes reales separadas dentro del spike. Como la ejecucion depende de `OpenAI` la practica no usa un modelo inventado ni un proveedor distinto. Si falta la libreria o `OPENAI_API_KEY` el runner informa el requisito en lugar de fallar de forma opaca.

La practica se conserva por fidelidad al material original. Segun la documentacion oficial actual de `OpenAI` estos modelos son heredados y conviene entender esta practica como una guia historica y comparativa.

Esta practica absorbe la parte de la cheat sheet centrada en generacion visual. Aqui se cubren `DALL-E 2` `DALL-E 3` `b64_json` guardado local comparacion de versiones y diferencias practicas entre tamanos calidad salida a archivo y generacion multiple con `dall-e-2`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/dalle_image_generation_config.py`: Prompts tamanos y rutas de salida.
- `data/dalle_prompt_catalog.py`: Catalogo de prompts base y de ejercicios.
- `models/dalle_openai_gateway.py`: Cliente opcional de `OpenAI` para el endpoint de imagenes.
- `orchestration/dalle_generation_orchestration.py`: Construccion de requests generacion y guardado local.
- `orchestration/dalle_lab_runner.py`: Ejecucion guiada de la practica.
- `dall_e_2_generation`: Variante real centrada en `dall-e-2`.
- `dall_e_3_generation`: Variante real centrada en `dall-e-3`.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencia opcional para esta practica: `pip install -U openai`.
3. Exportar la clave: `OPENAI_API_KEY`.

## Verificacion

1. Compilacion: `python -m compileall spikes\16-dalle_generation`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\16-dalle_generation\main.py`.
3. Variante `dall-e-2`: `.\venv\Scripts\python.exe .\spikes\16-dalle_generation\dall_e_2_generation\main.py`.
4. Variante `dall-e-3`: `.\venv\Scripts\python.exe .\spikes\16-dalle_generation\dall_e_3_generation\main.py`.
5. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_16_dalle_generation.py`.

## Cobertura

1. `build_dalle_2_request`: Request de generacion para `dall-e-2`.
2. `build_custom_dalle_2_request`: Request configurable para tamano cantidad y formato de salida.
3. `build_dalle_2_gallery_request`: Plantilla para generacion multiple con `dall-e-2`.
4. `build_dalle_3_request`: Request de generacion para `dall-e-3`.
5. `build_custom_dalle_3_request`: Request configurable para tamano calidad y formato.
6. `generate_image_with_openai`: Llamada real a la API de imagenes.
7. `generate_image_batch_with_openai`: Generacion multiple y exportacion local en lote.
8. `save_generated_image`: Escritura local del resultado.
9. `save_generated_images`: Escritura local de varias respuestas.
10. `run_dalle_image_generation_lab`: Comparacion basica entre ambas versiones y ejemplos de requests ampliados.
