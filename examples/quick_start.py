"""Quick start: list the companies and ask the AI accountant a question."""

# [readme]
from tungoai import Tungo

with Tungo() as client:  # reads TUNGO_API_KEY from the environment
    companies = client.companies.list()
    for company in companies.data:
        print(company.id, company.name)

    turn = client.ask(companies.data[0].id, "How much VAT is due this quarter?")
    print(turn.answer)
# [/readme]
