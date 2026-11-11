"""Retries, timeouts and idempotency keys."""

# [readme]
from tungoai import Tungo

client = Tungo(max_retries=5, timeout=20.0)  # for every request of this client
company_id = client.companies.list().data[0].id
proposal_id = client.proposals.list(company_id).data[0].id

# For one request. approve declares Idempotency-Key, so the SDK would generate a key anyway;
# pass your own to make a repeated call from your side safe too.
approved = client.proposals.approve(
    company_id,
    proposal_id,
    note="Checked against the contract",
    request_options={"idempotency_key": f"approve-{proposal_id}", "max_retries": 1, "timeout": 10.0},
)
print(approved.to_dict())

# A POST that does not declare the header is never retried unless you give it a key.
client.proposals.reject(
    company_id, proposal_id, reason="Duplicate", request_options={"idempotency_key": f"reject-{proposal_id}"}
)

client.close()
# [/readme]
