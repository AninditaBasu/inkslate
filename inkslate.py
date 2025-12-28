"""
Graphology Analysis Script for Personality Assessment
Uses Google Gemini API to analyse handwriting samples for personality traits
and psychological characteristics.

DISCLAIMER: Graphology is not a scientifically validated method for personality
assessment. This tool is for entertainment purposes only.
"""

import google.generativeai as genai
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import PIL.Image

# Current local date and time as a datetime object
now = datetime.now()

# Configuration
GEMINI_API_KEY = "<your_Google_AI_API_key_goes_here>"


def setup_gemini(api_key: str, model_name: str = "gemini-2.5-flash"):
    """Initialise Gemini API with the API key.

    Args:
        api_key: Your Gemini API key
        model_name: Model to use (default: gemini-2.5-flash, which is free-tier compatible)
    """
    genai.configure(api_key=api_key)
    print(f"[INFO] Using the `{model_name}` model\n")
    return genai.GenerativeModel(model_name)


def create_graphology_prompt() -> str:
    """Create the detailed prompt for graphology analysis."""
    prompt = """You are an expert graphologist specializing in personality analysis through handwriting. Analyze this handwriting sample to assess personality traits and psychological characteristics.

Please evaluate the following parameters and provide your assessment in valid JSON format ONLY (no Markdown, no additional text):

{
  "emotional_stability": "very_stable|stable|moderate|unstable|very_unstable",
  "extraversion_introversion": "very_extraverted|extraverted|balanced|introverted|very_introverted",
  "confidence_level": "very_high|high|moderate|low|very_low",
  "attention_to_detail": "very_high|high|moderate|low|very_low",
  "openness_to_experience": "very_high|high|moderate|low|very_low",
  "conscientiousness": "very_high|high|moderate|low|very_low",
  "agreeableness": "very_high|high|moderate|low|very_low",
  "emotional_expressiveness": "very_expressive|expressive|moderate|reserved|very_reserved",
  "stress_level": "very_low|low|moderate|high|very_high",
  "communication_style": "direct|assertive|balanced|diplomatic|cautious",
  "thinking_style": "analytical|logical|balanced|intuitive|creative",
  "energy_level": "very_high|high|moderate|low|very_low",
  "social_orientation": "highly_social|social|balanced|selective|solitary",
  "decisiveness": "very_decisive|decisive|moderate|hesitant|very_hesitant",
  "optimism_pessimism": "very_optimistic|optimistic|realistic|pessimistic|very_pessimistic",
  "self_discipline": "very_high|high|moderate|low|very_low",
  "creativity": "very_high|high|moderate|low|very_low",
  "adaptability": "very_adaptable|adaptable|moderate|rigid|very_rigid",
  "leadership_qualities": "very_strong|strong|moderate|weak|very_weak",
  "honesty_authenticity": "very_high|high|moderate|low|very_low",
  "key_observations": "Detailed observations about the handwriting characteristics",
  "personality_summary": "A comprehensive 2-3 paragraph personality profile",
  "strengths": ["List of 3-5 key personality strengths"],
  "potential_challenges": ["List of 3-5 areas for personal development"],
  "recommended_careers": ["List of 3-5 career types that may suit this personality"],
  "interpersonal_style": "Description of how this person likely interacts with others",
  "work_style": "Description of how this person likely approaches work and tasks",
  "stress_indicators": "Any signs of current stress or emotional state",
  "confidence_assessment": "low|medium|high"
}

Graphology Analysis Guidelines - Use these specific traits:

1. SLANT (angle of writing)
   - Right slant: Emotionally expressive, outgoing, future-oriented
   - Vertical: Balanced, controlled emotions, logical
   - Left slant: Reserved, introspective, cautious with emotions

2. PRESSURE (darkness/depth of strokes)
   - Heavy pressure: Strong emotions, intensity, commitment, high energy
   - Light pressure: Sensitive, adaptable, less aggressive, spiritual
   - Variable pressure: Emotional complexity, mood variations

3. SIZE (height of letters)
   - Large: Outgoing, confident, needs attention, thinks big picture
   - Small: Detail-oriented, introverted, analytical, focused
   - Medium: Well-adjusted, adaptable

4. SPACING
   - Between letters: Mental clarity and organization
   - Between words: Social boundaries and need for personal space
   - Between lines: Ability to organize thoughts and plans

5. MARGINS
   - Left margin: Relationship with past (wide = moving away from past)
   - Right margin: Relationship with future (wide = fear of unknown)
   - Top/bottom: Respect for boundaries, formality

6. BASELINE (line direction)
   - Upward: Optimistic, ambitious, positive outlook
   - Straight: Stable, disciplined, consistent
   - Downward: Tired, pessimistic, or realistic

7. LETTER FORMATIONS
   - Open letters (a, o, e): Honest, talkative, open communication
   - Closed letters: Private, selective in sharing
   - Angular: Analytical, logical, decisive
   - Rounded: Creative, artistic, empathetic

8. SPEED INDICATORS
   - Connected letters: Logical, systematic thinking
   - Disconnected letters: Intuitive, spontaneous
   - Simplified forms: Intelligent, efficient

Analyze ALL these aspects and integrate them into your personality assessment.

Respond ONLY with the JSON object, no other text or Markdown."""

    return prompt


