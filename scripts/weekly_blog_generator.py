#!/usr/bin/env python3
"""
Weekly Blog Post Generator for cyborgbusinessconsultant.com
Uses Ollama qwen3:8b to generate SEO-optimized blog posts
Author: Francesco Rosso Zingone
Version: 2.0 - Ottimizzato per 600 parole e contenuti concreti
"""

import subprocess
import json
import os
import sys
from datetime import datetime
import re
import random

# Configuration
BLOG_DIR = "/Users/zingo/Documents/SITI_WEB/cyborgbusinessconsultant-site/content/blog"
SITE_DIR = "/Users/zingo/Documents/SITI_WEB/cyborgbusinessconsultant-site"
OLLAMA_MODEL = "qwen3:8b"

# Topic pool for variety - più specifici e concreti
TOPICS = [
    "AI automation tools transforming small business operations",
    "How ChatGPT and AI assistants are revolutionizing customer service",
    "Marketing automation with AI: ROI measurement and implementation",
    "AI-driven financial analysis for better business decisions", 
    "Supply chain optimization using artificial intelligence",
    "Predictive analytics for inventory management and cost reduction",
    "AI tools for competitive analysis and market research",
    "Implementing AI chatbots for lead generation and conversion",
    "Machine learning applications in e-commerce personalization",
    "AI-powered content creation strategies for digital marketing"
]

# Internal links pool - più specifici
INTERNAL_LINKS = [
    ("/about", "Francesco Rosso Zingone's AI-integrated methodology"),
    ("/contact", "Discovery Day consultation"),
    ("/manifesto", "Cyborg Business Consultant approach"),
    ("/evolution", "Business Evolution Program")
]

# External links pool organizzati per topic
EXTERNAL_SOURCES_BY_TOPIC = {
    "marketing": [
        ("https://hbr.org/", "Harvard Business Review", "According to Harvard Business Review research"),
        ("https://www.mckinsey.com/", "McKinsey Global Institute", "McKinsey studies show that"),
        ("https://www.pwc.com/", "PwC Research", "PwC analysis reveals")
    ],
    "operations": [
        ("https://www.mckinsey.com/", "McKinsey Global Institute", "McKinsey research demonstrates"),
        ("https://www.accenture.com/", "Accenture Strategy", "Accenture findings indicate"),
        ("https://www.deloitte.com/", "Deloitte Insights", "Deloitte studies confirm")
    ],
    "technology": [
        ("https://www.accenture.com/", "Accenture Strategy", "Accenture technology research shows"),
        ("https://www.pwc.com/", "PwC Research", "PwC digital transformation studies reveal"),
        ("https://www.bcg.com/", "Boston Consulting Group", "BCG technology analysis indicates")
    ],
    "finance": [
        ("https://www.mckinsey.com/", "McKinsey Global Institute", "McKinsey financial analysis shows"),
        ("https://www.pwc.com/", "PwC Research", "PwC financial services research reveals"),
        ("https://www.deloitte.com/", "Deloitte Insights", "Deloitte financial studies demonstrate")
    ],
    "strategy": [
        ("https://www.bcg.com/", "Boston Consulting Group", "Boston Consulting Group research shows"),
        ("https://hbr.org/", "Harvard Business Review", "Harvard Business Review analysis reveals"),
        ("https://www.mckinsey.com/", "McKinsey Global Institute", "McKinsey strategic research demonstrates")
    ]
}

def select_external_source(topic):
    """Seleziona fonte esterna appropriata basata sul topic"""
    
    # Determina categoria del topic
    topic_lower = topic.lower()
    
    if any(word in topic_lower for word in ["marketing", "customer", "lead", "conversion", "content"]):
        category = "marketing"
    elif any(word in topic_lower for word in ["operations", "supply", "inventory", "automation", "process"]):
        category = "operations"
    elif any(word in topic_lower for word in ["ai", "technology", "chatbot", "machine learning", "digital"]):
        category = "technology"
    elif any(word in topic_lower for word in ["financial", "finance", "cost", "roi", "budget"]):
        category = "finance"
    else:
        category = "strategy"
    
    # Seleziona fonte casuale dalla categoria appropriata
    return random.choice(EXTERNAL_SOURCES_BY_TOPIC[category])

