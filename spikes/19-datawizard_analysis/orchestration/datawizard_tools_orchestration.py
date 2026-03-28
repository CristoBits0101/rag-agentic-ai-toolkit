# --- DEPENDENCIAS ---
import io
from pathlib import Path
from typing import Any

import pandas as pd
from langchain_core.tools import BaseTool
from langchain_core.tools import tool
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

SPIKE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = SPIKE_ROOT / "data"
DATAFRAME_CACHE: dict[str, pd.DataFrame] = {}
SAFE_DATAFRAME_METHODS = {
    "corr",
    "describe",
    "head",
    "info",
    "tail",
}


def list_dataset_paths() -> list[Path]:
    return sorted(DATA_DIR.glob("*.csv"))


def resolve_dataset_path(file_name: str) -> Path:
    direct_path = Path(file_name)
    if direct_path.exists():
        return direct_path

    candidate = DATA_DIR / file_name
    if candidate.exists():
        return candidate

    for path in list_dataset_paths():
        if path.name == file_name:
            return path

    raise FileNotFoundError(f"Dataset '{file_name}' not found.")


def dataset_cache_key(file_name: str) -> str:
    return resolve_dataset_path(file_name).name


def load_dataset_frame(file_name: str) -> pd.DataFrame:
    cache_key = dataset_cache_key(file_name)
    if cache_key not in DATAFRAME_CACHE:
        DATAFRAME_CACHE[cache_key] = pd.read_csv(resolve_dataset_path(file_name))
    return DATAFRAME_CACHE[cache_key]


def infer_problem_type(target_series: pd.Series) -> str:
    unique_count = int(target_series.nunique(dropna=True))
    row_count = max(int(target_series.shape[0]), 1)

    if not pd.api.types.is_numeric_dtype(target_series):
        return "classification"

    if unique_count <= 10 and unique_count / row_count <= 0.4:
        return "classification"

    return "regression"


def build_dataset_summary(file_name: str) -> dict[str, Any]:
    dataframe = load_dataset_frame(file_name)
    target_column = dataframe.columns[-1]
    target_series = dataframe[target_column]
    return {
        "file_name": dataset_cache_key(file_name),
        "row_count": int(dataframe.shape[0]),
        "column_count": int(dataframe.shape[1]),
        "column_names": dataframe.columns.tolist(),
        "data_types": dataframe.dtypes.astype(str).to_dict(),
        "target_column": target_column,
        "target_unique_values": int(target_series.nunique(dropna=True)),
        "suggested_problem_type": infer_problem_type(target_series),
    }


def normalize_metric(value: float) -> float:
    return round(float(value), 4)


@tool
def list_csv_files() -> dict[str, Any]:
    """
    List the CSV datasets available in the local practice directory.

    Returns:
        A payload with the dataset file names and the total count.
    """
    files = [path.name for path in list_dataset_paths()]
    return {
        "files": files,
        "count": len(files),
    }


@tool
def preload_datasets(paths: list[str]) -> dict[str, Any]:
    """
    Load one or more CSV datasets into the shared in memory cache.

    Args:
        paths: Dataset file names or paths.

    Returns:
        A payload that separates loaded datasets from already cached datasets.
    """
    loaded: list[str] = []
    cached: list[str] = []

    for path in paths:
        cache_key = dataset_cache_key(path)
        if cache_key not in DATAFRAME_CACHE:
            DATAFRAME_CACHE[cache_key] = pd.read_csv(resolve_dataset_path(path))
            loaded.append(cache_key)
        else:
            cached.append(cache_key)

    return {
        "loaded": loaded,
        "cached": cached,
        "active": loaded + cached,
    }


@tool
def get_dataset_summaries(dataset_paths: list[str]) -> list[dict[str, Any]]:
    """
    Analyze one or more cached CSV datasets and return compact metadata summaries.

    Args:
        dataset_paths: Dataset file names or paths.

    Returns:
        A list of summary dictionaries with structure target column and suggested task type.
    """
    return [build_dataset_summary(path) for path in dataset_paths]


@tool
def call_dataframe_method(file_name: str, method: str) -> dict[str, Any]:
    """
    Execute a safe no argument DataFrame method and return the formatted output.

    Args:
        file_name: Dataset file name or path.
        method: One of head tail describe corr or info.

    Returns:
        A payload with the rendered method output or an error message.
    """
    if method not in SAFE_DATAFRAME_METHODS:
        return {
            "file_name": file_name,
            "method": method,
            "error": f"Method '{method}' is not allowed.",
        }

    dataframe = load_dataset_frame(file_name)
    if method == "info":
        buffer = io.StringIO()
        dataframe.info(buf=buffer)
        result_text = buffer.getvalue().strip()
    else:
        result = getattr(dataframe, method)()
        result_text = result.to_string()

    return {
        "file_name": dataset_cache_key(file_name),
        "method": method,
        "result": result_text,
    }


@tool
def evaluate_classification_dataset(file_name: str, target_column: str) -> dict[str, Any]:
    """
    Train and evaluate a classification model on a cached dataset.

    Args:
        file_name: Dataset file name or path.
        target_column: Column used as the classification target.

    Returns:
        A payload with the classification accuracy and evaluation metadata.
    """
    dataframe = load_dataset_frame(file_name)
    if target_column not in dataframe.columns:
        return {
            "file_name": dataset_cache_key(file_name),
            "error": f"Target column '{target_column}' not found.",
        }

    features = pd.get_dummies(dataframe.drop(columns=[target_column]), drop_first=False)
    target = dataframe[target_column]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=42,
        stratify=target,
    )
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    return {
        "file_name": dataset_cache_key(file_name),
        "target_column": target_column,
        "task_type": "classification",
        "accuracy": normalize_metric(accuracy),
        "train_rows": int(x_train.shape[0]),
        "test_rows": int(x_test.shape[0]),
    }


@tool
def evaluate_regression_dataset(file_name: str, target_column: str) -> dict[str, Any]:
    """
    Train and evaluate a regression model on a cached dataset.

    Args:
        file_name: Dataset file name or path.
        target_column: Column used as the regression target.

    Returns:
        A payload with regression metrics and evaluation metadata.
    """
    dataframe = load_dataset_frame(file_name)
    if target_column not in dataframe.columns:
        return {
            "file_name": dataset_cache_key(file_name),
            "error": f"Target column '{target_column}' not found.",
        }

    features = pd.get_dummies(dataframe.drop(columns=[target_column]), drop_first=False)
    target = dataframe[target_column]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=42,
    )
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    r2 = r2_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    return {
        "file_name": dataset_cache_key(file_name),
        "target_column": target_column,
        "task_type": "regression",
        "r2_score": normalize_metric(r2),
        "mean_squared_error": normalize_metric(mse),
        "train_rows": int(x_train.shape[0]),
        "test_rows": int(x_test.shape[0]),
    }


def build_datawizard_tools() -> list[BaseTool]:
    return [
        list_csv_files,
        preload_datasets,
        get_dataset_summaries,
        call_dataframe_method,
        evaluate_classification_dataset,
        evaluate_regression_dataset,
    ]


def describe_tool_schemas(tools: list[BaseTool] | None = None) -> list[dict[str, Any]]:
    selected_tools = tools or build_datawizard_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "args": tool.args,
        }
        for tool in selected_tools
    ]
