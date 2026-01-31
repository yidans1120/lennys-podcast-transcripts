#!/usr/bin/env python3
import os
import re
import json
import yaml

# The 33 episode folders as specified
episodes = [
    "adam-fishman",
    "archie-abrams", 
    "bangaly-kaba",
    "casey-winters",
    "christopher-miller",
    "deb-liu",
    "elena-verna-40",
    "meltem-kuran",
    "sachin-monga",
    "sri-batchu",
    "yuriy-timen",
    "austin-hay",
    "brian-balfour",
    "cam-adams",
    "crystal-w",
    "benjamin-lauzier",
    "brian-chesky",
    "dan-hockenmaier",
    "eli-schwartz",
    "emily-kramer",
    "gustaf-alstromer",
    "melissa-tan",
    "andy-raskin",
    "bill-carr",
    "bob-moesta",
    "carole-robin",
    "chip-huyen",
    "dalton-caldwell",
    "dylan-field",
    "gokul-rajaram",
    "sean-ellis",
    "shishir-mehrotra",
    "noah-weiss"
]

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except:
            return {}
    return {}

def extract_insights_from_transcript(content, guest_name, title):
    """Extract key growth insights from transcript content with context awareness"""
    
    # Remove frontmatter to get just transcript
    transcript = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Remove the intro/sponsor sections at the beginning
    # Find the main transcript start (usually after "Transcript" header)
    transcript_start = transcript.find("## Transcript")
    if transcript_start != -1:
        transcript = transcript[transcript_start:]
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', transcript)
    
    insights = []
    
    # Look for key insights - sentences that talk about actionable growth strategies
    insight_keywords = [
        ("retention", ["retention", "keep", "staying", "churn", "long-term value", "lifetime"]),
        ("activation", ["activation", "aha moment", "first value", "onboarding", "getting started", "first impression"]),
        ("acquisition", ["acquire", "growth loop", "viral", "word of mouth", "distribution", "reach", "go-to-market", "market fit"]),
        ("monetization", ["pricing", "revenue", "subscription", "freemium", "paid", "upsell", "economics"]),
        ("product strategy", ["product", "feature", "user experience", "build", "launch", "strategy"]),
        ("team/culture", ["hire", "team", "culture", "leadership", "people", "organize"]),
        ("experimentation", ["test", "experiment", "learn", "iterate", "hypothesis", "measure"]),
        ("scaling", ["scale", "grow", "expand", "leverage", "efficiency", "operations"]),
    ]
    
    prioritized_insights = []
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        
        # Filter for substantial sentences
        if len(sentence) < 40 or len(sentence) > 800:
            continue
        
        # Check if sentence contains growth-relevant content
        lower_sent = sentence.lower()
        
        # Count how many growth keywords this sentence contains
        keyword_score = 0
        categories = set()
        
        for category, keywords in insight_keywords:
            for keyword in keywords:
                if keyword in lower_sent:
                    keyword_score += 1
                    categories.add(category)
        
        # Sentences mentioning concrete frameworks, numbers, or strategies get bonus points
        if any(pattern in lower_sent for pattern in ["framework", "way to", "key to", "secret", "mistake", "lesson", "%", "should", "don't", "must", "important"]):
            keyword_score += 2
        
        if keyword_score >= 2 and len(categories) >= 1:
            prioritized_insights.append({
                'text': sentence,
                'score': keyword_score,
                'categories': list(categories)
            })
    
    # Sort by score and take top insights
    prioritized_insights.sort(key=lambda x: x['score'], reverse=True)
    
    # Extract unique insights
    seen = set()
    final_insights = []
    for item in prioritized_insights[:15]:  # Check top 15
        text = item['text'].strip()
        # Remove speaker labels and timestamps
        text = re.sub(r'^[A-Z][a-z]+\s*\([\d:]+\):\s*', '', text)
        text = re.sub(r'\s*\([\d:]+\)\s*', '', text)
        
        # Clean up excessive whitespace
        text = ' '.join(text.split())
        
        # Avoid duplicates
        text_sig = text[:100]
        if text_sig not in seen and len(text) > 40:
            final_insights.append(text)
            seen.add(text_sig)
        
        if len(final_insights) >= 5:
            break
    
    return final_insights if final_insights else ["No specific insights extracted from transcript"]


# Extract data from all episodes
results = []
base_path = "/Users/potatsfambly/Documents/python_home/episodes"

for episode in episodes:
    episode_path = os.path.join(base_path, episode, "transcript.md")
    
    if not os.path.exists(episode_path):
        print(f"⚠️  Missing: {episode}/transcript.md")
        continue
    
    try:
        with open(episode_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        frontmatter = extract_frontmatter(content)
        guest = frontmatter.get('guest', 'Unknown')
        title = frontmatter.get('title', 'Unknown')
        
        # Extract insights with more sophisticated analysis
        insights = extract_insights_from_transcript(content, guest, title)
        
        results.append({
            "guest": guest,
            "title": title,
            "insights": insights
        })
        
        print(f"✓ {episode}: {guest} - {len(insights)} insights")
        
    except Exception as e:
        print(f"✗ {episode}: {str(e)}")

# Save results to JSON
output_path = "/Users/potatsfambly/Documents/python_home/episodes_data.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✓ Extracted {len(results)} episodes with growth insights")
print(f"✓ Saved to {output_path}")

# Also print the JSON to stdout for verification
print("\n" + "="*80)
print("COMPLETE RESULTS:")
print("="*80)
print(json.dumps(results, indent=2, ensure_ascii=False))
