import pytest

from app import handle


def test_handle_returns_session_and_output():
    response = handle({"input": "Consulta sintética", "session_id": "session-a"})

    assert response == {
        "output": "Solicitud recibida: Consulta sintética",
        "session_id": "session-a",
        "status": "completed",
    }


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"input": "", "session_id": "session-a"},
        {"input": "texto", "session_id": ""},
        {"input": "texto"},
    ],
)
def test_handle_rejects_invalid_payload(payload):
    with pytest.raises(ValueError):
        handle(payload)
