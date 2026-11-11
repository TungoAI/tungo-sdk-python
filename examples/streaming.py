"""Streaming a chat turn: events as they arrive, or the collected result."""

# [readme]
from tungoai import ChatStreamError, DecodeError, Tungo
from tungoai.types import ChatEventDone, ChatEventText, ChatEventTool

client = Tungo()
company_id = client.companies.list().data[0].id

# Events as they arrive. Leaving the "with" block closes the connection.
with client.chat.create_stream(company_id, message="How much VAT is due this quarter?") as stream:
    print("dialog", stream.dialog_id, "turn", stream.turn_no)
    for event in stream:
        if isinstance(event, ChatEventText):
            print(event.delta, end="", flush=True)
        elif isinstance(event, ChatEventTool):
            print(f"\n[{event.name}: {event.status}]")
        elif isinstance(event, ChatEventDone):
            print("\nstop reason:", event.stop_reason)

# Or let the SDK collect the turn. An "error" event of the turn is raised as ChatStreamError,
# and a stream that was cut before its "done" event as DecodeError: never a half answer.
try:
    result = client.chat.create_stream(company_id, message="And for the year?").get_final_result()
    print(result.text, result.stop_reason, result.cost_tiyn)
except ChatStreamError as error:
    print(error.type, error.code, error.message, error.request_id)
except DecodeError as error:
    print("the stream was cut:", error.result.text if error.result else "")

client.close()
# [/readme]
