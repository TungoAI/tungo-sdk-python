"""Client options, per-request options and raw response access."""

# [readme]
import os

import httpx

from tungoai import Tungo

http_client = httpx.Client(limits=httpx.Limits(max_connections=10))  # proxies, mTLS, custom transports
client = Tungo(
    api_key=os.environ["TUNGO_API_KEY"],  # default: the TUNGO_API_KEY environment variable
    base_url=os.environ.get("TUNGO_BASE_URL"),  # default: TUNGO_BASE_URL, then https://api.tungo.kz
    webhook_secret=os.environ.get("TUNGO_WEBHOOK_SECRET"),  # default: TUNGO_WEBHOOK_SECRET
    timeout=30.0,  # seconds for a whole ordinary request; default 60
    long_running_timeout=900.0,  # seconds for a non-streaming chat turn; default 600
    max_retries=3,  # default 2
    default_headers={"X-App-Name": "billing"},
    http_client=http_client,
)
company_id = client.companies.list().data[0].id

# Options of one request.
company = client.companies.get(
    company_id,
    request_options={"timeout": 5.0, "max_retries": 0, "headers": {"X-Trace-Id": "trace-1"}},
)

# A copy of the client with other settings; it shares the connection pool.
patient = client.with_options(timeout=120.0)
print(patient.companies.get(company_id).name)

# Status, headers, request id and rate limit of a response.
response = client.companies.with_raw_response.get(company_id)
print(response.status_code, response.request_id, response.rate_limit.remaining)
print(response.parse().name)

client.close()
http_client.close()  # the SDK never closes a client it did not create
# [/readme]
