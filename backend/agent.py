import os
from pathlib import Path
from typing import Annotated, Any, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_vertexai import ChatVertexAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    session_id: str


class SessionData(TypedDict):
    messages: list[BaseMessage]
    document_content: str


sessions: dict[str, SessionData] = {}


def _get_session(session_id: str) -> SessionData:
    if session_id not in sessions:
        sessions[session_id] = {"messages": [], "document_content": ""}
    return sessions[session_id]


@tool
def update_document(content: str) -> str:
    """Update the draft document with the complete provided content."""
    return content


@tool
def save_document(filename: str = "document.txt") -> str:
    """Save the current draft document to a text file."""
    return filename


tools = [update_document, save_document]
model = None


def _get_model() -> Any:
    global model
    if model is not None:
        return model

    project = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not project:
        raise RuntimeError("GCP_PROJECT_ID is required. Add it to your environment or .env file.")

    chat_model = ChatVertexAI(model=model_name, project=project, location=location)
    model = chat_model.bind_tools(tools)
    return model


def _clean_messages(messages: list[BaseMessage]) -> list[BaseMessage]:
    cleaned = []
    for message in messages:
        if hasattr(message, "content") and message.content == "":
            message.content = "Tool call requested."
        cleaned.append(message)
    return cleaned


def _agent_node(state: AgentState) -> dict[str, list[AIMessage]]:
    session = _get_session(state["session_id"])
    document_content = session["document_content"] or "No document content yet."

    system_prompt = SystemMessage(
        content=f"""
You are Drafter, a helpful document drafting assistant.

- Help the user write, revise, and polish documents.
- If the user asks to update, rewrite, edit, or replace the document, call update_document with the complete updated document content.
- If the user asks to save the document, call save_document. Use document.txt when no filename is provided.
- After edits, briefly summarize what changed.

Current document content:
{document_content}
""".strip()
    )

    response = _get_model().invoke(_clean_messages([system_prompt] + list(state["messages"])))

    if response.content == "":
        response.content = "I will use a tool to complete this request."

    return {"messages": [response]}


def _safe_filename(filename: str) -> str:
    safe_name = Path(filename or "document.txt").name
    if not safe_name.endswith(".txt"):
        safe_name = f"{safe_name}.txt"
    return safe_name


def save_current_document(session_id: str, filename: str) -> dict[str, str]:
    session = _get_session(session_id)
    safe_name = _safe_filename(filename)
    output_dir = Path(__file__).resolve().parent / "saved_documents"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / safe_name
    output_path.write_text(session["document_content"], encoding="utf-8")

    return {
        "message": f"Document saved successfully as {safe_name}.",
        "filename": safe_name,
        "path": str(output_path),
    }


def _tools_node(state: AgentState) -> dict[str, list[ToolMessage]]:
    session = _get_session(state["session_id"])
    last_message = state["messages"][-1]
    tool_messages = []

    for tool_call in getattr(last_message, "tool_calls", []):
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})

        if tool_name == "update_document":
            content = tool_args.get("content", "")
            session["document_content"] = content
            result = "Document updated successfully."
        elif tool_name == "save_document":
            result_data = save_current_document(state["session_id"], tool_args.get("filename", "document.txt"))
            result = result_data["message"]
        else:
            result = f"Unknown tool: {tool_name}"

        tool_messages.append(
            ToolMessage(
                content=result,
                name=tool_name,
                tool_call_id=tool_call["id"],
            )
        )

    return {"messages": tool_messages}


def _route_after_agent(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


def _route_after_tools(_: AgentState) -> str:
    return "agent"


graph = StateGraph(AgentState)
graph.add_node("agent", _agent_node)
graph.add_node("tools", _tools_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", _route_after_agent, {"tools": "tools", END: END})
graph.add_conditional_edges("tools", _route_after_tools, {"agent": "agent"})
app = graph.compile()


def get_document(session_id: str) -> str:
    return _get_session(session_id)["document_content"]


def run_agent(user_message: str, session_id: str) -> dict[str, str | None]:
    session = _get_session(session_id)
    state: AgentState = {
        "messages": session["messages"] + [HumanMessage(content=user_message)],
        "session_id": session_id,
    }

    result = app.invoke(state)
    session["messages"] = list(result["messages"])

    ai_message = ""
    tool_used = None
    tool_result = None

    for message in reversed(session["messages"]):
        if isinstance(message, AIMessage) and message.content:
            ai_message = str(message.content)
            break

    for message in reversed(session["messages"]):
        if isinstance(message, ToolMessage):
            tool_used = message.name
            tool_result = str(message.content)
            break

    return {
        "ai_message": ai_message,
        "document_content": session["document_content"],
        "tool_used": tool_used,
        "tool_result": tool_result,
    }
