"""Downloading a file: a proposal exported as PDF."""

# [readme]
from pathlib import Path

from tungoai import Tungo

client = Tungo()
company_id = client.companies.list().data[0].id
proposal_id = client.proposals.list(company_id).data[0].id

file = client.proposals.export(company_id, proposal_id, format="pdf")
# The name comes from the server: only its last part is used as a path.
path = Path(Path(file.filename or "").name or "proposal.pdf")
path.write_bytes(file.content)
print(f"saved {path}: {len(file.content)} bytes, {file.content_type}, request id {file.request_id}")

client.close()
# [/readme]
