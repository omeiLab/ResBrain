# ResBrain Phase 1 PRD & Roadmap

## Vision

ResBrain is an AI-augmented research operating system focused on helping researchers:

- organize papers
- build research memory
- retrieve knowledge efficiently
- gradually evolve into an intelligent research assistant

Phase 1 focuses on:

> Building a minimal but usable "AI-ready Zotero-like system"

The goal is NOT to compete with Zotero.
The goal is to build the foundational infrastructure for future AI-powered research workflows.

---

# Phase 1 Goals

## Core Goal

Build a working research paper management system with:

- paper storage
- metadata management
- tagging
- note-taking
- semantic-ready architecture
- simple usable UI

At the end of Phase 1, the system should allow:

1. Adding papers
2. Browsing papers
3. Searching papers
4. Viewing paper details
5. Writing notes
6. Structuring data for future embeddings/RAG

---

# Phase 1 Philosophy

## DO

- focus on shipping
- prioritize architecture clarity
- keep UI minimal
- build AI-ready backend structure
- optimize for learning + maintainability

## DO NOT

- rebuild full Zotero
- overengineer frontend
- optimize prematurely
- build complex auth systems
- build cloud infrastructure too early

---

# MVP Scope

## Included Features

### 1. Paper Library

Users can:

- add papers manually
- edit metadata
- delete papers
- browse all papers

Fields:

- title
- authors
- abstract
- year
- venue
- tags
- local PDF path (optional)

---

### 2. Search

Basic keyword search:

- title
- abstract
- tags

(No embeddings yet in Phase 1)

---

### 3. Notes

Each paper can have:

- personal notes
- summary notes
- idea fragments

---

### 4. Tagging System

Users can:

- add tags
- filter by tags

Example:

- NLP
- alignment
- bias
- evaluation
- RAG

---

### 5. Basic UI

Pages:

- paper list
- paper detail page
- add/edit paper page

Minimal UI only.
No advanced design requirements.

---

# Future AI Hooks (Important)

Even though embeddings/RAG are NOT Phase 1 features,
Phase 1 architecture should prepare for them.

Design the backend assuming future additions:

- embedding generation
- semantic search
- auto summarization
- citation graph
- recommendation system
- research memory

---

# Recommended Tech Stack

## Backend

### FastAPI
Purpose:

- API layer
- routing
- backend service architecture

Why:

- Python-native
- ideal for AI systems
- async-ready
- easy future scaling

---

## Database

### SQLite (initially)
Purpose:

- local development
- fast iteration

Future:

- PostgreSQL

---

## ORM

### SQLModel or SQLAlchemy

Recommendation:

Start with SQLModel.

Reason:

- easier learning curve
- integrates well with FastAPI
- sufficient for Phase 1

---

## Frontend

### Jinja2 + HTML + minimal CSS

Purpose:

- fast iteration
- avoid frontend complexity
- focus on system functionality

Optional:

- small amount of vanilla JS
- fetch API

---

## Styling

Minimal CSS only.

Goals:

- readable
- usable
- clean layout

Not goals:

- advanced animations
- pixel-perfect UI
- design systems

---

# Recommended Folder Structure

```text
resbrain/
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── database/
│   └── schemas/
│
├── tests/
├── requirements.txt
├── README.md
└── .env
```

---

# Suggested Database Schema

## Paper

```text
Paper
- id
- title
- authors
- abstract
- year
- venue
- pdf_path
- created_at
```

---

## Tag

```text
Tag
- id
- name
```

---

## PaperTag

```text
PaperTag
- paper_id
- tag_id
```

---

## Note

```text
Note
- id
- paper_id
- content
- created_at
```

---

# API Design (Phase 1)

## Paper APIs

```text
GET    /papers
GET    /papers/{id}
POST   /papers
PUT    /papers/{id}
DELETE /papers/{id}
```

---

## Notes APIs

```text
POST /papers/{id}/notes
GET  /papers/{id}/notes
```

---

## Tags APIs

```text
GET  /tags
POST /tags
```

---

# UI Screens

## 1. Paper List Page

Features:

- paper list
- search bar
- tag filter
- add paper button

---

## 2. Paper Detail Page

Features:

- metadata
- abstract
- notes
- tags
- edit button

---

## 3. Add/Edit Page

Features:

- form input
- save/update

---

# Technical Skills You Need To Learn

## Priority 1 (Immediate)

### FastAPI Basics

Learn:

- routing
- request/response
- JSON
- Pydantic models
- templates

Goal:

Convert Python logic into backend services.

---

### HTTP Basics

Learn:

- GET vs POST
- request body
- status codes
- REST concepts

---

### HTML Basics

Learn:

- forms
- input
- textarea
- buttons
- links

---

### Basic CSS

Only:

- flexbox
- spacing
- layout
- typography basics

Avoid advanced frontend topics.

---

## Priority 2 (Soon)

### Database Basics

Learn:

- tables
- relationships
- CRUD
- simple queries

---

### ORM Usage

Learn:

- model definitions
- sessions
- querying
- relationships

---

### Project Structure

Learn:

- separating routers/services/models
- reusable functions
- config organization

---

## Priority 3 (Later)

### Embeddings

Learn:

- vector embeddings
- semantic similarity
- retrieval

---

### RAG Architecture

Learn:

- retrieval pipeline
- chunking
- prompt augmentation

---

### Docker

Learn:

- container basics
- reproducible environments

---

# Recommended Development Order

## Step 1

Set up FastAPI project.

Goal:

Run:

```bash
uvicorn app.main:app --reload
```

---

## Step 2

Create paper model + SQLite connection.

Goal:

Store papers in DB.

---

## Step 3

Implement CRUD APIs.

Goal:

- create paper
- view paper
- edit paper
- delete paper

---

## Step 4

Build Jinja2 pages.

Goal:

Usable browser interface.

---

## Step 5

Implement notes + tags.

Goal:

Basic research workflow.

---

## Step 6

Implement keyword search.

Goal:

Search your library.

---

# Definition of Done (Phase 1)

Phase 1 is complete when:

- papers can be added and edited
- notes can be attached
- tags work
- search works
- data persists in database
- UI is usable
- architecture is clean enough for AI expansion

NOT required:

- production deployment
- authentication
- vector search
- multi-user support
- cloud infrastructure
- advanced frontend

---

# Phase 1 Success Criteria

A successful Phase 1 means:

> You have transformed from writing isolated Python scripts into building an actual AI-ready research system.

The most important outcome is NOT the app itself.

The most important outcome is:

- learning service architecture
- learning backend thinking
- learning how AI systems are structured
- building reusable infrastructure for future research tools

---

# Suggested Mental Model

ResBrain is NOT:

- a website project
- a frontend project
- a CRUD tutorial

ResBrain IS:

- research infrastructure
- AI tooling
- knowledge systems engineering
- the foundation for future intelligent research workflows

