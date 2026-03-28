# --- DEPENDENCIAS ---


def answer_without_tools(query: str) -> str:
    lowered_query = query.lower()

    if "dataset" in lowered_query or ".csv" in lowered_query:
        return (
            "Sin acceso a herramientas puedo explicar conceptos de analisis pero no puedo "
            "inspeccionar archivos CSV locales ni calcular metricas reales sobre tus datos."
        )

    return (
        "Puedo razonar sobre analitica de datos a nivel general pero para trabajar con "
        "datasets reales necesito herramientas de carga analisis y evaluacion."
    )
