Using the PRD above, build Cuba Digest exactly as specified.

Follow this execution plan:

PHASE 1
* Create full project structure
* Create config files with sources
* Implement youtube_collector.py
* Implement news_collector.py
* Build main.py basic flow

PHASE 2
* Create HTML template with:
  - header
  - core del día
  - tabs (Temas, Medios, Videos, Trending, Cuba Global)
  - toggle for "cobertura estatal"
* Ensure tabs work with JavaScript

PHASE 3
* Implement filter logic
* Classify sources
* Generate summaries and insights (simple initial version)
* Populate all views

PHASE 4
* Implement topic clustering
* Generate core del día
* Implement trending logic
* Implement Cuba Global view
* Generate final HTML output

RULES:
* Do not deviate from PRD
* Do not add unnecessary complexity
* Do not implement transcript library
* Do not use database
* Do not use external APIs
* Keep system robust to missing data

VALIDATION:
* Run python3 main.py --mode digest
* Ensure HTML is generated
* Ensure tabs work
* Ensure toggle works
* Ensure links are present
* Ensure system does not crash if a source fails

Work step by step, but complete the full system.
