"""
Content Generator - Creates engaging posts and images
Supports multiple AI services (OpenAI, Groq) and free image sources
"""

import os
import requests
import json
from datetime import datetime
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging

from config import (
    OPENAI_API_KEY, GROQ_API_KEY, CHANNEL_TOPIC, 
    USE_DALLE, USE_UNSPLASH, UNSPLASH_ACCESS_KEY,
    USE_GROQ, IMAGES_DIR
)

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generate AI-driven posts and images"""
    
    def __init__(self):
        self.topic = CHANNEL_TOPIC
        self.morning_posts_used = set()
        self.evening_posts_used = set()
        
    def generate_post_text(self, time_of_day: str = "morning") -> str:
        """
        Generate engaging post text using AI
        
        Args:
            time_of_day: "morning" or "evening"
            
        Returns:
            Generated post text
        """
        if USE_GROQ and GROQ_API_KEY:
            return self._generate_with_groq(time_of_day)
        elif OPENAI_API_KEY:
            return self._generate_with_openai(time_of_day)
        else:
            return self._generate_fallback_post(time_of_day)
    
    def _generate_with_openai(self, time_of_day: str) -> str:
        """Generate using OpenAI API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            prompt = f"""Generate a clear, eye-catching, engaging and not very long post about '{self.topic}' 
for a Telegram channel at {time_of_day}. Make it human-like and interesting.
Keep it under 300 characters. Make it relevant to current trends."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative social media expert writing for a Telegram channel."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            post_text = response.choices[0].message.content.strip()
            return post_text
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self._generate_fallback_post(time_of_day)
    
    def _generate_with_groq(self, time_of_day: str) -> str:
        """Generate using Groq API (free tier available)"""
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f"""Generate a clear, eye-catching, engaging and not very long post about '{self.topic}' 
for a Telegram channel at {time_of_day}. Make it human-like but also state that this is an AI-driven channel.
Keep it under 300 characters. Make it interesting and relevant to current trends."""
            
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are a creative social media expert writing for a Telegram channel."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            post_text = response.choices[0].message.content.strip()
            return post_text
            
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return self._generate_fallback_post(time_of_day)
    
    def _generate_fallback_post(self, time_of_day: str) -> str:
        """Fallback posts if APIs fail"""
        fallback_posts = {
            "morning": [
                f"🌅 Good morning! Today's insight about {self.topic}:\nStay tuned for more fascinating updates throughout the day!",
                f"☀️ Rise and shine! Here's your daily dose of {self.topic}.\nLet's make today amazing!",
                f"🌟 Morning vibes! Exploring today's trending aspects of {self.topic}.\nDon't miss out!",
            ],
            "evening": [
                f"🌙 Evening reflection: Today's most compelling {self.topic} moments.\nWhat caught your eye?",
                f"🌅 As the day winds down, here's what you need to know about {self.topic}.\nSee you tomorrow!",
                f"💫 Night time thoughts on {self.topic}. Goodnight and sweet dreams!",
            ]
        }
        
        posts = fallback_posts.get(time_of_day, fallback_posts["morning"])
        import random
        return random.choice(posts)
    
    def generate_image(self, post_text: str) -> Optional[str]:
        """
        Generate or fetch an image for the post
        
        Args:
            post_text: The post text to generate image for
            
        Returns:
            Path to the generated image
        """
        if USE_DALLE and OPENAI_API_KEY:
            return self._generate_with_dalle(post_text)
        elif USE_UNSPLASH:
            return self._fetch_from_unsplash(post_text)
        else:
            return self._create_simple_image(post_text)
    
    def _generate_with_dalle(self, post_text: str) -> Optional[str]:
        """Generate image using DALL-E"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            # Extract topic from post for image prompt
            prompt = f"Create an eye-catching, professional image related to: {self.topic}. Make it vibrant and engaging for social media."
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(IMAGES_DIR, f"dalle_{timestamp}.png")
            img.save(image_path)
            
            logger.info(f"DALL-E image generated: {image_path}")
            return image_path
            
        except Exception as e:
            logger.error(f"DALL-E error: {e}")
            return None
    
    def _fetch_from_unsplash(self, post_text: str) -> Optional[str]:
        """Fetch free images from Unsplash API"""
        try:
            # Extract keywords from topic
            keywords = self.topic.replace(" ", "+")
            
            url = "https://api.unsplash.com/photos/random"
            params = {
                "query": keywords,
                "client_id": UNSPLASH_ACCESS_KEY if UNSPLASH_ACCESS_KEY else "demo",
                "w": 1024,
                "h": 1024
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                image_url = data["urls"]["regular"]
                
                img_response = requests.get(image_url, timeout=10)
                img = Image.open(BytesIO(img_response.content))
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(IMAGES_DIR, f"unsplash_{timestamp}.png")
                img.save(image_path)
                
                logger.info(f"Unsplash image fetched: {image_path}")
                return image_path
            
        except Exception as e:
            logger.error(f"Unsplash error: {e}")
        
        return None
    
    def _create_simple_image(self, post_text: str) -> str:
        """Create a simple but attractive image with text"""
        try:
            # Create image with gradient-like effect
            width, height = 1024, 1024
            img = Image.new("RGB", (width, height), color=(15, 23, 42))  # Dark blue background
            draw = ImageDraw.Draw(img)
            
            # Try to use a nice font, fallback to default
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Extract first line as title
            lines = post_text.split("\n")
            title = lines[0][:40] if lines else self.topic
            
            # Draw decorative elements
            draw.rectangle([(50, 50), (974, 974)], outline=(100, 150, 255), width=5)
            draw.ellipse([(100, 100), (300, 300)], outline=(100, 150, 255), width=2)
            draw.ellipse([(724, 724), (924, 924)], outline=(100, 150, 255), width=2)
            
            # Draw title
            draw.text((100, 200), title, fill=(100, 200, 255), font=title_font)
            
            # Draw topic
            draw.text((100, 400), f"📌 {self.topic}", fill=(200, 220, 255), font=text_font)
            
            # Draw AI indicator
            draw.text((100, 700), "✨ AI-Driven Channel", fill=(150, 255, 200), font=text_font)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(IMAGES_DIR, f"generated_{timestamp}.png")
            img.save(image_path)
            
            logger.info(f"Simple image created: {image_path}")
            return image_path
            
        except Exception as e:
            logger.error(f"Image creation error: {e}")
            return None


def get_content_generator() -> ContentGenerator:
    """Get or create content generator instance"""
    return ContentGenerator()
