# --- DEPENDENCIAS ---
import logging
import re

from config.style_finder_fashion_config import STYLE_FINDER_MAX_TOTAL_ALTERNATIVES
from config.style_finder_fashion_config import STYLE_FINDER_TOP_ALTERNATIVES

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_all_items_for_image(image_key, dataset):
    related_items = dataset[dataset["Image Key"] == image_key]
    logger.info("Found %d items for image key %s", len(related_items), image_key)
    return related_items


def build_alternatives_map(
    related_items,
    dataset,
    per_item_limit: int = STYLE_FINDER_TOP_ALTERNATIVES,
) -> dict:
    alternatives = {}

    for _, row in related_items.iterrows():
        matches = dataset[
            (dataset["Category"] == row["Category"])
            & (dataset["Item Name"] != row["Item Name"])
        ].sort_values("Price")
        alternatives[row["Item Name"]] = [
            {
                "title": match["Item Name"],
                "price": f"${match['Price']:.2f}",
                "source": match["Source"],
                "link": match["Link"],
            }
            for _, match in matches.head(per_item_limit).iterrows()
        ]

    return alternatives


def format_alternatives_response(user_response, alternatives, similarity_score, threshold=0.8):
    if not user_response or any(
        phrase in user_response
        for phrase in (
            "I'm not able to provide",
            "I cannot",
            "I apologize, but",
            "I don't feel comfortable",
            "Error generating response",
        )
    ):
        user_response = "## Fashion Analysis Results\n\nHere are the items detected in your image:"

    if similarity_score >= threshold:
        enhanced_response = (
            user_response + "\n\n## Similar Items Found\n\nHere are some similar items we found:\n"
        )
    else:
        enhanced_response = (
            user_response
            + "\n\n## Similar Items Found\n\nHere are some visually similar items:\n"
        )

    items_added = 0

    for item_name, alternatives_for_item in alternatives.items():
        enhanced_response += f"\n### {item_name}\n"
        if alternatives_for_item:
            for alternative in alternatives_for_item:
                if items_added >= STYLE_FINDER_MAX_TOTAL_ALTERNATIVES:
                    break

                enhanced_response += (
                    f"- {alternative['title']} for {alternative['price']} from "
                    f"{alternative['source']} ([Buy it here]({alternative['link']}))\n"
                )
                items_added += 1
        else:
            enhanced_response += "- No alternatives found.\n"

    return enhanced_response


def process_response(response: str) -> str:
    if not response:
        return "# Fashion Analysis\n\nNo detailed analysis was generated."

    processed = response.replace("$", "\\$")
    processed = processed.replace("ITEM DETAILS:", "## Item Details")
    processed = processed.replace("SIMILAR ITEMS:", "## Similar Items")
    processed = re.sub(r"^\* ", "- ", processed, flags=re.MULTILINE)

    if not processed.startswith("#"):
        processed = "# Fashion Analysis\n\n" + processed

    return processed
