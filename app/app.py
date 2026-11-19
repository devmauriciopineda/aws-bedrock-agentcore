from __future__ import annotations

from typing import Any

from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


def handle(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")

    text = payload.get("input")
    session_id = payload.get("session_id")

    if not isinstance(text, str) or not text.strip():
        raise ValueError("input must be a non-empty string")
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError("session_id must be a non-empty string")

    return {
        "output": f"Solicitud recibida: {text.strip()}",
        "session_id": session_id,
        "status": "completed",
    }


@app.entrypoint
def invoke(payload: dict[str, Any]) -> dict[str, Any]:
    return handle(payload)


if __name__ == "__main__":
    app.run()
