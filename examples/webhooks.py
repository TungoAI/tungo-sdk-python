"""Verifying a webhook delivery and sending an event to an incoming hook."""

# [readme]
from collections.abc import Mapping

import tungoai
from tungoai import Tungo, WebhookVerificationError
from tungoai.types import WebhookEventProposalWritten

client = Tungo()  # the webhook secret comes from TUNGO_WEBHOOK_SECRET, or pass webhook_secret=...


def handle_webhook(raw_body: bytes, headers: Mapping[str, str]) -> int:
    """Call it from your HTTP handler with the raw request body and the request headers.

    Returns the HTTP status to answer with.
    """
    try:
        event = client.verify_webhook(raw_body, headers)
    except WebhookVerificationError as error:
        print("rejected:", error.reason)
        return 400
    if isinstance(event, WebhookEventProposalWritten):
        print("written to 1C:", event.data.proposal_id)
    return 204


# Send an event to an incoming hook. With a secret the exact bytes sent are signed (X-Signature).
accepted = client.send_hook(
    "th_example",
    {"id": "order_1532", "amount_tiyn": 4_500_000},
    secret="hksec_example",
    event_id="order_1532",
)
print(accepted.to_dict())

# Check a hook signature yourself (for example in a test double of the hook endpoint).
body = b'{"id":"order_1532"}'
assert tungoai.verify_hook_signature(body, tungoai.hook_signature_header(body, "hksec_example"), "hksec_example")
# [/readme]

# The rest only makes the example runnable on its own: it signs a sample delivery the way Tungo
# signs one and hands it to the handler above.
import base64
import hashlib
import hmac
import json
import time

secret = "whsec_" + base64.b64encode(b"example-secret-key").decode()
raw_body = json.dumps(
    {
        "id": "evt_1",
        "type": "proposal.written",
        "created_at": "2026-11-09T15:00:00.000Z",
        "workspace_id": "ws_1",
        "company_id": "co_1",
        "data": {"proposal_id": "P-000042", "kind": "payment_order"},
    }
).encode()
timestamp = str(int(time.time()))
digest = hmac.new(base64.b64decode(secret[6:]), b"msg_1." + timestamp.encode() + b"." + raw_body, hashlib.sha256)
request_headers = {
    "webhook-id": "msg_1",
    "webhook-timestamp": timestamp,
    "webhook-signature": "v1," + base64.b64encode(digest.digest()).decode(),
}
pool_owner = client
client = pool_owner.with_options(webhook_secret=secret)  # the handler reads the module-level client
assert handle_webhook(raw_body, request_headers) == 204
assert handle_webhook(raw_body + b" ", request_headers) == 400
pool_owner.close()
