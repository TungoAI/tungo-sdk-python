# tungo-sdk — Официальный Python SDK для Tungo AI

Официальный Python SDK (0 внешних зависимостей, Python 3.10+) для **Tungo Platform API**:
- **Новичкам:** `client.ask()`, `client.stream_chat()`, `client.send_hook()`, `client.run_scenario_and_wait()`, `client.verify_webhook()`, авто-пагинаторы `*_all()` и `TungoMoney`.
- **Профи:** 100% покрытие всех 13 ресурсов и 82 методов API, строгие `TypedDict`-типы, авто-повторы с `Idempotency-Key` и `Retry-After`, иерархия исключений `TungoApiError`.

## Установка

```bash
pip install tungo-sdk
```

## Быстрый старт

```python
from tungo import TungoClient, TungoMoney

client = TungoClient(api_key="tg_...")

# 1. Задать вопрос ИИ-бухгалтеру
reply = client.ask("co_01h455vb4pex5vsknk084sn02q", "Какой НДС у последней реализации?")
print(reply["answer"], TungoMoney.format_tiyn(reply["usage"]["cost_tiyn"]))

# 2. Авто-пагинация по всем предложениям
for proposal in client.proposals.list_all("co_01h455vb4pex5vsknk084sn02q", query={"status": "awaiting_approval"}):
    print(proposal["id"], proposal["summary"])
```

## Все ресурсы и методы SDK

<!-- sdkgen:methods -->
Автоматически сгенерировано из OpenAPI-контракта Tungo Platform API: **13 ресурсов, 82 метода, 22 вебхука**.

| Ресурс | Описание | Методы |
| --- | --- | --- |
| `workspaces` | Организации (workspace), доступные ключу API | `list` |
| `companies` | Компании организации и их карточки | `list` · `get` |
| `platform` | Баланс платформы, книга движений, отчёты о расходе, лимиты, аудит и тарифы моделей | `list_usage_rates` · `get_account` · `get_audit` · `get_ledger` · `list_limits` · `list_requests` · `get_usage` |
| `api_keys` | Сведения о текущем ключе API и статистика его расхода | `get_current` · `get_current_usage` · `get_usage` |
| `webhooks` | Исходящие вебхуки организации (Svix): адреса, каталог событий, доставки и проверка подписи | `list_endpoints` · `create_endpoint` · `get_endpoint` · `update_endpoint` · `delete_endpoint` · `list_endpoint_attempts` · `rotate_endpoint_secret` · `test_endpoint` · `list_event_types` · `list_messages` · `list_message_attempts` · `resend_message` · `get_usage` |
| `chat` | Диалоги с ИИ-бухгалтером: вопросы, потоковый чат (SSE), подсчёт токенов и история | `list` · `create` · `count_tokens` · `get` · `update` · `delete` · `answer` · `list_events` · `stop` |
| `proposals` | Предложения документов ИИ-бухгалтера: просмотр, одобрение записи в 1С и отклонение | `list` · `approve_batch` · `get` · `approve` · `reject` |
| `feed` | Лента событий и предложений компании (страницы и живой поток SSE) | `get` · `list_events` |
| `batches` | Пачки обработки банковских выписок, входящих ЭСФ и DirectBank | `list` · `create_bank_statement` · `create_esf_purchases` · `get` · `list_events` · `stop` · `get_summary` · `list_statements` · `poll_directbank` |
| `esf` | Входящие и исходящие электронные счета-фактуры (ИС ЭСФ) | `get_incoming` · `get_outgoing` |
| `forms` | Налоговые формы (ФНО 100.00 и др.): сборка, проверка ИСНА и разрывы данных | `list` · `build` · `list_data_gaps` · `get_isna` · `list_notes` |
| `onec` | Состояние подключения компании к базе 1С | `get_status` |
| `automations` | Автоматизации компании: входящие хуки, сценарии, цепочки шагов, запуски и уровень автономности ИИ | `post_hook` · `list_hooks` · `create_hook` · `get_hook` · `update_hook` · `delete_hook` · `rotate_hook` · `test_hook` · `list_runs` · `get_run` · `cancel_run` · `retry_run` · `list_scenarios` · `create_scenario` · `get_scenario` · `put_scenario` · `update_scenario` · `delete_scenario` · `run_scenario` · `get_state` · `put_state` · `get_autonomy` · `put_autonomy` |
<!-- /sdkgen:methods -->
