# --- DEPENDENCIAS ---
from langgraph.graph import END
from langgraph.graph import StateGraph

from config.langgraph_workflows_config import AUTH_MAX_ATTEMPTS
from config.langgraph_workflows_config import AUTH_VALID_PASSWORD
from config.langgraph_workflows_config import AUTH_VALID_USERNAME
from models.langgraph_workflows_entities import AuthWorkflowResult
from models.langgraph_workflows_state import AuthState


def input_node(state: AuthState) -> AuthState:
    credential_attempts = state.get("credential_attempts", [])
    attempt_index = state.get("attempt_index", 0)

    if credential_attempts and attempt_index < len(credential_attempts):
        current_attempt = credential_attempts[attempt_index]
        return {
            "username": current_attempt.get("username", "").strip(),
            "password": current_attempt.get("password", ""),
            "attempt_index": attempt_index + 1,
        }

    return {
        "username": state.get("username", "").strip(),
        "password": state.get("password", ""),
    }


def validate_credentials_node(
    state: AuthState,
    valid_username: str = AUTH_VALID_USERNAME,
    valid_password: str = AUTH_VALID_PASSWORD,
) -> AuthState:
    username = state.get("username", "")
    password = state.get("password", "")
    attempts = state.get("attempts", 0) + 1
    is_authenticated = username == valid_username and password == valid_password
    return {"is_authenticated": is_authenticated, "attempts": attempts}


def success_node(state: AuthState) -> AuthState:
    return {"output": "Authentication successful! Welcome."}


def failure_node(state: AuthState) -> AuthState:
    attempts = state.get("attempts", 0)
    max_attempts = state.get("max_attempts", AUTH_MAX_ATTEMPTS)
    remaining_attempts = max(max_attempts - attempts, 0)
    return {
        "output": (
            "Authentication failed. "
            f"{remaining_attempts} attempt(s) remaining before lockout."
        )
    }


def lockout_node(state: AuthState) -> AuthState:
    return {
        "output": f"Authentication failed after {state.get('attempts', 0)} attempt(s)."
    }


def auth_router(state: AuthState) -> str:
    if state.get("is_authenticated", False):
        return "success"

    credential_attempts = state.get("credential_attempts", [])
    max_attempts = state.get("max_attempts", AUTH_MAX_ATTEMPTS)
    has_more_attempts = state.get("attempt_index", 0) < len(credential_attempts)
    can_retry = has_more_attempts and state.get("attempts", 0) < max_attempts

    if can_retry:
        return "retry"

    return "lockout"


def build_auth_workflow(
    valid_username: str = AUTH_VALID_USERNAME,
    valid_password: str = AUTH_VALID_PASSWORD,
):
    workflow = StateGraph(AuthState)

    def validation_node(state: AuthState) -> AuthState:
        return validate_credentials_node(
            state,
            valid_username=valid_username,
            valid_password=valid_password,
        )

    workflow.add_node("InputNode", input_node)
    workflow.add_node("ValidateCredential", validation_node)
    workflow.add_node("Success", success_node)
    workflow.add_node("Failure", failure_node)
    workflow.add_node("Lockout", lockout_node)

    workflow.add_edge("InputNode", "ValidateCredential")
    workflow.add_conditional_edges(
        "ValidateCredential",
        auth_router,
        {
            "success": "Success",
            "retry": "Failure",
            "lockout": "Lockout",
        },
    )
    workflow.add_edge("Failure", "InputNode")
    workflow.add_edge("Success", END)
    workflow.add_edge("Lockout", END)
    workflow.set_entry_point("InputNode")
    return workflow.compile()


def invoke_auth_workflow(
    initial_state: AuthState,
    valid_username: str = AUTH_VALID_USERNAME,
    valid_password: str = AUTH_VALID_PASSWORD,
) -> AuthWorkflowResult:
    app = build_auth_workflow(valid_username=valid_username, valid_password=valid_password)
    result = app.invoke({"max_attempts": AUTH_MAX_ATTEMPTS, **initial_state})
    return AuthWorkflowResult(
        username=result.get("username", ""),
        is_authenticated=result.get("is_authenticated", False),
        output=result.get("output", ""),
        attempts=result.get("attempts", 0),
    )