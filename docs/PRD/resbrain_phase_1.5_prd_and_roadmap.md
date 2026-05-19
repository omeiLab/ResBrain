# Phase 1.5 PRD: Zotero Integration Layer

## Vision

Phase 1.5 connects ResBrain (local research system) with Zotero (external research ecosystem).

> Goal: Use Zotero as ingestion + sync layer, while ResBrain becomes the AI + knowledge layer.

ResBrain does NOT replace Zotero.
It extends Zotero into an AI-ready research infrastructure.

---

# Core Principle

- Zotero = source of truth for bibliographic metadata&#x20;
- ResBrain = source of truth for computation + AI-ready structure

---

# Phase 1.5 Goals

## 1. Zotero Library Ingestion

Support importing user Zotero library via API:

- fetch user items
- fetch collections
- fetch tags
- fetch attachments metadata

Mapping:

- Zotero Item → Paper
- Zotero Tag → Tag
- Zotero Note → Note (optional, Phase 1.5-lite)

---

## 2. One-way Sync (Zotero → ResBrain)

Initial version is **read-only ingestion**:

- ResBrain does NOT push updates back to Zotero
- Zotero remains authoritative source for metadata

---

## 3. ID Mapping Layer (Critical)

Maintain deterministic mapping:

- zotero\_key → resbrain\_paper\_id

Responsibilities:

- prevent duplicate imports
- enable incremental sync
- support re-sync safely (idempotent design)

---

## 4. Incremental Sync Strategy

Phase 1.5 uses **manual + incremental sync**:

- full sync (initial import)
- sync by timestamp / version (if available)
- sync single item by Zotero key

Constraints:

- no real-time sync
- no webhook dependency

---

## 5. Attachment Handling (PDF)

Support Zotero attachments via two modes:

### Mode A: Download local copy

- download PDF from Zotero
- store in ResBrain file system

### Mode B: Reference mode

- store Zotero file metadata only
- no file duplication

Phase 1.5 supports both, but defaults to Mode A.

---

## 6. Data Transformation Layer

Zotero → ResBrain normalization layer:

- title normalization
- author formatting
- tag flattening
- collection mapping (optional)

This layer MUST be isolated from API/router logic.

---

## 7. Sync State Tracking

Track sync status per item:

- last\_synced\_at
- sync\_status (success / failed / partial)
- error logs (optional)

---

# Zotero API Scope

## Required API Endpoints

- GET user items
- GET item metadata
- GET collections
- GET tags
- GET item attachments

## Authentication

- Zotero API Key (user-provided)
- User ID

Store securely in config/env (no plaintext in DB)

---

# ResBrain New Components (Phase 1.5 only)

## 1. Zotero Client Layer

Responsibilities:

- HTTP requests to Zotero API
- retry logic
- pagination handling
- rate limit awareness

---

## 2. Sync Service

Core logic:

- fetch Zotero items
- transform data
- upsert into DB
- update mapping table

Must be idempotent.

---

## 3. Mapping Table

### ZoteroMapping

- id
- zotero\_key (unique)
- paper\_id (FK)
- last\_synced\_at
- sync\_status

---

# API Layer Additions

## Zotero Integration APIs

```
GET  /zotero/status
POST /zotero/connect
POST /zotero/sync/full
POST /zotero/sync/item/{zotero_key}
GET  /zotero/mapping
```

---

# Sync Flow

## Full Sync Flow

```text
Zotero API
  ↓
Fetch items (paginated)
  ↓
Transform layer
  ↓
Dedup via mapping table
  ↓
Upsert into ResBrain DB
  ↓
Update mapping + sync status
```

---

# Edge Cases (Important)

## 1. Duplicate items

Handled via zotero\_key mapping

## 2. Partial sync failure

- continue sync
- log failed items

## 3. Deleted Zotero items

- optional: soft delete in ResBrain
- or ignore in Phase 1.5

## 4. Missing attachments

- allow paper without PDF

---

# UI Additions (Minimal)

## Zotero Sync Panel

- connect API key
- trigger full sync
- show sync status

## Paper Source Label

- "Zotero imported"
- "Local"

---

# Non-Goals

Do NOT implement:

- real-time sync
- Zotero write-back
- browser extension
- embedding / AI features
- RAG system
- collaboration features

---

# Development Order

1. Zotero API client
2. Pagination handling
3. Sync service (fetch → transform)
4. Mapping table implementation
5. Upsert logic
6. Sync APIs
7. Minimal UI trigger

---

# Definition of Done

Phase 1.5 is complete when:

- Zotero library can be imported reliably
- mapping prevents duplicates
- sync is idempotent
- PDF attachments handled
- ResBrain remains independent system

---

# Outcome

ResBrain evolves into:

> a structured research data layer built on top of Zotero

This enables Phase 2:

- embeddings on real-world papers
- semantic search
- research memory system
- citation graph construction

---

# Key Insight

Phase 1.5 is not feature expansion.

It is:

> turning Zotero from a UI tool into a deterministic data ingestion pipeline for AI systems.

