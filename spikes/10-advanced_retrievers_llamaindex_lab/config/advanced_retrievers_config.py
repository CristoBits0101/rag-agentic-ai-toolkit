# --- DEPENDENCIAS ---
# 1. Path: Para resolver la raiz del spike.
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_QUERY = "What is machine learning?"
TECHNICAL_QUERY = "neural networks deep learning"
LEARNING_TYPES_QUERY = "different types of learning"
ADVANCED_QUERY = "How do neural networks work in deep learning?"
APPLICATIONS_QUERY = "What are the applications of AI systems?"
COMPREHENSIVE_QUERY = "What are the main approaches to machine learning?"
SPECIFIC_QUERY = "supervised learning techniques"
SIMILARITY_TOP_K = 3
AUTO_MERGING_TOP_K = 6
QUERY_FUSION_TOP_K = 3
QUERY_FUSION_NUM_QUERIES = 3
HYBRID_TOP_K = 4
HIERARCHICAL_CHUNK_SIZES = [420, 180, 90]
HIERARCHICAL_CHUNK_OVERLAP = 20
