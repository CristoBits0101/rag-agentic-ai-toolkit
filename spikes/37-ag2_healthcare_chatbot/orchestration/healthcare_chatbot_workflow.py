# --- DEPENDENCIAS ---
from config.healthcare_chatbot_config import DEFAULT_LLM_CONFIG
from config.healthcare_chatbot_config import DEFAULT_MENTAL_HEALTH_PROMPT
from config.healthcare_chatbot_config import DEFAULT_SYMPTOMS
from models.ag2_compat import ConversableAgent
from models.ag2_compat import GroupChat
from models.ag2_compat import GroupChatManager


def build_healthcare_agents():
    patient_agent = ConversableAgent(name="patient", system_message="You describe symptoms and ask for medical help.", llm_config=DEFAULT_LLM_CONFIG)
    diagnosis_agent = ConversableAgent(name="diagnosis", system_message="You analyze symptoms and provide a possible diagnosis.", llm_config=DEFAULT_LLM_CONFIG)
    pharmacy_agent = ConversableAgent(name="pharmacy", system_message="You recommend medications based on diagnosis.", llm_config=DEFAULT_LLM_CONFIG)
    consultation_agent = ConversableAgent(
        name="consultation",
        system_message="You determine if a doctor visit is required and end with CONSULTATION_COMPLETE.",
        llm_config=DEFAULT_LLM_CONFIG,
        is_termination_msg=lambda x: "CONSULTATION_COMPLETE" in (x.get("content", "") or ""),
    )
    return patient_agent, diagnosis_agent, pharmacy_agent, consultation_agent


def run_automed_consultation(symptoms: str = DEFAULT_SYMPTOMS):
    patient_agent, diagnosis_agent, pharmacy_agent, consultation_agent = build_healthcare_agents()
    groupchat = GroupChat(agents=[diagnosis_agent, pharmacy_agent, consultation_agent], messages=[], max_round=5, speaker_selection_method="round_robin")
    manager = GroupChatManager(name="manager", groupchat=groupchat)
    response = patient_agent.initiate_chat(manager, message=f"I am feeling {symptoms}. Can you help?", max_turns=5, summary_method="reflection_with_llm")
    return response


def run_mental_health_chatbot(user_message: str = DEFAULT_MENTAL_HEALTH_PROMPT):
    patient_agent = ConversableAgent(name="patient", system_message="You describe your mood and emotional state.", llm_config=DEFAULT_LLM_CONFIG)
    emotion_agent = ConversableAgent(name="emotion_analysis", system_message="You identify emotions based on the user input.", llm_config=DEFAULT_LLM_CONFIG)
    therapy_agent = ConversableAgent(name="therapy_recommendation", system_message="You provide relaxation techniques and coping strategies.", llm_config=DEFAULT_LLM_CONFIG)
    groupchat = GroupChat(agents=[emotion_agent, therapy_agent], messages=[], max_round=3, speaker_selection_method="round_robin")
    manager = GroupChatManager(name="mental_health_manager", groupchat=groupchat)
    return patient_agent.initiate_chat(manager, message=user_message, max_turns=3, summary_method="reflection_with_llm")


def run_healthcare_demo() -> None:
    consultation = run_automed_consultation()
    print("=== AutoMed Consultation ===")
    print(consultation.summary)
    print("\n=== Mental Health Exercise ===")
    print(run_mental_health_chatbot().summary)