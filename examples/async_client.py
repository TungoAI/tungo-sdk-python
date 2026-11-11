"""The asynchronous client has the same resources, helpers, pagination and streaming."""

# [readme]
import asyncio

from tungoai import AsyncTungo
from tungoai.types import ChatEventText


async def main() -> None:
    async with AsyncTungo() as client:
        companies = await client.companies.list()
        company_id = companies.data[0].id

        proposals = await client.proposals.list(company_id, limit=50)
        async for proposal in proposals:  # requests the following pages as needed
            print(proposal.id, proposal.title)

        async with await client.chat.create_stream(company_id, message="What is new today?") as stream:
            async for event in stream:
                if isinstance(event, ChatEventText):
                    print(event.delta, end="")


asyncio.run(main())
# [/readme]
