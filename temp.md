---
title: "InkSlate Developer Guide for Handwriting Analysis"
description: "Technical documentation for a Python handwriting analysis tool using Google Gemini multimodal API to generate graphology-based personality assessments from handwriting images."
author: "Anindita Basu"
project: "InkSlate"
version: "1.0"
language: "en"
audience: ["developers", "data-scientists", "python-engineers", "AI-hobbyists"]
topics:
  - handwriting analysis
  - graphology
  - personality assessment
  - Google Gemini API
  - multimodal AI
  - computer vision
  - prompt engineering
  - JSON schema enforcement
keywords:
  - handwriting personality analysis python
  - graphology AI
  - gemini multimodal handwriting analysis
  - personality detection handwriting
  - python gemini api example
  - multimodal ai prompt engineering
intent: "Provide developers with technical understanding, architecture overview, and extension points for the handwriting personality analysis system."
capabilities:
  - image-to-text multimodal inference
  - personality trait extraction
  - batch handwriting processing
  - longitudinal personality tracking
  - JSON-structured AI output
limitations:
  - graphology is not scientifically validated
  - outputs are for entertainment and reflection only
last_updated: "2025-12-28"
---

# InkSlate Developer Guide

---

InkSlate is a Python script that uses the Google Gemini API to analyse handwriting images and generate a personality profile that's based on graphology-inspired heuristics.

> **Disclaimer:**
> Graphology is **not scientifically validated**. InkSlate is for entertainment only.

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Functions](#functions)
	- [Essential functions](#essential-functions)
	- [Optional functions](#optional-functions)
- [Output](#output)
- [Limitations](#limitations)
- [Enhancements](#enhancements)
- [License](#license)

---

## Features

- Analyses a handwriting image and creates a detailed JSON personality report
- Pretty-prints results to the console
- Can do batch analysis for multiple images
- Detects changes over time
- Has a capability discovery mode (asks Gemini what traits it can assess)
- Automatically stores timestamped JSON analysis files

<div class="figure">
  <img src="{{ '/images/inkslate_developer.png' | relative_url }}" class="center-image" style="width:50%;">
  <div>&nbsp;</div>
</div>

## Requirements

- Python 3.9 or later.
- Python packages: `pip install google-generativeai pillow`.
- Google Gemini API key. The free tier is fine. With it, you can analyse up to 20 handwriting samples in a day, and process 5 samples in a minute (with a brief pause between batches).

## Setup

1. Get a Gemini API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
1. Clone the repository:
	```
	git clone https://github.com/AninditaBasu/inkslate.git
	cd inkslate
	```
1. Edit the script (`inkslate.py`) to specify the key: `GEMINI_API_KEY = "<your_Google_AI_API_key_goes_here>"`

## Functions

Some of these functions aren't called; they're there for extended use cases.

### Essential functions

- `setup_gemini(api_key, model_name="gemini-2.5-flash")`: Initialises the Gemini client and returns a GenerativeModel instance.
- `create_graphology_prompt() -> str`: Builds and returns the full structured prompt that's used for instructing Gemini about how to analyse handwriting. This function is the brain of InkSlate. It encodes the graphology rules to follow, the output constraints, and the required JSON schema. This is the function to modify if you need to add or delete any personality fields, change the wording that's printed in the report, tighten the output constraints, or experiment with different graphology heuristics. This function makes Gemini do the following things:
	- Evaluate specific handwriting parameters (slant, pressure, spacing, margins, baseline, letter forms, speed).
	- Map these visual cues to defined personality traits.
	- Return only valid JSON with a fixed set of keys, so that downstream parsing is reliable.
- `analyse_personality(image_path, model, save_results=True) -> Dict`: Runs the handwriting analysis on a single image.
	- Arguments: 
		- `image_path`: Path to the handwriting photo
		- `model`: Gemini model instance
		- `save_results`: Whether to write JSON to disk
	- Returns:
		- Python dictionary with personality data + metadata.
- `print_personality_results(results: Dict)`: Pretty-prints the analysis result to the terminal.

### Optional functions

- `create_comparison_report(file1, file2)`: Compares two JSON analysis files and highlights any changes in the defined traits. Useful for longitudinal tracking, and the trigger for creating InkSlate.
- `discover_analysis_capabilities(model)` : Asks Gemini which handwriting traits it is able to assess, and saves them in `model_capabilities_YYYYMMDD_HHMMSS.json`. Useful for creating the heuristic prompt.
- `batch_analyse(image_paths: list, model, output_dir="personality_reports")`: Processes multiple handwriting images and saves the reports in a folder. Useful for...well, not thought this out fully yet.

## Output

Each InkSlate run generates a file called `<image_name>_personality_analysis_YYYYMMDD_HHMMSS.json`. This is what the contents of the file can look like:

```
{
  "emotional_stability": "stable",
  "extraversion_introversion": "balanced",
  "confidence_level": "high",
  "attention_to_detail": "high",
  "openness_to_experience": "moderate",
  "conscientiousness": "very_high",
  "agreeableness": "moderate",
  "emotional_expressiveness": "moderate",
  "stress_level": "low",
  "communication_style": "assertive",
  "thinking_style": "analytical",
  "energy_level": "high",
  "social_orientation": "balanced",
  "decisiveness": "decisive",
  "optimism_pessimism": "realistic",
  "self_discipline": "very_high",
  "creativity": "moderate",
  "adaptability": "moderate",
  "leadership_qualities": "strong",
  "honesty_authenticity": "high",
  "key_observations": "...",
  "personality_summary": "...",
  "strengths": ["..."],
  "potential_challenges": ["..."],
  "recommended_careers": ["..."],
  "interpersonal_style": "...",
  "work_style": "...",
  "stress_indicators": "...",
  "confidence_assessment": "high",
  "timestamp": "2025-01-01T13:45:00",
  "image_path": "IMG_2375.JPEG",
  "analysis_type": "graphology"
}
```

## Limitations

- Gemini can occasionally return malformed JSON.
- Graphology has no scientific backing.
- API usage is subject to Gemini rate limits.

## Enhancements

- CLI arguments instead of `input()`, so that automation, scripting, and scheduled runs are easier.
- HTML report generator, for prettiness and user friendlyness.
- Timeline visualisation of changes, for UX purposes.
- Encryption of stored personality files, because the `.json` files can be interpreted as ones containing sensitive data.
- Time-lapsed, reminder-based tracking app for motor conditions such as Parkinson's, which was the trigger for creating InkSlate.

---

## License

MIT

