# =============================================================================================
# PRINCIPIOS DE ACTUACION DEL AGENTE
# =============================================================================================

1. El agente debe interpretar la intencion del usuario y no ejecutar instrucciones de forma literal sin analisis.
2. El agente debe analizar el contexto del proyecto antes de modificar archivos o ejecutar comandos.
3. El agente debe validar impacto tecnico en arquitectura seguridad estabilidad mantenibilidad y rendimiento.
4. Si una accion rompe el proyecto implica mala practica o aumenta riesgo tecnico la accion no se ejecuta.
5. Cuando una accion no se ejecuta el agente debe comunicar el motivo y proponer una alternativa segura.
6. El agente debe priorizar buenas practicas estandares de la industria y codigo moderno compatible con el stack actual.
7. El agente debe aplicar cambios minimos y enfocados para resolver la solicitud sin efectos colaterales.
8. Si faltan datos criticos el agente debe preguntar antes de aplicar cambios de alto riesgo.

# =============================================================================================
# ORDEN DE EJECUCION OBLIGATORIO
# =============================================================================================

9. Paso uno analizar la solicitud y definir objetivo tecnico verificable.
10. Paso dos revisar archivos y rutas afectadas antes de editar.
11. Paso tres aplicar cambios con criterio de minima superficie.
12. Paso cuatro validar resultado con test y compilacion.
13. Paso cinco actualizar documentacion si existen cambios funcionales o de arquitectura.
14. Paso seis comunicar resultado final con archivos modificados y validaciones ejecutadas.

# =============================================================================================
# REGLAS DE ESTILO PARA COMENTARIOS Y ESTRUCTURA
# =============================================================================================

15. Los comentarios deben mantener texto fluido y directo.
16. Todos los comentarios deben terminar con punto final.
17. No se debe escribir texto entre parentesis en comentarios.
18. No se deben usar comas ni punto y coma en comentarios.
19. Despues de los dos puntos debe existir un espacio y una mayuscula.
20. Los titulos de cabecera deben usar este formato exacto con una linea en blanco antes y despues del bloque y con longitud exacta de 95 caracteres por linea en todos los comentarios con `=====`.

# =============================================================================================
# REGLAS DE ARCHIVOS Y MANTENIMIENTO
# =============================================================================================

21. Cada archivo `.py` no vacio debe separar responsabilidades con el bloque `# --- DEPENDENCIAS ---`.
22. Debe existir un solo espacio de separacion entre bloques y nunca dos lineas en blanco seguidas.
23. No debe existir espacio en blanco al inicio de cualquier archivo y debe existir un solo salto final.
24. Nunca se deben modificar archivos de dependencias del lenguaje o del sistema operativo.
25. Todo archivo que no sea de codigo debe ordenarse alfabeticamente si no provoca errores.

# =============================================================================================
# REGLAS ESPECIFICAS PARA PRACTICAS EN SPIKES
# =============================================================================================

26. Toda practica nueva o modificada dentro de `spikes` debe revisarse contra el patron de estructura nombres comentarios y estilo usado por las practicas previas del repositorio.
27. Si una practica nueva es en realidad una extension natural de una practica ya existente no se debe crear un spike nuevo sin justificar primero la separacion tecnica y pedagogica.
28. Cada practica nueva o modificada debe quedar cubierta por tests ejecutables y esos tests deben correrse dentro del mismo turno.
29. No se debe cerrar una practica con errores de ejecucion advertencias evitables imports no resueltos o alertas de configuracion que hayan sido introducidos por el cambio.
30. Toda practica nueva o actualizada debe reflejarse en la documentacion correspondiente incluyendo `README.md` general `spikes/README.md` y el `README.md` propio de la practica cuando aplique.
31. Cuando una practica nueva o actualizada introduzca dependencias comandos de ejecucion conceptos o guias de uso se deben documentar de forma explicita en los README afectados.

# =============================================================================================
# VALIDACION ANTES DE EJECUTAR EN LOCAL
# =============================================================================================

32. Antes de arrancar el servidor web en local se deben ejecutar los test.
33. Antes de arrancar el servidor web en local se debe validar la compilacion de Python con `python -m compileall src`.
34. Si falla algun test o falla la compilacion el servidor no se arranca y se reporta el error.
35. Antes de arrancar el servidor web en local se debe actualizar el README cuando existan cambios funcionales o cambios de arquitectura.
