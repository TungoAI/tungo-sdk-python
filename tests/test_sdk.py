from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import pytest

from tungo import (
    TungoClient,
    TungoHooks,
    TungoMoney,
    TungoPaymentRequiredError,
    TungoWebhooks,
    parse_sse_text,
)

VECTORS = json.loads(
    (Path(__file__).resolve().parents[2] / "tungo-sdkgen" / "conformance" / "vectors.json").read_text("utf-8")
)


def test_webhook_verification() -> None:
    w = VECTORS["webhook_verification"]
    headers = {
        "webhook-id": w["msg_id"],
        "webhook-timestamp": str(w["timestamp"]),
        "webhook-signature": w["valid_signature"],
    }
    assert TungoWebhooks.verify_signature(w["body"], headers, w["secret"], 300, w["timestamp"] + 5) is True
    assert (
        TungoWebhooks.verify_signature(
            w["body"], {**headers, "webhook-signature": w["dual_signature"]}, w["secret"], 300, w["timestamp"] + 5
        )
        is True
    )
    assert TungoWebhooks.verify_signature(w["body"], headers, w["secret"], 300, w["timestamp"] + 600) is False
    assert (
        TungoWebhooks.verify_signature(
            w["body"], {**headers, "webhook-signature": w["bad_signature"]}, w["secret"], 300, w["timestamp"] + 5
        )
        is False
    )
    parsed = TungoWebhooks.verify_and_parse(w["body"], headers, w["secret"], 300, w["timestamp"])
    assert parsed["type"] == "proposal.written"


def test_incoming_hook_signing() -> None:
    h = VECTORS["incoming_hook"]
    assert TungoHooks.sign_payload(h["body"], h["secret"], prefix=False) == h["hex_signature"]
    assert TungoHooks.sign_payload(h["body"], h["secret"], prefix=True) == h["prefixed_signature"]


def test_money_conversion_and_formatting() -> None:
    for m in VECTORS["money"]:
        assert TungoMoney.to_tiyn(m["tenge"]) == m["tiyn"]
        assert TungoMoney.to_tenge(m["tiyn"]) == m["tenge"]
        assert TungoMoney.format_tiyn(m["tiyn"]) == m["formatted"]


def test_sse_parsing() -> None:
    events = parse_sse_text(VECTORS["sse"]["raw_stream"])
    assert len(events) == len(VECTORS["sse"]["events"])
    assert events[0].event == "text"
    assert events[2].event == "done"


def test_client_ask_pagination_retries_and_errors() -> None:
    calls = 0

    def fake_sender(method: str, url: str, headers: dict[str, str], payload: bytes | None) -> tuple[int, dict[str, str], bytes]:
        nonlocal calls
        calls += 1
        if url.endswith("/v1/companies/co_1/chat"):
            body = json.loads(payload.decode("utf-8")) if payload else {}
            assert body["stream"] is False
            return (
                200,
                {"x-ratelimit-limit": "60", "x-ratelimit-remaining": "58", "x-ratelimit-reset": "30"},
                json.dumps({"dialog_id": "dlg_1", "turn_no": 1, "answer": "Готово!"}).encode("utf-8"),
            )
        if "/v1/companies/co_1/proposals" in url:
            qs = parse_qs(urlparse(url).query)
            if "cursor" not in qs:
                return 200, {}, json.dumps({"data": [{"id": "P-1"}, {"id": "P-2"}], "next_cursor": "c2"}).encode("utf-8")
            return 200, {}, json.dumps({"data": [{"id": "P-3"}], "next_cursor": None}).encode("utf-8")
        if url.endswith("/v1/api-key"):
            if calls == 1:
                return 429, {"Retry-After": "0"}, VECTORS["errors"][1]["body"].encode("utf-8")
            return 200, {}, json.dumps({"id": "key_1"}).encode("utf-8")
        return 402, {}, VECTORS["errors"][0]["body"].encode("utf-8")

    client = TungoClient(api_key="tg_test", sender=fake_sender)
    assert client.api_keys.get_current()["id"] == "key_1"

    reply = client.ask("co_1", "Привет")
    assert reply["answer"] == "Готово!"
    assert client.last_rate_limit is not None and client.last_rate_limit.remaining == 58

    ids = [p["id"] for p in client.proposals.list_all("co_1")]
    assert ids == ["P-1", "P-2", "P-3"]

    with pytest.raises(TungoPaymentRequiredError) as exc_info:
        client.platform.get_account("ws_1")
    assert exc_info.value.error_code == "platform_balance_exhausted"
    assert exc_info.value.request_id == "req_01jbalance001"
