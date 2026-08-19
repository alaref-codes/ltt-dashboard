---
name: ltt-ai-webapp-builder
description: >
  Trainer-ready skill for LTT trainees to use AI to scope, build, test,
  debug, secure, publish to GitHub, and deploy practical web applications
  to Vercel. Designed for mixed technical levels and daily telecom work.
version: "1.0.0"
audience:
  - LTT trainees
  - business analysts
  - technical support staff
  - network and operations staff
  - developers
  - data analysts
  - product teams
  - trainers
default_stack:
  frontend: Next.js + React + TypeScript + Tailwind CSS
  backend: Next.js Route Handlers
  database: Supabase PostgreSQL
  version_control: Git + GitHub
  deployment: Vercel
training_mode: practical
---

# LTT AI Web App Builder

## Purpose

Teach trainees to move from a telecom work problem to a tested, versioned,
and deployed web application using AI as a development partner.

The core workflow is:

Problem → Scope → Plan → Build → Run → Test → Debug → Secure → Commit → Deploy → Verify → Improve

The objective is not to make every trainee a traditional software engineer.
The objective is to help trainees use AI effectively while understanding,
testing, and controlling what gets built.

## Core Rule

AI-generated code is a proposal until evidence shows it works.

Never claim:
- the application works without running it
- an API works without testing it
- a deployment succeeded without opening it
- a security issue is fixed without retesting it

Use these states:

GENERATED
RUN
TESTED
VERIFIED

## Skill Behavior

When helping a trainee:

1. Identify the current phase:
   IDEA, SCOPE, SETUP, FRONTEND, BACKEND, DATABASE, API, TESTING,
   DEBUGGING, SECURITY, GIT, GITHUB, DEPLOYMENT, VALIDATION, IMPROVEMENT.

2. Explain:
   - what we are doing
   - why we are doing it
   - what file changes
   - how to test it
   - what success looks like

3. Never invent:
   - terminal output
   - test results
   - API responses
   - database records
   - build status
   - deployment status
   - security findings

4. Before major changes, create a checkpoint:

```bash
git status
git add .
git commit -m "checkpoint before feature change"
```

5. Make one logical change at a time.

## Mixed Technical Levels

### Level A: AI-Assisted Operator

Should understand:
- frontend
- backend
- API
- database
- GitHub
- deployment
- commands
- common errors
- AI prompting
- verification

### Level B: AI-Assisted Builder

Also understands:
- components
- TypeScript basics
- JSON
- CRUD
- route handlers
- environment variables
- Git branches
- deployment logs

### Level C: Advanced Builder

Also works with:
- authentication
- authorization
- database policies
- automated tests
- logging
- security reviews
- architecture decisions
- pull requests
- preview deployments

## Web Application Mental Model

```text
USER
  |
  v
FRONTEND
  |
  | HTTP / API
  v
BACKEND
  |        |
  v        v
DATABASE  EXTERNAL API
```

Frontend = pages, forms, tables, buttons, filters, dashboards.

Backend = validation, business rules, permissions, API calls, data processing.

Database = persistent structured information.

API = communication between systems.

## Recommended Training Stack

Use:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Supabase
- Git
- GitHub
- Vercel
- ChatGPT, Codex, Claude Code, Cursor, or GitHub Copilot

Use one standard stack in class to reduce setup differences.

## Default Project Setup

```bash
npx create-next-app@latest ltt-issue-tracker
cd ltt-issue-tracker
npm run dev
```

Recommended create-next-app choices:

```text
TypeScript: Yes
ESLint: Yes
Tailwind CSS: Yes
App Router: Yes
```

Open:

```text
http://localhost:3000
```

Do not continue until the starter application runs.

## AI Prompting Pattern

Use:

CONTEXT
TASK
CONSTRAINTS
INPUT
ACCEPTANCE CRITERIA
OUTPUT

### Project Scoping Prompt

```text
CONTEXT

I work at a telecom company.
I want to solve an internal operational problem with a small web application.

PROBLEM

[describe the problem]

USERS

[list the users]

TASK

Help me define an MVP suitable for a training session.

CONSTRAINTS

Use synthetic data only.
Use Next.js, TypeScript and Tailwind.
Keep the MVP to five core features maximum.

OUTPUT

Return:
1. Problem statement
2. User roles
3. Five core features maximum
4. Data model
5. Required pages
6. Required API endpoints
7. Acceptance criteria
8. Explicit V1 exclusions
```

