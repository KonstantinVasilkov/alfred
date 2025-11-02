# Personal Finance Assistant — PRD (ReWork-style)

> A lean, living document to align on what we’re building, why it matters, and the principles that guide every decision.

---

## 1) Purpose & Vision

**Purpose:** make it effortless for anyone to capture day-to-day money flows and understand their real financial picture — without forms, friction, or bookkeeping jargon.

**Vision:** a conversational financial companion that accepts **text, voice, or photos** and turns them into structured transactions, categories, and insights. It should feel like chatting with a smart, discreet assistant rather than operating finance software.

**Change we want:** people develop good money habits because recording and seeing finances is finally easy, immediate, and trustworthy. Over time, the app becomes a single source of truth for personal and (later) household finances.

---

## 2) Product Philosophy & Principles

* **Conversation over chrome.** Input is free-form (text / voice / receipt photo). The system adapts to the user, not vice versa.
* **Start simple, earn complexity.** MVP first: transactions + categories + simple analytics. Add budgets, goals, family sharing later.
* **Modular by default.** Swappable providers for OCR, speech, and LLMs. Avoid lock-in; keep boundaries clean.
* **Privacy as posture, not a feature.** Build with minimization and clear user controls. Explain what we store and why.
* **Truth before advice.** First nail accurate capture and classification. Insights come after the ledger is reliable.
* **SQL-first clarity.** If a question can be answered with a straightforward SQL query, it belongs in “simple analytics.”
* **No promises, only shipping.** This PRD avoids roadmaps and due dates. We iterate weekly and improve continuously.
* **ReWork mindset.** Fewer preferences, more principles; fewer layers, more shipping; small, steady wins.

---

## 3) User Experience Concept

**Feel:** like messaging a friendly, competent finance assistant.

**Primary flows:**

* **Text:** “Spent 20 bucks on barber.” → creates a transaction with category “Personal care.”
* **Voice:** short memo, transcribed → same outcome as text.
* **Image:** snap/upload a receipt → MVP extracts **total** (later: line items).
* **Edit & recall:** “Update the dinner on Oct 5: friend paid me back $15.” → adjust the original transaction.
* **Glanceable insights:** quick replies to “How much this month on groceries?” or “Top 3 categories last week?”

**Onboarding ethos:** guided but optional.

* Users may set starting balances **or** track from zero.
* No balance “types” at launch (keep minimal); can extend later.
* Predefined category set (10–15). Custom categories are **premium**.

**Surfaces:**

* **Phase 1:** Telegram bot (conversational center of gravity).
* **Phase 2:** Mobile app (coexists with bot; richer viewing & insights).
* **Phase 3:** Web app (parity with mobile for analysis & management).

---

## 4) Core Functionality (MVP)

**Must-have**

* **Accounts (minimal):** user can create balance accounts without types; optional initial balance.
* **Transactions CRUD:** add/edit/delete income/expense transfers.
* **Multi-modal input:** text, voice (via cloud speech), image receipts (OCR total only).
* **Categorization:** auto-suggest into predefined categories; manual override.
* **Simple analytics (SQL-first):**

  * Spend per category per month/week.
  * Income vs expense over time.
  * Top merchants/categories.
* **Search & corrections:** natural language queries (“show coffee in September”).
* **Auth & identity:** basic authentication/authorization (Cognito TBD).
* **Trial & subscriptions:** freemium with trial for premium features.

**Out-of-MVP (but anticipated)**

* **Budgets** and **financial goals** (requires product design: goal as account vs rule-based).
* **Detailed receipt line-items** + smart classification.
* **Family/household sharing** (account-level sharing; privacy by account).
* **Custom categories** management (premium).
* **Advanced analytics & forecasting.**
* **Tax helper** (household taxation insights, later).

---

## 5) Architecture & Technical Overview (conceptual)

**Stack choices (guiding):**

* **Backend:** FastAPI (Python) + **PydanticAI** for agentic logic & tools, MCP server wrapper for backend tools.
* **Data:** PostgreSQL for core entities (users, accounts, transactions, categories, subscriptions).
* **RAG / context:** TBD; keep option for pgvector or an external vector DB. Start without RAG where possible.
* **LLMs:** modular “small” vs “main” LLM selection via adapter interfaces (provider-agnostic).
* **OCR & STT:** cloud providers (e.g., Google/AWS/OpenAI). Wrap behind internal interfaces.
* **Infra:** Docker Compose for local/dev; deploy on AWS (single EU region). Keep provider boundaries to allow GCP or local runs.

**Service boundaries (high-level):**

* **Gateway (FastAPI):** auth, rate limiting, input normalization.
* **Ingestion service:** text/voice/image handlers → standardized “Intents” → transaction drafts.
* **Classifier service (LLM-assisted):** category & merchant inference with human override.
* **Ledger service:** authoritative write path; ensures idempotency; emits domain events.
* **Insights service:** SQL views/materialized views for “simple analytics.”
* **Subscriptions/billing:** freemium + trials; entitlement checks at feature gates.

