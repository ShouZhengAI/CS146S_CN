# Week 8 – Multi-Stack AI-Accelerated Web App Build

## Demo Day Confirmation
Please navigate to this [form](https://forms.gle/J3R3PSRqnFAJxhjG8) for details about our class demo day.


## Assignment Overview
Build the same functional web application in 3 distinct technology stacks. At least one version must be created using [`bolt.new`](https://bolt.new/), an AI app generation platform. At least one version must use a non-JavaScript language for either the frontend or backend (e.g., Django, Ruby on Rails).

You may reuse the app from previous weeks (the "developer control center") or create a new app of your choosing, as long as it meets the [minimum functional scope](#minimum-functional-scope). The app should be end-to-end functional (frontend + backend + persistence where applicable) and demonstrate a coherent feature set.

## Minimum Functional Scope 
- User can create, read, update, and delete a primary resource (e.g., notes, tasks, posts).
- Persistent storage (database or file-based) where appropriate for the stack.
- Basic validation and error handling.
- Simple but functional UI that surfaces the main flows.
- Clear instructions to run each version locally (and deploy links if you deploy).

## Stack Requirements
Build 3 separate versions of the same app, each of which use a distinct stack. Examples:
- MERN (MongoDB, Express, React, Node.js)
- MEVN (MongoDB, Express, Vue.js, Node.js)
- Django + React (or Vue)
- Flask + Vanilla JS (or React)
- Next.js + Node (or NestJS)
- Ruby on Rails (full-stack)

Reminder that at least one version must include a non-JavaScript language for either frontend or backend (e.g., Python/Django, Ruby/Rails).


At least one version must be built using the AI app generation platform **[`bolt.new`](https://bolt.new/)**, but feel free to explore other app generation platforms (e.g. Lovable, Figma Make) for the other versions.


## Learn about Bolt
Bolt is an AI-assisted development platform that generates websites, web apps, and mobile apps from natural language prompts. Users can describe their idea in plain text, and Bolt produces a functional prototype—ranging from landing pages and e-commerce sites to CRMs and mobile tools—within minutes. Learn more [here](https://support.bolt.new/building/intro-bolt).

### Claim your Bolt Credits:
1. Locate the unique Bolt promotion code that we've emailed to you.
2. Navigate to [bolt.new](bolt.new) and create an account.
3. In Personal Settings > Subscriptions & Tokens, in the Upgrade to Pro block, click the blue "Upgrade" button.
3. Select "Add promotion code" and paste your unqiue promotion code into this field.
4. You’ll receive 3 months of Bolt Pro for free. A credit card is required to activate the trial. **Remember to cancel before the 3-month period ends to avoid automatic billing if you don’t plan to continue your subscription.**


## Tips for Usage of AI App Generators
- App generators like Bolt are best-suited for modern full-stack technologies, which you will get by default when using them without specifying specific frameworks.
- Prefer starting from a clean prompt describing your app concept, entities, routes, and UI flows.
- Clearly describe data models and relationships in your prompts.
- Iteratively refine prompts for data models, CRUD endpoints, auth (if used), and frontend components.
- Keep each version isolated to avoid dependency conflicts.
- Export or sync generated code and commit it as a standalone project folder for that stack.
 
## Deliverables
1) **THREE** project folders (one per version) within the `week8/` folder, each including:
   - Source code
   - `README.md` with prerequisites, installation/set-up instructions, run, and env configuration
   - Notes on deviations, known issues, and any manual fixes after generation
2) Completed `writeup.md` file:
   - App Concept
   - 3 App Descriptions (1 per version)

## Grading Rubric (100 points)
- App concept meets minimum functional scope (10 pts)
- Three distinct tech stacks (10 pts)
- Usage of Bolt in at least one version (10 pts)
- Usage of a non-JS language in at least one version (10 pts)
- Three version of the app (20 pts **each**):
   - Source code provided in a folder in `week8/`(5pts)
   - README.md: prerequisites, installation/set-up instructions, run, and env configuration (5 pts)
   - App functionality (5 pts)
   - Complete version description detailed in `writeup.md` (5 pts)

