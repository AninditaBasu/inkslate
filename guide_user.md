---
title: "InkSlate User Guide for Handwriting Analysis"
description: "Step-by-step beginner guide for analysing handwriting with AI to generate personality insights using a Python script and a free Google Gemini API key."
author: "Anindita Basu"
project: "InkSlate"
version: "1.0"
language: "en"
audience: ["general-users", "self-reflection", "journaling", "personal-growth"]
topics:
  - handwriting analysis
  - self-reflection
  - personality insights
  - AI tools for beginners
  - journaling automation
keywords:
  - handwriting personality test ai
  - graphology handwriting analysis tool
  - handwriting personality software
  - self reflection handwriting analysis
  - ai handwriting personality
intent: "Help non-technical users safely run the tool, interpret results, and track personal changes over time for reflection."
safety_notes:
  - not a medical or psychological diagnostic tool
  - not scientifically validated
  - use for entertainment and awareness only
features:
  - one-time handwriting analysis
  - monthly personality reflection
  - progress comparison reports
  - trend tracking over time
last_updated: "2025-12-28"
---

# InkSlate User Guide

---

InkSlate is a personality analyser.

It looks at an image of your handwriting and creates a personality profile for fun. It is meant for self-reflection and curiosity, **not** diagnosis.

- [What you need](#what-you-need)
- [Steps](#steps)
- [What next](#what-next)
- [Disclaimer](#disclaimer)

---

## What you need

- A computer with Python 3.9 or later.
- A clear photo of your handwriting.
- A Gemini API key from Google. Get your free key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

## Steps

1. Create a handwriting sample. Write 3 or 4 sentences on paper. Then, take a clear photo of the writing, and save it on your computer.
1. Make the `inkslate.py` script ready for use.
	1. Assuming that Python is installed on your computer, open the command prompt and type `pip install google-generativeai pillow`. Wait for the Python libraries to be downloaded and installed.
	1. Download the `inkslate.py` file from the [GitHub repository](https://github.com/AninditaBasu/inkslate/blob/9e645b68eef6a657b6fda1adb767c14a0ee72664/inkslate.py). Openthe file in any text editor and find this line near the top: `GEMINI_API_KEY = "<your_Google_AI_API_key_goes_here>"`. Paste your API key between the quotes. Save the file.
1. Run InkSlate by returning to the command prompt and typing the following command: `python inkslate.py`. When prompted, enter the full path to the image file you created in a previous step. It might take a while for the analysis to be done, after which the result is displayed on the terminal. A time-stamped result file (in `.json` format) is saved in the same folder as the image file.

<div class="figure">
  <img src="{{ '/images/inkslate_user.png' | relative_url }}" class="center-image" style="width:40%;">
  <div>&nbsp;</div>
</div>

The result can contain phrases such as these:

- Emotional stability
- Confidence level
- Stress level
- Strengths
- Weaknesses

Treat these as conversation starters with yourself, not hard facts. After all, InkSlate is a fun tool, not a medical doctor.

Have fun!

## What next

You can repeat this process weekly, monthly, or as frequently as you want to, by supplying a handwriting sample of that day. You're limited only by the free limits of your API key. Every time, a time-stamped file is created with the results. 

Changes in handwriting can sometimes reflect changes in fine motor control, fatigue, or stress levels. When you're writing by hand, several pieces of your body interact with each other: your brain, nervous system, muscles, vision, and posture. Changes in any of these systems can alter the slant, pressure, spacing, or consistency in your writing. Besides, your writing is also affected by medication or injury. A single analysis means very little, but consistent changes across many samples over weeks or months could be worth paying attention to. If you notice strong or persistent handwriting changes, together with the following real-world symptoms, it might make sense to seek professional medical help:

- Frequent hand tremors
- Loss of coordination
- Numbness or weakness
- Unexplained fatigue

> **Remember:**
>You are the expert on your own body. InkSlate can only highlight some patterns, and that too with artificial Gemini intelligence (and we all know what kind of a trickster Gemini's owner, Mercury, is in real mythology). It is you who knows best when something feels different enough to investigate further.

To compare two pieces of writing programmatically:

1. Open `inkslate.py` in any text editor and uncomment the following line:`create_comparison_report("analysis1_personality.json", "analysis2_personality.json")`.
1. Replace the two file names with that of the two reports that you want to compare.
1. Run `inkslate.py`. It displays the key changes.

---

## Disclaimer

This program is for entertainment only. It does not diagnose any personality or health conditions.

