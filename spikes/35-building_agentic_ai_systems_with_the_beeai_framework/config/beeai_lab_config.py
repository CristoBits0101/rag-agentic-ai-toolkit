# --- DEPENDENCIAS ---
DEFAULT_TEXT_MODEL = "qwen2.5:7b"
DEFAULT_ANALYSIS_QUERY = (
    "Analyze the cybersecurity risks of quantum computing for financial institutions. "
    "What are the main threats timeline for concern and recommended preparation strategies?"
)
DEFAULT_TRAVEL_QUERY = (
    "I'm planning a 2 week cultural immersion trip to Japan covering Tokyo and Osaka. "
    "What should I know about landmarks weather and respectful language or cultural practices?"
)

WIKIPEDIA_SNIPPETS = {
    "quantum computing": (
        "Quantum computing threatens classical public key cryptography because sufficiently capable fault tolerant quantum computers "
        "could break RSA and elliptic curve schemes using Shor's algorithm."
    ),
    "financial institutions": (
        "Financial institutions depend on long lived encrypted data stores and complex third party integrations which increases the urgency of post quantum migration planning."
    ),
    "tokyo": (
        "Tokyo combines historical districts such as Asakusa and Meiji Shrine with dense modern neighborhoods and extensive rail connectivity."
    ),
    "osaka": (
        "Osaka is known for Osaka Castle merchant history and a lively food culture centered around districts like Dotonbori."
    ),
    "japanese etiquette": (
        "Japanese etiquette values politeness punctuality quiet public behavior and respectful greetings with a slight bow."
    ),
}

WEATHER_DATA = {
    "tokyo": "Tokyo is typically mild in spring and autumn humid in summer and cool but manageable in winter.",
    "osaka": "Osaka has similar seasonality to Tokyo with humid summers and generally mild shoulder seasons suitable for walking tours.",
    "japan": "Japan has strong seasonal variation so packing layers and checking regional rainfall matters for multi city trips.",
}

PROJECT_SCENARIOS = [
    {
        "project_name": "Smart Inventory Optimization",
        "business_problem": "Reduce inventory costs while maintaining 95 percent product availability.",
        "data_description": "Two years of sales data supplier lead times seasonal patterns and 500K records.",
        "timeline": "3 months development and 1 month testing.",
        "success_metrics": "15 percent cost reduction 95 percent availability and less than 2 percent forecast error.",
    },
    {
        "project_name": "Fraud Detection System",
        "business_problem": "Detect fraudulent transactions in real time with minimal false positives.",
        "data_description": "One million transaction records user behavior data and device fingerprints.",
        "timeline": "6 months development and 2 months validation.",
        "success_metrics": "95 percent fraud detection less than 1 percent false positives and less than 100ms response time.",
    },
]

CALCULATOR_QUERIES = [
    "What is 15 + 27?",
    "Calculate 144 / 12",
    "I need to know what 8 * 9 equals",
    "What is (10 + 5) * 3 - 7?",
]