def analyse_personality(image_path: str, model, save_results: bool = True) -> Dict:
    """
    Analyse a handwriting sample for personality traits.

    Args:
        image_path: Path to the handwriting image
        model: Initialised Gemini model
        save_results: Whether to save results to a JSON file

    Returns:
        Dictionary containing personality analysis results
    """
    try:
        # Load the image
        img = PIL.Image.open(image_path)

        # Create the prompt
        prompt = create_graphology_prompt()

        # Generate analysis
        print(f"[INFO] Analysing the handwriting in `{image_path}`")
        print("[INFO] This might take a while...\n")

        response = model.generate_content([prompt, img])

        # Parse the response
        response_text = response.text.strip()

        # Remove Markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        # Parse JSON
        analysis_results = json.loads(response_text)

        # Add metadata
        analysis_results["timestamp"] = datetime.now().isoformat()
        analysis_results["image_path"] = str(image_path)
        analysis_results["analysis_type"] = "graphology"

        # Save the results
        if save_results:
            output_path = Path(image_path).stem + f"_personality_analysis_{now.strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_path, "w") as f:
                json.dump(analysis_results, f, indent=2)
            print(f"[INFO] Results saved to `{output_path}`\n")

        return analysis_results

    except json.JSONDecodeError as e:
        print(f"[ERROR] Error parsing JSON response: {e}")
        print(f"[ERROR] Raw response: {response.text}")
        return {"error": "Failed to parse response", "raw_response": response.text}
    except Exception as e:
        print(f"[ERROR] Error during analysis: {e}")
        return {"error": str(e)}


def print_personality_results(results: Dict):
    """Print personality analysis results in a readable format."""
    if "error" in results:
        print(f"[ERROR] Error: {results['error']}")
        return

    print("=" * 70)
    print("PERSONALITY ANALYSIS")
    print("=" * 70)
    print(f"Timestamp: {results.get('timestamp', 'N/A')}")
    print(f"Image: {results.get('image_path', 'N/A')}")
    print(f"Confidence: {results.get('confidence_assessment', 'N/A').upper()}")
    print("=" * 70)

    # Personality summary
    print("\nSUMMARY")
    print("-" * 70)
    print(results.get('personality_summary', 'N/A'))

    # Core traits
    print("\n\nCORE TRAITS")
    print("-" * 70)

    core_traits = [
        ("Emotional Stability", "emotional_stability"),
        ("Extraversion/Introversion", "extraversion_introversion"),
        ("Confidence Level", "confidence_level"),
        ("Attention to Detail", "attention_to_detail"),
        ("Openness to Experience", "openness_to_experience"),
        ("Conscientiousness", "conscientiousness"),
        ("Agreeableness", "agreeableness"),
    ]

    for label, key in core_traits:
        value = results.get(key, "N/A").replace("_", " ").title()
        print(f"{label:.<35} {value}")

    # Additional characteristics
    print("\n\nADDITIONAL CHARACTERISTICS")
    print("-" * 70)

    additional_traits = [
        ("Emotional Expressiveness", "emotional_expressiveness"),
        ("Stress Level", "stress_level"),
        ("Communication Style", "communication_style"),
        ("Thinking Style", "thinking_style"),
        ("Energy Level", "energy_level"),
        ("Social Orientation", "social_orientation"),
        ("Decisiveness", "decisiveness"),
        ("Optimism/Pessimism", "optimism_pessimism"),
        ("Self-Discipline", "self_discipline"),
        ("Creativity", "creativity"),
        ("Adaptability", "adaptability"),
        ("Leadership Qualities", "leadership_qualities"),
        ("Honesty/Authenticity", "honesty_authenticity"),
    ]

    for label, key in additional_traits:
        value = results.get(key, 'N/A').replace('_', ' ').title()
        print(f"{label:.<35} {value}")

    # Strengths
    print("\n\nSTRENGTHS")
    print("-" * 70)
    strengths = results.get('strengths', [])
    for i, strength in enumerate(strengths, 1):
        print(f"{i}. {strength}")

    # Potential challenges
    print("\n\nWEAKNESSES")
    print("-" * 70)
    challenges = results.get('potential_challenges', [])
    for i, challenge in enumerate(challenges, 1):
        print(f"{i}. {challenge}")

    # Career recommendations
    print("\n\nRECOMMENDED CAREER PATHS")
    print('-' * 70)
    careers = results.get('recommended_careers', [])
    for i, career in enumerate(careers, 1):
        print(f"{i}. {career}")

    # Interpersonal style
    print("\n\nINTERPERSONAL STYLE")
    print("-" * 70)
    print(results.get('interpersonal_style', 'N/A'))

    # Work style
    print("\n\nWORK STYLE")
    print("-" * 70)
    print(results.get("work_style", "N/A"))

    # Stress indicators
    stress_indicators = results.get("stress_indicators", "None detected")
    if stress_indicators and stress_indicators.lower() != 'none' and stress_indicators.lower() != "none detected":
        print("\n\nCURRENT STRESS INDICATORS")
        print("-" * 70)
        print(stress_indicators)

    # Key observations
    print("\n\nOBSERVATIONS")
    print("-" * 70)
    print(results.get("key_observations", "N/A"))

    print("\n" + "=" * 70)
    print("\nDISCLAIMER: This analysis has no proven scientific basis.")
    print("It is for entertainment only.")
    print("Take it with a pinch of salt.")
    print("=" * 70)


