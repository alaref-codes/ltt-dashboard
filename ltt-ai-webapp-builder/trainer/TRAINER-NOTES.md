# TRAINER NOTES

## Teaching Goal

Teach the complete AI-assisted software workflow:

Problem
→ Scope
→ Architecture
→ Build
→ Test
→ Debug
→ Git
→ GitHub
→ Vercel
→ Validate

## Recommended Demonstration

1. Start with a bad prompt:
   "Build me an LTT support system."

2. Ask:
   Who uses it?
   What problem?
   What data?
   What action?
   What result?

3. Convert it into a five-feature MVP.

4. Draw:
   USER → FRONTEND → API → BACKEND → DATABASE

5. Build the frontend with synthetic data only.

6. Introduce one deliberate error.

7. Read the exact error.

8. Ask AI for diagnosis, not a rewrite.

9. Create a Git checkpoint.

10. Push to GitHub.

11. Deploy to Vercel.

12. Create a feature branch and demonstrate preview deployment.

## Questions to Ask Trainees

How do you know it works?
Which layer failed?
What evidence do you have?
What changed?
Which file controls this?
Where is the data stored?
Who is allowed to do this?
What happens if the API fails?
What happens if the database is empty?
Would this be safe with real telecom data?
What changes before production?

## Intervention Rules

Intervene if trainees:
- paste real credentials into AI
- use real customer data
- install random packages without understanding why
- change many layers at once
- delete working code without Git checkpoint
- claim success without testing
- deploy before local build works

## Recovery Protocol

1. Stop adding features.
2. Run git status.
3. Identify the last working state.
4. Reproduce one failure.
5. Capture exact evidence.
6. Identify failing layer.
7. Ask AI for diagnosis.
8. Apply smallest fix.
9. Retest.
10. Commit recovered state.

## Suggested Role Rotation

AI DRIVER
→ TESTER
→ REVIEWER
→ AI DRIVER

Every trainee should touch:
AI
code
terminal
browser
Git
deployment

## Assessment

Problem and scope: 15
Application: 25
AI usage: 15
Testing and debugging: 15
Git and GitHub: 10
Deployment: 10
Security: 10

Total: 100