def generate_prompt(topic):
    """Generate optimized prompt for qwen3:8b - versione ottimizzata"""
    
    # Seleziona link casuali
    internal_link = random.choice(INTERNAL_LINKS)
    external_url, external_name, external_phrase = select_external_source(topic)
    
    prompt = f"""You are Francesco Rosso Zingone, Italy's first Cyborg Business Consultant with 25+ years of experience. Write a professional blog post for cyborgbusinessconsultant.com.

TOPIC: "{topic}"

REQUIREMENTS:
- Exactly 600 words
- Perfect English
- Professional, authoritative tone (NO sci-fi language)
- Include Hugo front matter with complete SEO fields
- MANDATORY: Include external link in ROI section
- MANDATORY: Include internal link in call to action
- Focus on practical business applications and measurable results

STRUCTURE REQUIRED:
```
---
title: "Compelling Title with Main Keyword (under 60 chars)"
description: "SEO meta description 150-160 chars with primary keyword"
date: {datetime.now().strftime('%Y-%m-%d')}
tags: ["AI-business", "digital-transformation", "business-automation"]
categories: ["Business Strategy", "AI Applications"]
keywords: ["AI business consulting", "Francesco Rosso Zingone", "business automation", "digital transformation"]
---

# Compelling Headline (H1)

**Strong opening sentence that hooks the reader with a concrete benefit or statistic.**

Brief introduction paragraph establishing the problem/opportunity and your 25+ years of authority.

## Practical Applications (H2)
Concrete examples with specific tools (ChatGPT, automation platforms, etc.) and realistic metrics (efficiency gains, cost savings percentages).

## Implementation Strategy (H2)  
Step-by-step approach for businesses to adopt these AI solutions, including budget considerations and timeline.

## ROI and Competitive Advantage (H2)
Measurable benefits with specific examples. 
MANDATORY: Include this EXACT external link: "{external_phrase} that [{external_name}]({external_url}) companies using AI achieve 25-40% efficiency gains."

## Key Takeaways
- Bullet point 1 with actionable insight
- Bullet point 2 with practical tip  
- Bullet point 3 with implementation advice

---

**Ready to implement AI solutions in your business? [Book a Discovery Day]({internal_link[0]}).**

*Francesco Rosso Zingone - Italy's First Cyborg Business Consultant*
```

CONTENT GUIDELINES:
- Reference your 25+ years of experience naturally in introduction
- Mention "AI-integrated consulting methodology" and "fractional CMO" organically
- Include specific metrics: efficiency gains (20-40%), cost reductions (15-30%), time savings
- Use terms like "measurable results", "competitive advantage", "proven methodologies"
- Avoid sci-fi terms: no "transcend", "evolve", "post-human", "species"
- Focus on: automation, optimization, data-driven decisions, ROI, scalability
- Keep tone professional but accessible - business executive level

SEO KEYWORDS TO INTEGRATE NATURALLY:
- AI business consulting (primary)
- Business automation
- Digital transformation  
- Francesco Rosso Zingone
- Fractional CMO
- Competitive advantage
- AI tools
- Business intelligence

Write the complete 600-word blog post following the exact structure above. Count words carefully to hit exactly 600."""

    return prompt

def call_ollama(prompt):
    """Call Ollama with qwen3:8b model - versione ottimizzata"""
    try:
        print("🤖 Calling Ollama qwen3:8b...")
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ Ollama error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("⏰ Ollama call timed out")
        return None
    except Exception as e:
        print(f"❌ Error calling Ollama: {e}")
        return None

