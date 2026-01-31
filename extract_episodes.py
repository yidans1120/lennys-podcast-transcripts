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

def extract_insights_from_transcript(content):
    """Extract key growth insights from transcript content"""
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Lowercase for searching
    lower_content = content.lower()
    
    insights = []
    
    # Common growth insight keywords/patterns
    patterns = {
        "retention": ["retention", "churn", "staying power", "keeping users"],
        "activation": ["activation", "aha moment", "first value", "onboarding"],
        "monetization": ["pricing", "monetization", "revenue model", "subscription", "freemium"],
        "acquisition": ["acquisition", "growth loop", "viral", "word of mouth", "distribution"],
        "experimentation": ["experiment", "test", "hypothesis", "iteration", "learnings"],
        "product": ["product-market fit", "product strategy", "feature", "user experience"],
        "team": ["hiring", "team building", "culture", "leadership", "people"],
        "strategy": ["strategy", "positioning", "market", "competitive", "go-to-market"],
        "scaling": ["scaling", "growth hacks", "leverage", "operational", "efficiency"]
    }
    
    # Extract key sentences that contain growth insights
    sentences = re.split(r'[.!?]+', content)
    
    key_insights_found = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 30:
            continue
        
        # Check for multiple growth-related keywords
        keyword_count = 0
        for keyword in ["growth", "retention", "acquisition", "activation", "product", "market", "scale", "strategy", "experimentation", "customer", "user"]:
            if keyword in sentence.lower():
                keyword_count += 1
        
        if keyword_count >= 2 and len(sentence) > 50 and len(sentence) < 500:
            key_insights_found.append(sentence)
    
    return key_insights_found[:5]  # Return top 5

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
        
        # Extract insights
        insights = extract_insights_from_transcript(content)
        
        results.append({
            "guest": guest,
            "title": title,
            "insights": insights if insights else ["Episode content available but insights require manual review"]
        })
        
        print(f"✓ {episode}: {guest}")
        
    except Exception as e:
        print(f"✗ {episode}: {str(e)}")

# Save results to JSON
output_path = "/Users/potatsfambly/Documents/python_home/episodes_data.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✓ Extracted {len(results)} episodes")
print(f"✓ Saved to {output_path}")
