# --- DEPENDENCIAS ---
import re


def get_all_items_for_image(image_key, dataset):
    return dataset[dataset["Image Key"] == image_key]


def build_nutrition_reference_text(related_items) -> str:
    lines = []
    total_calories = int(related_items["Calories"].sum())

    for _, row in related_items.iterrows():
        lines.append(
            (
                f"- {row['Food Item']}: {row['Portion Size']}, {row['Calories']} calories, "
                f"Protein {row['Protein']}, Carbohydrates {row['Carbohydrates']}, Fats {row['Fats']}, "
                f"Vitamins {row['Vitamins']}, Minerals {row['Minerals']}. "
                f"Note: {row['Health Note']}"
            )
        )

    lines.append(f"- Total Calories: {total_calories}")
    return "\n".join(lines)


def build_identification_lines(related_items) -> str:
    return "\n".join(f"- {row['Food Item']}" for _, row in related_items.iterrows())


def build_calorie_breakdown_lines(related_items) -> str:
    return "\n".join(
        f"- {row['Food Item']}: {row['Portion Size']}, {row['Calories']} calories"
        for _, row in related_items.iterrows()
    )


def build_nutrient_breakdown_lines(related_items) -> str:
    return "\n".join(
        (
            f"- {row['Food Item']}: Protein {row['Protein']}, "
            f"Carbohydrates {row['Carbohydrates']}, Fats {row['Fats']}, "
            f"Vitamins {row['Vitamins']}, Minerals {row['Minerals']}."
        )
        for _, row in related_items.iterrows()
    )


def format_response(response_text: str) -> str:
    formatted = re.sub(r"\*\*(.*?)\*\*", r"<p><strong>\1</strong></p>", response_text)
    formatted = re.sub(r"(?m)^\s*-\s(.*)", r"<li>\1</li>", formatted)
    formatted = re.sub(
        r"(<li>.*?</li>)+",
        lambda match: f"<ul>{match.group(0)}</ul>",
        formatted,
        flags=re.DOTALL,
    )
    formatted = re.sub(r"\n+", "<br>", formatted)
    return formatted
