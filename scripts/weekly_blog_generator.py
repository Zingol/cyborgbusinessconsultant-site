#!/usr/bin/env python3
"""
Weekly Blog Post Generator for cyborgbusinessconsultant.com
Uses Ollama qwen3:8b to generate SEO-optimized blog posts
Author: Francesco Rosso Zingone
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

# Topic pool for variety
TOPICS = [
    "AI integration methodologies for business consulting",
    "How data-driven consulting transforms client outcomes", 
    "The competitive advantage of AI-augmented business strategy",
    "Digital transformation frameworks for modern businesses",
    "Measuring ROI in AI-powered consulting engagements",
    "Building scalable business intelligence systems",
    "The evolution of strategic consulting in the digital age",
    "Automation vs human insight in business decision making",
    "Client success patterns in AI-integrated consulting",
    "Future-proofing business models with intelligent systems"
]

# Internal links pool
INTERNAL_LINKS = [
    ("/about", "Francesco Rosso Zingone's methodology"),
    ("/evolution", "Business Evolution Program"),
    ("/manifesto", "Cyborg Business Consultant approach"),
    ("/contact", "Discovery Day consultation")
]

def generate_prompt(topic):
    """Generate optimized prompt for qwen3:8b"""
    
    prompt = f"""You are Francesco Rosso Zingone, Italy's first Cyborg Business Consultant with 25+ years of experience. Write a professional blog post about "{topic}" for cyborgbusinessconsultant.com.

CRITICAL REQUIREMENTS:
- Write in perfect English
- 1200-1500 words
- Professional, authoritative tone (NO sci-fi language)
- SEO optimized with natural keyword integration
- Include Hugo front matter with all SEO fields
- Focus on measurable business results and competitive advantage

STRUCTURE MUST BE:
```
---
title: "Compelling Title with Main Keyword"
description: "SEO meta description 150-160 chars with keyword"
date: {datetime.now().strftime('%Y-%m-%d')}
tags: ["business-transformation", "AI-integration", "strategic-consulting", "competitive-advantage"]
categories: ["Business Strategy", "AI Consulting"]
keywords: ["AI business consulting", "strategic consulting", "digital transformation"]
---

# Compelling Headline

**Strong opening sentence that hooks the reader.**

Introduction paragraph that establishes the problem/opportunity and your authority.

---

## First Major Section

Content with practical insights, include specific metrics when possible.

## Second Major Section  

More strategic insights with real-world applications.

## Third Major Section

Advanced concepts with actionable frameworks.

---

## Key Takeaways

Summary of main points with practical next steps.

---

*This insights series explores advanced methodologies in AI-integrated business consulting.*

**Ready to transform your consulting approach? [Book a Discovery Day](/contact).**

---

*Francesco Rosso Zingone  
The First Cyborg Business Consultant*
```

CONTENT GUIDELINES:
- Reference your 25+ years of experience naturally
- Mention "AI-integrated consulting methodology" 
- Include at least one specific metric/result (can be hypothetical but realistic)
- Focus on ROI, efficiency gains, competitive positioning
- Use terms like "measurable results", "strategic advantage", "proven methodologies"
- Avoid terms like "transcend", "evolve species", "post-human"
- Keep tone professional but accessible

SEO KEYWORDS TO INTEGRATE NATURALLY:
- AI business consulting
- Strategic consulting  
- Digital transformation
- Business intelligence
- Competitive advantage
- Francesco Rosso Zingone
- Fractional CMO
- Business automation

Write the complete blog post following the exact structure above."""

    return prompt

def call_ollama(prompt):
    """Call Ollama with qwen3:8b model"""
    try:
        print("Calling Ollama qwen3:8b...")
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
            print(f"Ollama error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("Ollama call timed out")
        return None
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return None

def add_external_link_placeholder(content):
    """Add placeholder for manual external link addition"""
    
    # Add note for manual external link insertion
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        # Add external link placeholder after first section
        if line.startswith('## ') and len([l for l in new_lines if l.startswith('## ')]) == 1:
            new_lines.append('')
            new_lines.append('<!-- EXTERNAL LINK: Add relevant authoritative source (Harvard Business Review, McKinsey, MIT, etc.) related to this section -->')
            new_lines.append('')
    
    return '\n'.join(new_lines)

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
        slug = f"business-insights-{datetime.now().strftime('%m-%d')}"
    
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
    
    # Add external link placeholder
    enhanced_content = add_external_link_placeholder(content)
    
    # Create filename
    filename = create_filename(enhanced_content)
    print(f"📁 Filename: {filename}")
    
    # Save post
    success, filepath = save_post(enhanced_content, filename)
    
    if success:
        print(f"✅ Blog post created: {filename}")
        
        # Show content preview
        print("\n" + "="*50)
        print("CONTENT PREVIEW:")
        print("="*50)
        print(enhanced_content[:500] + "...")
        print("="*50)
        
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
