# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = SPIKE_ROOT / "data" / "student-mat.csv"
ARTIFACTS_DIR = SPIKE_ROOT / "artifacts"

OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

LAB_INTRODUCTION = (
    "Practica 22 adapta el lab de visualizacion conversacional con DataFrame agents "
    "usando ChatOllama real y create_pandas_dataframe_agent."
)

DATASET_DESCRIPTION = (
    "Student Alcohol Consumption dataset for mathematics students in Portugal. "
    "Use the dataframe called df and answer from data. "
    "When a chart is requested always save the figure to the exact path provided by the user. "
    "Do not call plt.show(). "
    "Return a concise explanation after running the code."
)

ROW_COUNT_QUERY = "How many rows of data are in this file?"
AGE_FILTER_QUERY = "Give me all the data where student's age is over 18 years old."

VISUALIZATION_QUERIES = [
    {
        "slug": "gender_count_bar",
        "title": "Gender Count Bar Chart",
        "query": "Generate a bar chart to plot the gender count.",
    },
    {
        "slug": "walc_gender_pie",
        "title": "Weekend Alcohol by Gender",
        "query": "Generate a pie chart to display average value of Walc for each Gender.",
    },
    {
        "slug": "freetime_vs_g3_boxplot",
        "title": "Free Time and Final Grade",
        "query": (
            "Create box plots to analyze the relationship between 'freetime' and 'G3' "
            "across different levels of free time."
        ),
    },
    {
        "slug": "absences_vs_g3_scatter",
        "title": "Absences and Academic Performance",
        "query": "Generate a scatter plot to explore the relationship between absences and G3.",
    },
]

EXERCISE_QUERIES = [
    {
        "slug": "parental_education_vs_grades",
        "title": "Parental Education and Grades Heatmap",
        "query": (
            "Create a heatmap of average G3 grouped by Medu and Fedu "
            "to analyze parental education level and grades."
        ),
    },
    {
        "slug": "internet_access_vs_grades",
        "title": "Internet Access and Grades",
        "query": (
            "Create box plots to compare G3 for students with and without internet access at home."
        ),
    },
]
