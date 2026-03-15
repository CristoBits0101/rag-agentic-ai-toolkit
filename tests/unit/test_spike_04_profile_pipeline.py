# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "04-linkedin_icebreaker_bot_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from pipeline.icebreaker_profile_pipeline import format_profile_text
from pipeline.icebreaker_profile_pipeline import list_profile_keys
from pipeline.icebreaker_profile_pipeline import load_profile_data


def test_list_profile_keys_returns_sorted_mock_profiles():
    profile_keys = list_profile_keys()

    assert profile_keys == sorted(profile_keys)
    assert "ana_martinez" in profile_keys
    assert "diego_santos" in profile_keys


def test_load_profile_data_reads_mock_profile():
    profile_data = load_profile_data("ana_martinez")

    assert profile_data["full_name"] == "Ana Martinez"
    assert profile_data["headline"] == "Principal AI Engineer at Nova Retail"


def test_format_profile_text_flattens_nested_sections():
    profile_text = format_profile_text(
        {
            "full_name": "Ana Martinez",
            "experience": [
                {
                    "company": "Nova Retail",
                    "title": "Principal AI Engineer",
                }
            ],
        }
    )

    assert "full_name: Ana Martinez" in profile_text
    assert "experience.1.company: Nova Retail" in profile_text
    assert "experience.1.title: Principal AI Engineer" in profile_text