def validate_content(content):
    """Validate generated content for quality and requirements"""
    
    issues = []
    
    # Check for Hugo front matter
    if not content.startswith('---'):
        issues.append("Missing Hugo front matter")
    
    # Check for required sections
    required_sections = ['title:', 'description:', 'date:', 'tags:', 'categories:', 'keywords:']
    for section in required_sections:
        if section not in content:
            issues.append(f"Missing {section} in front matter")
    
    # Check word count (approximate)
    words = len(content.split())
    if words < 550 or words > 650:
        issues.append(f"Word count {words} outside target range (550-650)")
    
    # Check for internal and external links
    if 'Book a Discovery Day' not in content or '](' not in content:
        issues.append("Missing internal link")
    
    if 'https://' not in content or '](' not in content:
        issues.append("Missing external link")
    
    return issues

def create_filename(content):
    """Create SEO-friendly filename from title"""
    
    # Extract title from content
    lines = content.split('\n')
    title_line = next((line for line in lines if line.startswith('title:')), None)
    
    if title_line:
        # Extract title from YAML front matter
        title = title_line.replace('title:', '').strip().strip('"').strip("'")
        # Remove special characters and create slug
        slug = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        slug = re.sub(r'\s+', '-', slug.strip())
        slug = slug.lower()[:50]  # Limit length
    else:
        slug = f"ai-business-insights-{datetime.now().strftime('%m-%d')}"
    
    # Add date prefix
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"{date_str}-{slug}.md"

def save_post(content, filename):
    """Save blog post to content/blog directory"""
    filepath = os.path.join(BLOG_DIR, filename)
    
    try:
        # Ensure directory exists
        os.makedirs(BLOG_DIR, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Blog post saved: {filepath}")
        return True, filepath
    except Exception as e:
        print(f"❌ Error saving post: {e}")
        return False, None

def git_commit_and_push():
    """Commit and push changes to repository"""
    try:
        # Change to site directory
        os.chdir(SITE_DIR)
        
        print("📝 Committing to Git...")
        
        # Git commands
        subprocess.run(["git", "add", "."], check=True)
        
        commit_msg = f"Auto-generated weekly blog post - {datetime.now().strftime('%Y-%m-%d')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        print("🚀 Pushing to repository...")
        subprocess.run(["git", "push"], check=True)
        
        print("✅ Successfully published to repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

def main():
    """Main execution function"""
    print("🤖 Starting weekly blog post generation for cyborgbusinessconsultant.com")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: 600 words, SEO optimized, business-focused")
    
    # Select random topic
    topic = random.choice(TOPICS)
    print(f"📝 Selected topic: {topic}")
    
    # Generate prompt
    prompt = generate_prompt(topic)
    
    # Call Ollama
    content = call_ollama(prompt)
    
    if not content:
        print("❌ Failed to generate content")
        sys.exit(1)
    
    print("✅ Content generated successfully")
    
    # Validate content
    issues = validate_content(content)
    if issues:
        print("⚠️ Content validation issues:")
        for issue in issues:
            print(f"   • {issue}")
        
        # Continue anyway but note issues
        print("📝 Proceeding with generated content...")
    else:
        print("✅ Content validation passed")
    
    # Create filename
    filename = create_filename(content)
    print(f"📁 Filename: {filename}")
    
    # Save post
    success, filepath = save_post(content, filename)
    
    if success:
        print(f"✅ Blog post created: {filename}")
        
        # Show content preview
        print("\n" + "="*50)
        print("CONTENT PREVIEW:")
        print("="*50)
        preview_lines = content.split('\n')[:20]  # First 20 lines
        print('\n'.join(preview_lines))
        if len(content.split('\n')) > 20:
            print("...")
        print("="*50)
        
        # Word count
        word_count = len(content.split())
        print(f"📊 Word count: {word_count}")
        
        # Commit and push
        if git_commit_and_push():
            print("🎉 Blog post published successfully!")
            print(f"🌐 Available at: https://cyborgbusinessconsultant.com/blog/")
        else:
            print("⚠️ Failed to publish - manual intervention required")
            print(f"📄 File saved locally: {filepath}")
    else:
        print("❌ Failed to save blog post")
        sys.exit(1)

if __name__ == "__main__":
    main()