def create_comparison_report(file1: str, file2: str, compare_all: bool = False):
    """Compare two personality analyses (useful for tracking changes over time).
    
    Args:
        file1: Path to first analysis JSON file
        file2: Path to second analysis JSON file
        compare_all: If True, compare all traits. If False, compare key traits only.
    """
    try:
        with open(file1, 'r') as f:
            analysis1 = json.load(f)
        with open(file2, 'r') as f:
            analysis2 = json.load(f)
        
        print("\n" + "=" * 70)
        print("PERSONALITY COMPARISON REPORT")
        print("=" * 70)
        print(f"Analysis 1: {analysis1.get('timestamp', 'N/A')}")
        print(f"Analysis 2: {analysis2.get('timestamp', 'N/A')}")
        print("-" * 70)
        
        if compare_all:
            # Compare all personality traits
            traits_to_compare = [
                "emotional_stability", "extraversion_introversion", "confidence_level",
                "attention_to_detail", "openness_to_experience", "conscientiousness",
                "agreeableness", "emotional_expressiveness", "stress_level",
                "communication_style", "thinking_style", "energy_level",
                "social_orientation", "decisiveness", "optimism_pessimism",
                "self_discipline", "creativity", "adaptability",
                "leadership_qualities", "honesty_authenticity"
            ]
            print("\nCOMPLETE TRAIT COMPARISON:\n")
        else:
            # Compare key traits most relevant for longitudinal tracking
            traits_to_compare = [
                "emotional_stability", "extraversion_introversion", "confidence_level",
                "stress_level", "optimism_pessimism", "energy_level"
            ]
            print("\nKEY TRAIT CHANGES (use compare_all=True for full comparison):\n")
        
        changes_detected = False
        unchanged_count = 0
        
        for trait in traits_to_compare:
            val1 = analysis1.get(trait, "N/A")
            val2 = analysis2.get(trait, "N/A")
            
            if val1 != val2:
                changes_detected = True
                label = trait.replace("_", " ").title()
                print(f"  {label}:")
                print(f"   {val1.replace('_', ' ').title()} → {val2.replace('_', ' ').title()}")
                print()
            else:
                unchanged_count += 1
        
        if not changes_detected:
            print("  No changes detected in tracked personality traits.")
        else:
            print(f"\nSummary: {len(traits_to_compare) - unchanged_count} traits changed, {unchanged_count} unchanged")
        
        # Compare strengths and challenges
        print("\n" + "-" * 70)
        print("STRENGTHS COMPARISON:")
        strengths1 = set(analysis1.get('strengths', []))
        strengths2 = set(analysis2.get('strengths', []))
        
        new_strengths = strengths2 - strengths1
        lost_strengths = strengths1 - strengths2
        
        if new_strengths:
            print("\n  New strengths identified:")
            for s in new_strengths:
                print(f"   + {s}")
        
        if lost_strengths:
            print("\n   Previously identified strengths not spotted today:")
            for s in lost_strengths:
                print(f"   - {s}")
        
        if not new_strengths and not lost_strengths:
            print("  Strengths profile remains consistent")
        
        print("\n" + "-" * 70)
        print("STRESS INDICATORS COMPARISON:")
        stress1 = analysis1.get('stress_indicators', 'None detected')
        stress2 = analysis2.get('stress_indicators', 'None detected')
        
        print(f"\nPrevious: {stress1}")
        print(f"Current:  {stress2}")
        
        if stress1 != stress2:
            if "none" in stress2.lower():
                print("\n  Stress indicators have decreased")
            elif "none" in stress1.lower():
                print("\n  New stress indicators detected")
            else:
                print("\n  Stress patterns have changed")
        
        print("\n" + "=" * 70)
        
    except FileNotFoundError as e:
        print(f"[ERROR] Error: Could not find file: {e}")
    except Exception as e:
        print(f"[ERROR] Error comparing the analysis reports: {e}")


