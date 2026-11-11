"""Cursor pagination: one page at a time, or every item lazily."""

# [readme]
from tungoai import Tungo

client = Tungo()
company_id = client.companies.list().data[0].id

# One page: the items, the cursor and the whole typed response.
page = client.proposals.list(company_id, status="awaiting_approval", limit=50)
print(len(page.data), page.next_cursor, page.body.total)
if page.has_next_page():
    page = page.get_next_page()  # same filters, next cursor

# Every item: iterating a page requests the following pages only when they are needed.
for proposal in client.proposals.list(company_id, status="awaiting_approval", limit=50):
    print(proposal.id, proposal.title, proposal.total.formatted)
    if proposal.blocker_count > 0:
        break  # no further page is requested

client.close()
# [/readme]
