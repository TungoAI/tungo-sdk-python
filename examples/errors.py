"""Typed errors and their fields."""

# [readme]
import tungoai
from tungoai import Tungo

client = Tungo()
try:
    client.companies.get("co_missing")
except tungoai.NotFoundError as error:
    print(error.status, error.type, error.code, error.message, error.request_id)
except tungoai.InvalidRequestError as error:
    for item in error.fields:
        print(item.path, item.code, item.message)
except tungoai.LimitError as error:
    print("retry after", error.retry_after, "s; the limit resets at", error.extra.get("resets_at"))
except tungoai.APIError as error:  # any other error response
    print(error.status, error.headers.get("x-request-id"), error.body)
except tungoai.APITimeoutError:
    print("the request timed out")
except tungoai.APIConnectionError as error:
    print("network problem:", error.__cause__)
except tungoai.DecodeError as error:
    print("unexpected response body:", error.body)
except tungoai.ConfigError as error:  # raised before any request, e.g. no API key
    print(error)
finally:
    client.close()
# [/readme]