def discover_analysis_capabilities(model):
    """Ask the AI what parameters it can reliably analyse from handwriting."""
    prompt = """You are an expert graphologist. List all the personality traits, psychological characteristics, 
    and behavioral indicators that can be reliably assessed through handwriting analysis according to 
    graphology principles.

    For each trait, indicate:
    1. The trait name
    2. What handwriting features reveal it
    3. Reliability level (high/medium/low)

    Respond ONLY with valid JSON, no other text or markdown:
    {
      "traits": [
        {
          "name": "trait name",
          "indicators": "what handwriting features show this",
          "reliability": "high|medium|low"
        }
      ]
    }"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        print("=" * 70)
        print("GRAPHOLOGY ANALYSIS CAPABILITIES")
        print("=" * 70)
        print(response_text)
        print("=" * 70)

        # Remove Markdown code blocks if present
        if "```json" in response_text:
            # Extract content between ```json and ```
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        elif "```" in response_text:
            # Extract content between ``` and ```
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()

        # Try to find JSON object if there is extra text
        if not response_text.startswith("{"):
            # Find first { and last }
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end != 0:
                response_text = response_text[start:end]

        # Parse JSON
        capabilities = json.loads(response_text)

        # Save to file
        with open(f"model_capabilities_{now.strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(capabilities, f, indent=2)
        print(f"\n[INFO] Model capabilities saved as `model_capabilities_{now.strftime('%Y%m%d_%H%M%S')}.json`")

        return capabilities

    except json.JSONDecodeError as e:
        print(f"\n[ERROR] JSON parsing error: {e}")
        print(f"[ERROR] Saving raw response to `model_capabilities_raw_{now.strftime('%Y%m%d_%H%M%S')}.txt`")
        with open(f"model_capabilities_raw_{now.strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
            f.write(response.text)
        print("[ERROR] Raw JSON response saved for model capabilities; needs manual inspection")
        return None
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        return None

def batch_analyse(image_paths: list, model, output_dir: str = 'personality_reports'):
    """Analyse multiple handwriting samples in batch."""
    Path(output_dir).mkdir(exist_ok=True)
    results = []

    print(f"\n[INFO] Batch analysing {len(image_paths)} samples...\n")

    for i, image_path in enumerate(image_paths, 1):
        print(f"[INFO] [{i}/{len(image_paths)}] Processing: {image_path}")
        result = analyse_personality(image_path, model, save_results=False)

        if "error" not in result:
            # Save to output directory
            filename = Path(image_path).stem + f"_personality_{now.strftime('%Y%m%d_%H%M%S')}.json"
            output_path = Path(output_dir) / filename
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"   [INFO] Saved to `{output_path}`\n")
        else:
            print(f"   [ERROR] Error: {result.get('error')}\n")

        results.append(result)

    print(f"[INFO] Batch analysis complete. Results saved to `{output_dir}/` directory")
    return results


# Main
if __name__ == '__main__':
    print("\n[INPUT] A photo of your handwriting is needed:")
    print("       • Use clear, natural handwriting samples (not printed text)")
    print("       • Ensure that it contains at least 3 or 4 sentences")

    # User input for image
    image_path = input("Enter the full path to the image file, for example, `C:/data/handwriting_sample.jpg`: ")  # Replace with your image path

    # Check if API key is set
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("[ACTION NEEDED] Please set your Gemini API key in the script")
        print("[ACTION NEEDED] Get your free API key at: https://aistudio.google.com/app/apikey")
        exit(1)

    # Initialise Gemini with Flash model (free-tier compatible)
    model = setup_gemini(GEMINI_API_KEY, model_name="gemini-2.5-flash")

    # Optional: Discover what the model can analyse
    # print(f"[INFO] \nDiscovering the analysis capabilities of `{model}`...")
    # discover_analysis_capabilities(model)

    # Single analysis
    results = analyse_personality(image_path, model, save_results=True)
    print_personality_results(results)

    # Optional: Batch analysis
    # batch_image_paths = ["sample1.jpg", "sample2.jpg", "sample3.jpg"]
    # batch_analyse(batch_image_paths, model)

    # Optional: Compare two analysis reports
    # create_comparison_report("analysis1_personality.json", "analysis2_personality.json")
    # create_comparison_report("analysis1_personality.json", "analysis2_personality.json", compare_all=True)

