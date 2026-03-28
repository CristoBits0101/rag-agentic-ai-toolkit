# --- DEPENDENCIAS ---
SAMPLE_DOCUMENTS = [
    {
        "title": "Machine Learning Foundations",
        "topic": "ml_basics",
        "text": (
            "Machine learning is a branch of artificial intelligence that learns "
            "patterns from data. Machine learning systems support classification "
            "regression recommendation and forecasting tasks."
        ),
    },
    {
        "title": "Deep Learning and Neural Networks",
        "topic": "deep_learning",
        "text": (
            "Deep learning uses layered neural networks to learn rich "
            "representations from data. Forward passes backpropagation and "
            "gradient based updates allow neural networks to model complex "
            "patterns at scale."
        ),
    },
    {
        "title": "Natural Language Processing",
        "topic": "nlp",
        "text": (
            "Natural language processing helps computers understand search "
            "translate summarize and generate text. NLP systems power chatbots "
            "assistants document understanding and enterprise search."
        ),
    },
    {
        "title": "Computer Vision",
        "topic": "computer_vision",
        "text": (
            "Computer vision enables image classification object detection "
            "medical imaging analysis and video understanding. Vision models "
            "extract visual features from scenes pixels and frames."
        ),
    },
    {
        "title": "Reinforcement Learning",
        "topic": "reinforcement_learning",
        "text": (
            "Reinforcement learning trains agents with rewards penalties "
            "policies and sequential decisions. It is useful for robotics game "
            "playing and control problems."
        ),
    },
    {
        "title": "Supervised Learning",
        "topic": "supervised_learning",
        "text": (
            "Supervised learning uses labeled examples to map inputs to "
            "outputs. Typical supervised learning tasks include spam detection "
            "credit scoring classification regression and prediction."
        ),
    },
    {
        "title": "Unsupervised Learning",
        "topic": "unsupervised_learning",
        "text": (
            "Unsupervised learning finds structure in unlabeled data through "
            "clustering dimensionality reduction topic discovery and anomaly "
            "detection."
        ),
    },
    {
        "title": "Transfer Learning",
        "topic": "transfer_learning",
        "text": (
            "Transfer learning reuses knowledge from pretrained models so new "
            "tasks need less labeled data. It accelerates adaptation in vision "
            "language and speech systems."
        ),
    },
    {
        "title": "Generative AI",
        "topic": "generative_ai",
        "text": (
            "Generative AI creates new text images code and synthetic media. "
            "Generative models support assistants content generation rapid "
            "prototyping and knowledge work."
        ),
    },
    {
        "title": "Large Language Models",
        "topic": "llm",
        "text": (
            "Large language models are trained on massive text corpora to "
            "perform reasoning summarization question answering and code "
            "generation. They are a major part of modern generative AI."
        ),
    },
    {
        "title": "Hybrid Retrieval",
        "topic": "hybrid_retrieval",
        "text": (
            "Hybrid retrieval combines semantic vector search with keyword "
            "ranking such as BM25. It improves recall when users mix exact "
            "terms with broad conceptual questions."
        ),
    },
]

LONG_FORM_DOCUMENTS = [
    {
        "title": "Learning Paradigms Guide",
        "topic": "learning_paradigms",
        "text": (
            "Learning Paradigms Guide\n"
            "Supervised learning uses labeled examples so models can predict a "
            "known target. Teams use supervised learning for classification "
            "regression and risk prediction when the desired answer is already "
            "known.\n"
            "Unsupervised learning explores unlabeled data. Analysts apply "
            "clustering dimensionality reduction and anomaly detection to find "
            "structure that is not obvious from manual review.\n"
            "Reinforcement learning focuses on agents rewards and sequential "
            "decisions. It is common in robotics scheduling and control where a "
            "policy improves through repeated interaction.\n"
            "Transfer learning speeds up delivery because a pretrained model can "
            "be adapted to a new domain with less labeled data and less compute."
        ),
    },
    {
        "title": "Model Architectures Guide",
        "topic": "model_architectures",
        "text": (
            "Model Architectures Guide\n"
            "Deep learning uses neural networks with input layers hidden layers "
            "and output layers. Each layer transforms features into richer "
            "representations that help the model detect complex patterns.\n"
            "During training a neural network runs a forward pass and compares "
            "predictions with targets. Backpropagation sends the error backward "
            "through the network so gradient based optimization can update "
            "weights and improve performance.\n"
            "Activation functions make neural networks nonlinear and expressive. "
            "Regularization batching and monitoring reduce overfitting while "
            "maintaining stable training in deep learning systems.\n"
            "Production teams often combine neural networks with retrieval so "
            "answers remain grounded in current domain context."
        ),
    },
    {
        "title": "AI Applications Guide",
        "topic": "ai_applications",
        "text": (
            "AI Applications Guide\n"
            "Natural language processing supports search assistants document "
            "classification and translation. Computer vision supports inspection "
            "medical imaging and safety systems.\n"
            "Generative AI helps teams draft content generate code create design "
            "variants and assist customer support. Large language models power "
            "question answering summarization and workflow automation.\n"
            "Organizations often combine retrieval with generation so assistants "
            "can answer domain specific questions with precise supporting "
            "context.\n"
            "When projects move to production engineers balance quality latency "
            "cost and governance."
        ),
    },
]

RECURSIVE_TOPIC_DOCUMENTS = {
    "learning": [
        {
            "title": "Learning Topic Overview",
            "text": (
                "Machine learning includes supervised learning unsupervised "
                "learning reinforcement learning and transfer learning. Each "
                "approach solves a different type of problem and uses different "
                "signals from data."
            ),
        },
        {
            "title": "Deep Learning Topic Overview",
            "text": (
                "Deep learning is a specialized machine learning approach that "
                "uses neural networks with many layers. It excels when large "
                "datasets and complex patterns are involved."
            ),
        },
    ],
    "applications": [
        {
            "title": "AI Applications Overview",
            "text": (
                "AI applications include assistants translation search computer "
                "vision inspection recommendation systems and content generation. "
                "Business teams use AI to automate repetitive work and improve "
                "decision support."
            ),
        },
        {
            "title": "Enterprise AI Systems",
            "text": (
                "Enterprise AI systems combine natural language processing "
                "computer vision and generative AI. Retrieval pipelines give "
                "assistants grounded context for support knowledge management and "
                "analytics."
            ),
        },
    ],
}