**Data model (essentials):**

* **User** ←→ **Account** ←→ **Transaction** (amount, currency, timestamp, memo, merchant, category_id, source_type[text/voice/image], original_payload_ref).
* **Category** (predefined; user-custom only for premium later).
* **Audit trail** (append-only domain events; minimal at start).

---

## 6) AI & Data Design Principles

* **Two-tier LLM pattern:**

  * **Small/intake LLM:** light parsing, intent detection, entity extraction.
  * **Main LLM:** dialog management, edge-case interpretation, repair/clarification prompts.
* **Determinism where it matters:** critical transforms backed by rules/regex/unit tests; LLMs propose, rules validate.
* **Receipts path (MVP):** OCR → **Markdown summary (total/date/vendor)** → parse → transaction draft → user confirm/auto-file via confidence threshold.
* **Confidence & review:** maintain confidence scores; below threshold → ask user in natural language.
* **Observability of AI:** log prompts/responses with redaction; store minimal artifacts necessary for debugging.
* **Switchable providers:** one interface per capability (LLM, OCR, STT). No provider-specific code in business logic.

---

## 7) Security & Privacy Principles

* **Start pragmatic, grow strong.** MVP ships with TLS in transit, basic authN/Z, least-privilege DB creds, secrets in a secure store.
* **Encryption posture:** plan for encryption at rest (DB-level / KMS) even if not enabled day-1; keep schema/infra ready.
* **Data minimization:** store only what’s needed. Separate **original inputs** (voice/image/text) from normalized records; short retention for raw artifacts when possible.
* **User controls:** export my data; delete my data (anonymize where possible).
* **Audit logging plan:** adopt an **evented write path** so every sensitive DB write can emit an audit event even if the sink is minimal at MVP.
* **Compliance compass:** design toward GDPR/CCPA principles; no PCI scope (we don’t process payments); prepare for SSO/Cognito but not required day-1.

---

## 8) Business & Monetization Logic

**Model:** freemium with trials for premium features.

**Free includes:**

* Transactions CRUD
* Text + voice input
* Predefined categories (10–15)
* Simple analytics (SQL-first)
* Limited number of accounts

**Premium candidates (evolving):**

* Custom categories & category management
* OCR (receipts) with auto-categorization
* Extended analytics & forecasting
* Higher account limits
* Early access to new features

**Referrals:** reward with **premium trials** or temporary access to premium modules. Keep it simple and reversible.

**No ads.** Align revenue with user value, not attention harvesting.

---

## 9) Feedback & Learning Loop

* **In-chat prompts:** occasionally ask, “Was this correct?” after auto-categorization or when confidence is low.
* **One-tap feedback:** 👍 / 👎 on transactions and insights; store lightweight reasons.
* **Surveys & pulses:** short, contextual, optional.
* **Anonymous conversational analysis:** aggregate patterns to improve prompts, categories, and heuristics.
* **Weekly iteration:** ship small improvements that reduce friction or increase correctness; maintain a living “Problems We’re Solving Next” list.

---

## 10) What the Product Is / Is Not

**Is:**

* A conversational ledger that captures reality quickly and correctly.
* A pragmatic tool with just-enough AI, designed to be swapped and tuned.
* A privacy-aware system with clear user control.

**Is not (yet):**

* A banking product, a tax advisor, or a trading platform.
* A budgeting suite with envelopes and forecasts on day-1.
* A household sharing platform (arrives later; account-level sharing model).

---

## 11) Early Product Rules (to keep us honest)

1. **Every new feature must justify itself against friction reduction or truthfulness.**
2. **Default to human-readable artifacts.** (e.g., Markdown summaries from OCR)
3. **LLM outputs are proposals; business rules have final say.**
4. **Simple analytics must be expressible in one SQL query or one view.**
5. **Provider interfaces are the boundary; swapping a provider does not touch domain logic.**
6. **Ask users less, infer more — but confirm when confidence is low.**
7. **Delete/Export must remain simple and discoverable.**

---

## 12) Appendices (living)

**A. Predefined categories (seed set):** Groceries, Restaurants, Transport, Housing, Utilities, Personal Care, Health, Entertainment, Education, Misc. *(expand later)*

**B. Minimal entities (MVP):**

* `users(id, email, created_at, …)`
* `accounts(id, user_id, name, starting_balance, currency, …)`
* `transactions(id, account_id, amount_minor, currency, when, merchant, category_id, note, source_type, confidence, original_ref, …)`
* `categories(id, name, is_system, …)`
* `audit_events(id, user_id, entity, action, entity_id, metadata_json, created_at)`

**C. Capability interfaces (sketch):**

* `LLMProvider.generate(messages, tools?)`
* `OCRProvider.extract_total(receipt_image) -> {total, date?, vendor?}`
* `STTProvider.transcribe(audio) -> text`

---

### Final Word

This PRD is a **north star**, not a contract. If a choice makes capture slower or truth fuzzier, we rethink it. We’ll keep the surface area minimal, the boundaries clean, and the loop tight: **ship → learn → refine**.