### Architecture Prompt

```text
Act as a senior web application architect and teacher.

PROJECT
[project description]

STACK
Next.js
TypeScript
Tailwind
Supabase PostgreSQL
Vercel

Design the smallest architecture needed for the MVP.

Show:
1. frontend components
2. backend responsibilities
3. database tables
4. API routes
5. data flow
6. environment variables
7. security boundaries
8. folder structure

Explain each part for a trainee with basic technical knowledge.

Do not generate application code yet.
```

### Feature Prompt

```text
TASK

[feature]

FILES TO INSPECT

[list relevant files]

REQUIREMENTS

[list requirements]

CONSTRAINTS

Preserve the current working layout.
Do not change unrelated code.
Use existing dependencies whenever possible.

ACCEPTANCE CRITERIA

[list criteria]

Before editing, explain which files you plan to change.
After editing, explain exactly how to test the feature.
```

### Debugging Prompt

```text
I need you to diagnose this error.

EXPECTED BEHAVIOR
[expected]

ACTUAL BEHAVIOR
[actual]

EXACT ERROR
[paste exact error]

LAST WORKING STATE
[describe]

RECENT CHANGES
[describe]

RELEVANT CODE
[paste code]

TASK
1. Identify the most likely cause.
2. Show how to prove or reject the hypothesis.
3. Propose the smallest fix.
4. Do not rewrite unrelated files.
5. Tell me exactly how to retest it.
```

### Security Review Prompt

```text
Act as a defensive application security reviewer.

Review this training web application for:
- exposed secrets
- authentication
- authorization
- input validation
- database permissions
- sensitive data in logs
- insecure environment variables
- injection risks
- information leakage
- dependency risks
- file upload risks
- missing rate limits

Classify findings:
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL

For every finding provide:
1. component
2. risk
3. evidence
4. fix
5. test to verify the fix

Do not claim a vulnerability exists without evidence.
```

## Project Scoping Canvas

Every team fills this before coding:

```text
PROJECT NAME:

BUSINESS PROBLEM:

PRIMARY USER:

SECONDARY USER:

CURRENT PROCESS:

PROBLEM WITH CURRENT PROCESS:

DESIRED OUTCOME:

INPUT DATA:

OUTPUT:

MUST-HAVE FEATURES:
1.
2.
3.
4.
5.

NOT IN V1:
1.
2.
3.

DATA CLASSIFICATION:

EXTERNAL SYSTEMS REQUIRED:

SUCCESS CRITERIA:

DEPLOYMENT TARGET:

OWNER:
```

## Five-Feature Rule

For training MVPs, use five primary features maximum.

Example LTT Issue Tracker:

1. Create issue
2. View issues
3. Filter issues
4. Update status
5. View summary statistics

Do not add AI, SMS, GIS, billing integrations, authentication, or other
large features until the basic workflow works.

## Reference Telecom Training App

Project:

LTT Service Issue Tracker

Purpose:

Create and track synthetic telecom service issues.

Example services:
- 4G
- ADSL
- VDSL
- FWA
- Fiber
- Libya Phone
- MyLTT / LTT Life
- Other

Example fields:

```text
id
service
area
category
severity
description
status
assigned_team
created_at
updated_at
```

Statuses:

```text
new
assigned
investigating
resolved
closed
```

Severities:

```text
low
medium
high
critical
```

Use fictional incidents, users, areas, IDs, and records.

## Suggested Folder Structure

```text
app/
  api/
    issues/
      route.ts
  issues/
    page.tsx
  layout.tsx
  page.tsx

components/
  IssueForm.tsx
  IssueTable.tsx
  IssueFilters.tsx
  SummaryCards.tsx

lib/
  supabase.ts
  validation.ts

types/
  issue.ts

.env.local
.gitignore
package.json
README.md
tsconfig.json
```

## Environment Variables

