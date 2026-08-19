# MASTER PROMPTS

## 1. Scope a Project

```text
CONTEXT

I work at a telecom company.

PROBLEM
[describe]

USERS
[list]

TASK

Define a training-ready MVP.

CONSTRAINTS

Use synthetic data only.
Use Next.js, TypeScript, Tailwind.
Five core features maximum.

OUTPUT

1. problem statement
2. users
3. five core features
4. data model
5. pages
6. API endpoints
7. acceptance criteria
8. V1 exclusions
```

## 2. Architecture

```text
Act as a senior web application architect and teacher.

PROJECT
[description]

STACK
Next.js
TypeScript
Tailwind
Supabase
Vercel

Design the smallest architecture required.

Return:
frontend components
backend responsibilities
database tables
API routes
data flow
environment variables
security boundaries
folder structure

Do not generate code yet.
```

## 3. Implement a Feature

```text
Read PROJECT.md first.

GOAL
[feature]

USER
[user]

BUSINESS REASON
[reason]

ACCEPTANCE CRITERIA
1.
2.
3.

CONSTRAINTS
Preserve existing features.
Do not expose secrets.
Do not add dependencies unless required.
Validate external input.
Use synthetic data.

PROCESS
1. inspect relevant files
2. explain plan
3. identify risks
4. make smallest coherent change
5. report files changed
6. provide exact test steps
7. identify anything still unverified
```

## 4. Debug

```text
EXPECTED
[expected]

ACTUAL
[actual]

EXACT ERROR
[paste]

RECENT CHANGE
[describe]

RELEVANT FILES
[paste]

First:
1. classify failing layer
2. list three likely hypotheses
3. rank them
4. give smallest test for hypothesis #1

Do not rewrite the application.
```

## 5. Review

```text
Review changes since the last Git commit.

Check:
incorrect logic
duplicate code
unnecessary complexity
missing validation
broken error handling
security risks
TypeScript errors
dead code
inconsistent naming
loading states
empty states
accessibility

Classify:
BLOCKER
IMPORTANT
OPTIONAL

Return findings before suggesting changes.
```

## 6. Security Review

```text
Act as a defensive security reviewer.

Check:
secrets
authentication
authorization
validation
database permissions
logs
public APIs
environment variables
injection
error leakage
dependencies
uploads
rate limiting

Classify:
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL

For each finding:
component
risk
evidence
fix
verification test

Do not claim findings without evidence.
```
