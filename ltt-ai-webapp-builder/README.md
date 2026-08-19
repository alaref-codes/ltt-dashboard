# LTT AI Web App Builder Skill

Trainer-ready skill package for teaching LTT trainees how to use AI to build,
test, debug, push, and deploy practical telecom web applications.

## Install

### Generic skill folder

Copy the whole `ltt-ai-webapp-builder` folder into the skills directory used by
your AI coding environment.

The important entry file is:

```text
ltt-ai-webapp-builder/SKILL.md
```

### Claude Code style

Place the folder under your configured skills directory, for example:

```text
.claude/skills/ltt-ai-webapp-builder/
```

### Project-local use

You may also keep the folder inside a training repository:

```text
training-project/
  skills/
    ltt-ai-webapp-builder/
      SKILL.md
```

Then instruct the AI to read `SKILL.md` before helping with the project.

## Recommended trainee instruction

```text
Use the ltt-ai-webapp-builder skill.

Help me build a telecom web application using the workflow in the skill.
Start by identifying the current phase and do not jump directly to coding.

My problem is:
[describe the work problem]
```

## Package Contents

```text
SKILL.md
README.md
templates/
  PROJECT.md
  PROJECT-SCOPE.md
  AI-RULES.md
  DEBUG-REPORT.md
  TEST-CHECKLIST.md
prompts/
  MASTER-PROMPTS.md
labs/
  LABS.md
trainer/
  TRAINER-NOTES.md
```

## Recommended Stack

Next.js + TypeScript + Tailwind + Supabase + GitHub + Vercel

## Training Safety

Use synthetic telecom data only.
Do not put real customer data, credentials, network details, or production
secrets into public repositories, AI prompts, or demo deployments.
