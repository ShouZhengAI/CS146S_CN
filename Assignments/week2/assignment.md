# Week 2 – Action Item Extractor

This week, we will be expanding upon a minimal FastAPI + SQLite app that converts free‑form notes into enumerated action items.

***We recommend reading this entire document before getting started.***

Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`


## Getting Started

### Cursor Set Up
Follow these instructions to set up Cursor and open your project:
1. Redeem your free year of Cursor Pro: https://cursor.com/students
2. Download Cursor: https://cursor.com/download
3. To enable the Cursor command line tool, open Cursor and press `Command (⌘) + Shift+ P` for Mac users (or `Ctrl + Shift + P` for non-Mac users) to open the Command Palette. Type: `Shell Command: Install 'cursor' command`. Select it and hit Enter.
4. Open a new terminal window, navigate to your project root, and run: `cursor .`

### Current Application
Here's how you can start running the current starter application: 
1. Activate your conda environment.
```
conda activate cs146s 
```
2. From the project root, run the server:
```
poetry run uvicorn week2.app.main:app --reload
```
3. Open a web browser and navigate to http://127.0.0.1:8000/.
4. Familiarize yourself with the current state of the application. Make sure you can successfully input notes and produce the extracted action item checklist. 

## Exercises
For each exercise, use Cursor to help you implement the specified improvements to the current action item extractor application.

As you work through the assignment, use `writeup.md` to document your progress. Be sure to include the prompts you use, as well as any changes made by you or Cursor. We will be grading based on the contents of the write-up. Please also include comments throughout your code to document your changes. 

### TODO 1: Scaffold a New Feature

Analyze the existing `extract_action_items()` function in `week2/app/services/extract.py`, which currently extracts action items using predefined heuristics.

Your task is to implement an **LLM-powered** alternative, `extract_action_items_llm()`, that utilizes Ollama to perform action item extraction via a large language model.

Some  tips:
- To produce structured outputs (i.e. JSON array of strings), refer to this documentation: https://ollama.com/blog/structured-outputs 
- To browse available Ollama models, refer to this documentation: https://ollama.com/library. Note that larger models will be more resource-intensive, so start small. To pull and run a model: `ollama run {MODEL_NAME}`

### TODO 2: Add Unit Tests 

Write unit tests for `extract_action_items_llm()` covering multiple inputs (e.g., bullet lists, keyword-prefixed lines, empty input) in `week2/tests/test_extract.py`.

### TODO 3: Refactor Existing Code for Clarity

Perform a refactor of the code in the backend, focusing in particular on well-defined API contracts/schemas, database layer cleanup, app lifecycle/configuration, error handling. 

### TODO 4: Use Agentic Mode to Automate Small Tasks

1. Integrate the LLM-powered extraction as a new endpoint. Update the frontend to include an "Extract LLM" button that, when clicked, triggers the extraction process via the new endpoint.

2. Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" button that, when clicked, fetches and displays them.

### TODO 5: Generate a README from the Codebase

***Learning Goal:***
*Students learn how AI can introspect a codebase and produce documentation automatically, showcasing Cursor’s ability to parse code context and translate it into human‑readable form.*

Use Cursor to analyze the current codebase and generate a well-structured `README.md` file. The README should include, at a minimum:
- A brief overview of the project
- How to set up and run the project
- API endpoints and functionality
- Instructions for running the test suite

## Deliverables
Fill out `week2/writeup.md` according to the instructions provided. Make sure all your changes are documented in your codebase. 

## Evaluation rubric (100 pts total)
- 20 points per part 1-5 (10 for the generated code and 10 for each prompt).