Example:

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SERVER_ONLY_API_KEY=
```

Rules:

- Keep secrets outside source code.
- Do not commit .env.local.
- Do not put server secrets in variables intended for browser use.
- Add required variables to Vercel.
- Redeploy after changing deployment environment variables.

Environment checklist:

- [ ] .env.local exists when required
- [ ] .env.local is ignored by Git
- [ ] no secret appears in source code
- [ ] public variables are intentionally public
- [ ] server-only secrets remain server-only
- [ ] Vercel contains required variables

## Database Basics

A database stores persistent structured information.

Example table:

```sql
create table issues (
  id bigint generated by default as identity primary key,
  service text not null,
  area text not null,
  category text,
  severity text not null,
  description text not null,
  status text not null default 'new',
  assigned_team text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

Teach:

Create table
→ determine who needs access
→ configure permissions
→ test authorized access
→ test unauthorized access

Never solve access problems by making everything public.

## CRUD

CREATE = create issue
READ = view issues
UPDATE = change status
DELETE = remove or archive test record

Typical API mapping:

POST = CREATE
GET = READ
PATCH = UPDATE
DELETE = DELETE

## API Basics

Example endpoints:

```text
GET /api/issues
POST /api/issues
PATCH /api/issues/{id}
```

Validate server-side:
- required values
- allowed enum values
- input lengths
- user permissions
- valid status transitions

Never assume frontend controls provide sufficient validation.

## Git Mental Model

```text
Working files
   |
git add
   v
Staging area
   |
git commit
   v
Local history
   |
git push
   v
GitHub
```

Essential commands:

```bash
git status
git diff
git add .
git commit -m "add issue creation form"
git log --oneline
git remote -v
```

Publish:

```bash
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git branch -M main
git push -u origin main
```

Good commit messages:

```text
add issue creation form
add service filter
validate severity on API
fix empty dashboard state
configure Supabase client
```

Avoid:

```text
update
fix
stuff
final
final2
```

## Branch Workflow

```bash
git switch -c feature/service-filter
```

Then:

```bash
git add .
git commit -m "add service filter"
git push -u origin feature/service-filter
```

Review through a pull request before merging.

## Vercel Workflow

```text
Local computer
   |
git push
   v
GitHub
   |
   v
Vercel
   |
   v
Preview / Production URL
```

Deployment steps:

1. Push project to GitHub.
2. Open Vercel.
3. Add New → Project.
4. Import GitHub repository.
5. Confirm Next.js framework.
6. Add required environment variables.
7. Deploy.
8. Open deployment URL.
9. Test deployed application.

## Deployment Validation

- [ ] home page loads
- [ ] navigation works
- [ ] mobile view works
- [ ] data loads
- [ ] form submission works
- [ ] database writes work
- [ ] database reads work
- [ ] invalid input is rejected
- [ ] authentication works if implemented
- [ ] unauthorized actions are blocked
- [ ] Arabic text displays correctly
- [ ] browser console has no critical errors
- [ ] server logs have no unresolved errors

## Preview Deployment Workflow

```text
main
 |
 +-- feature/new-dashboard
          |
         push
          |
          v
      Vercel Preview
          |
         test
          |
      Pull Request
          |
        merge
          |
          v
      Production
```

## Build Before Deployment

Run:

```bash
npm run build
npm run lint
```

Investigate build failures before relying on deployment logs.

## Debugging Framework

Use:

SYMPTOM
→ EVIDENCE
→ LAYER
→ HYPOTHESIS
→ TEST
→ FIX
→ RETEST

Layer guide:

```text
UI looks wrong → frontend
button does nothing → frontend/browser
400 → request/validation
401 → authentication
403 → authorization
404 → route/path
500 → backend/database
database denied → permissions/RLS
works locally only → environment/deployment/runtime
build fails → code/types/dependencies/configuration
```

## Common Troubleshooting

### Missing environment variable

Check:
- spelling
- correct environment
- Vercel variable exists
- deployment rebuilt

### Module not found

Check:
- package installed
- import path
- filename capitalization
- package.json

### Blank page

Check:
- browser console
- terminal
- rendering error
- imports
- failed API calls
- client/server component mistakes

### API 500

Check:
- server logs
- database connection
- JSON parsing
- environment variables
- query errors
- null handling

### Database permission error

Check:
- authentication state
- database role
- RLS
- policies
- table grants

### Works locally, fails after deployment

Compare:
- environment variables
- runtime
- database
- URLs
- build settings
- filesystem assumptions

## Testing Strategy

Use four layers:

1. BUILD TEST
2. FEATURE TEST
3. INTEGRATION TEST
4. DEPLOYMENT TEST

Example feature test:

```text
Feature:
Create issue

Input:
service = Fiber
area = Training Zone A
severity = high
description = Synthetic fiber connectivity issue

Expected:
One issue is created.
It appears in the list.
Status is new.
```

Negative tests:
- missing service
- invalid severity
- long input
- duplicate submission
- unauthorized request
- invalid ID
- network failure
- database failure
- empty database

## Security Rules for Telecom Training

Use synthetic data only.

Do not put real data in:
- AI prompts
- public repositories
- demo databases
- Vercel demos
- screenshots
- README examples
- logs

Do not use:
- real MSISDNs
- real customer names
- national IDs
- payment information
- CDRs
- private network addresses
- internal hostnames
- VPN credentials
- production tokens
- production database exports

## Demo vs Production

Training demo:
- synthetic data
- rapid iteration
- GitHub training repository
- Vercel
- Supabase
- learning focus

LTT production:
- approved infrastructure
- approved identity
- data classification
- access control
- audit logging
- backups
- monitoring
- change management
- security testing
- incident response
- production support

A Vercel training deployment proves the development workflow.
It does not approve an application for production telecom workloads.

## Security Minimum Checklist

- [ ] no credentials committed
- [ ] no real customer data used
- [ ] inputs validated
- [ ] sensitive operations require authentication
- [ ] authorization checked server-side
- [ ] database permissions reviewed
- [ ] RLS reviewed where applicable
- [ ] errors do not reveal secrets
- [ ] logs do not expose sensitive data
- [ ] environment variables classified correctly
- [ ] build succeeds
- [ ] negative tests performed

## Guided Labs

### Lab 1: Scope a Telecom App

Deliverable:
PROJECT-SCOPE.md

Do not start coding until trainees can answer:
- Who uses it?
- What problem does it solve?
- What are its five features?
- What data does it need?
- How do we know it works?

### Lab 2: Build the Frontend

Use hard-coded synthetic data first.

Required UI:
- dashboard
- summary cards
- issue table
- create form
- filters
- empty state

Quality gate:
- [ ] app opens
- [ ] UI is readable
- [ ] synthetic records display
- [ ] filters work
- [ ] empty state exists
- [ ] mobile layout is usable

### Lab 3: Add the API

Create:
- GET /api/issues
- POST /api/issues

Quality gate:
- [ ] GET returns expected JSON
- [ ] POST validates fields
- [ ] valid POST succeeds
- [ ] invalid POST fails cleanly
- [ ] frontend consumes API data

### Lab 4: Add Database Persistence

Sequence:

Create database
→ create table
→ configure access
→ set environment variables
→ connect application
→ read
→ create
→ update
→ verify persistence

Proof:
Create a record, refresh the page, verify it still exists.

### Lab 5: Debug and Test

Trainer introduces one bug.

Required process:
1. reproduce
2. capture exact error
3. classify layer
4. form hypothesis
5. test hypothesis
6. smallest fix
7. retest
8. commit

Deliverable:
DEBUG-REPORT.md

### Lab 6: GitHub

```bash
git status
git add .
git commit -m "complete issue tracker MVP"
```

Push to GitHub.

Verify:
- [ ] repository exists
- [ ] README exists
- [ ] .env.local absent
- [ ] no secrets present
- [ ] latest commit visible

### Lab 7: Deploy to Vercel

Steps:
1. Import GitHub repository
2. Configure project
3. Add environment variables
4. Deploy
5. Open live URL
6. Test
7. Inspect logs

### Lab 8: Feature Branch and Preview

```bash
git switch -c feature/critical-filter
```

Implement:
Show unresolved critical 4G and Fiber issues.

Then:
modify
→ test locally
→ build
→ commit
→ push
→ preview
→ pull request
→ merge
→ production

## Telecom Project Exercise Bank

1. Service Incident Tracker
2. Customer Complaint Dashboard
3. Network Maintenance Board
4. Field Team Task Tracker
5. SLA Monitoring Dashboard
6. Telecom KPI Exception Board
7. Knowledge Base Search
8. Device Inventory Tracker
9. Outage Communication Board

All use synthetic data.

## Daily Telecom Work Pattern

Look for repetitive work involving:
- spreadsheets
- email
- manual forms
- copy/paste
- status tracking
- approval
- search
- reports
- calculations
- dashboards
- classification
- follow-up

Ask:

Could a small internal web application reduce this repeated work?

## AI Roles

Use AI intentionally as:

1. ANALYST
2. ARCHITECT
3. BUILDER
4. TESTER
5. DEBUGGER
6. REVIEWER

Do not ask one giant prompt to perform every role at once.

## Project Constitution

Create PROJECT.md containing:

```text
Purpose
Users
Stack
Core Features
Non-Goals
Data Model
Security Rules
UI Rules
Coding Rules
Acceptance Criteria
Deployment
Current Status
```

Tell AI:

```text
Read PROJECT.md before implementing changes.
Treat it as the project source of truth.
```

## AI Rules File

Recommended AI-RULES.md:

```text
1. Read existing code before editing.
2. Do not rewrite unrelated files.
3. Prefer existing dependencies.
4. Explain major changes.
5. Do not expose secrets.
6. Validate external input.
7. Do not invent test results.
8. Request or run validation after changes.
9. Keep components focused.
10. Preserve working features.
11. Use synthetic telecom data.
12. Update README when setup changes.
```

## Definition of Done

SCOPE
- [ ] problem clear
- [ ] users identified
- [ ] MVP defined
- [ ] non-goals defined

BUILD
- [ ] frontend works
- [ ] backend works when required
- [ ] persistence works when required
- [ ] APIs work when required

QUALITY
- [ ] acceptance criteria tested
- [ ] invalid inputs tested
- [ ] build succeeds
- [ ] important errors handled

SECURITY
- [ ] synthetic data only
- [ ] no secrets committed
- [ ] access controls reviewed
- [ ] environment variables reviewed

GIT
- [ ] meaningful commits
- [ ] clean repository
- [ ] README exists

DEPLOYMENT
- [ ] Vercel deployment exists
- [ ] live workflow tested
- [ ] environment variables configured

UNDERSTANDING
- [ ] trainee explains frontend
- [ ] trainee explains backend
- [ ] trainee explains database
- [ ] trainee explains API
- [ ] trainee explains GitHub
- [ ] trainee explains deployment

## Trainer Walkthrough Notes

Start with a poor prompt:

```text
Build me an LTT support system.
```

Ask:
- Who uses it?
- What problem?
- What data?
- What action?
- What result?

Rewrite it into a scoped MVP.

Draw the architecture:

```text
USER
 |
FRONTEND
 |
API
 |
BACKEND
 |
DATABASE
```

Build the first screen without a database.

Then deliberately break something, read the exact error, and use AI to diagnose it.

Show Git as a recovery and history system.

Finally show:

Laptop → GitHub → Vercel → Browser

Then demonstrate a feature branch and preview deployment.

## Trainer Questions

Ask:
- How do you know it works?
- Which layer failed?
- What evidence do you have?
- What changed?
- Which file controls this behavior?
- Where is the data stored?
- Who is allowed to perform this action?
- What happens if the API fails?
- What happens if the database is empty?
- Would this be safe with real telecom data?
- What changes before production?

## Trainer Recovery Protocol

When a team gets stuck:

1. Stop adding features.
2. Run git status.
3. Identify last known working commit.
4. Reproduce one failure.
5. Capture exact evidence.
6. Identify failing layer.
7. Ask AI for diagnosis, not a rewrite.
8. Apply smallest fix.
9. Retest.
10. Commit recovered state.

## Final Capstone

Each team delivers:

- PROJECT-SCOPE.md
- PROJECT.md
- working application
- README.md
- GitHub repository
- Vercel deployment
- test checklist
- debug report
- security checklist
- short live demonstration

Rules:
- five core features maximum
- synthetic data only
- at least one API interaction
- database required
- one negative test
- at least three meaningful commits
- one feature branch
- one preview deployment
- one production deployment

## Final Response Pattern

When assisting a trainee, respond with:

CURRENT PHASE

WHAT WE ARE TRYING TO ACHIEVE

WHY IT MATTERS

NEXT ACTION

COMMAND OR CODE

WHAT SUCCESS LOOKS LIKE

HOW TO TEST

WHAT TO DO IF IT FAILS

NEXT CHECKPOINT

## Golden Rule

Do not use:

Ask AI → copy code → hope

Use:

Define
→ Prompt
→ Inspect
→ Build
→ Run
→ Test
→ Debug
→ Secure
→ Version
→ Deploy
→ Verify
→ Improve
