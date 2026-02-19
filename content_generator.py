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
import random

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
            
            prompt = f"""You are writing for "Signals of the Future" - a Telegram channel about quiet, emerging changes in technology, society, behavior, money, and internet culture.

Your style:
- Observational, not preachy
- Layered and philosophically curious
- Notice patterns others miss
- Short, sharp insights that build
- Use metaphors (wars as narratives, silence as strategy, etc)
- Question assumptions about the future
- Mix concrete examples with abstract thinking
- Ends with a thought about what's changing, not a call to action
- 150-250 words, well-structured with short paragraphs/lines
- Use minimal, lively emojis at the start (1-2): 📡 🔇 🔮 ∞ ⚖️ 🪫 etc - not cringe, minimalist

Recent examples of your tone:
"Modern wars aren't fought just on the ground anymore. They're fought in feeds, systems, and supply chains. Drones decide before soldiers arrive. Narratives spread faster than troops."

"Silence is becoming a strategy. Governments pause instead of announce. Companies delay instead of deny."

"Ownership is becoming abstract. You don't own software — you subscribe. Access replaces possession."

Generate a post about a signal or change in: {self.topic}
Make it feel like you noticed something important that nobody talks about yet.
For {time_of_day}.
Start with a minimal, fitting emoji then the content."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a keen observer of emerging patterns and quiet changes in the world. You write sharp, layered posts that make people think differently about what's already happening."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9
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
            
            prompt = f"""You are writing for "Signals of the Future" - a Telegram channel about quiet, emerging changes in technology, society, behavior, money, and internet culture.

Your style:
- Observational, not preachy
- Layered and philosophically curious
- Notice patterns others miss
- Short, sharp insights that build
- Use metaphors (wars as narratives, silence as strategy, etc)
- Question assumptions about the future
- Mix concrete examples with abstract thinking
- Ends with a thought about what's changing, not a call to action
- 150-250 words, well-structured with short paragraphs/lines
- Use minimal, lively emojis at the start (1-2): 📡 🔇 🔮 ∞ ⚖️ 🪫 etc - not cringe, minimalist

Recent examples of your tone:
"Modern wars aren't fought just on the ground anymore. They're fought in feeds, systems, and supply chains. Drones decide before soldiers arrive. Narratives spread faster than troops."

"Silence is becoming a strategy. Governments pause instead of announce. Companies delay instead of deny."

"Ownership is becoming abstract. You don't own software — you subscribe. Access replaces possession."

Generate a post about a signal or change in: {self.topic}
Make it feel like you noticed something important that nobody talks about yet.
For {time_of_day}.
Start with a minimal, fitting emoji then the content."""
            
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are a keen observer of emerging patterns and quiet changes in the world. You write sharp, layered posts that make people think differently about what's already happening."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9
            )
            
            post_text = response.choices[0].message.content.strip()
            return post_text
            
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return self._generate_fallback_post(time_of_day)
    
    def _generate_fallback_post(self, time_of_day: str) -> str:
        """Fallback posts if APIs fail - matches channel style"""
        fallback_posts = {
            "morning": [
                "📡 Data isn't neutral.\nAlgorithms aren't objective.\nYet we treat both like facts.\n\nInfrastructure shapes belief.\nBelief shapes what we build next.\n\nThe systems we use don't just deliver information—\nthey reshape how we think.\nEvery default is a choice.\nEvery algorithm is a philosophy.\n\nNotice which infrastructure you live inside.\nThen ask: who built this? Why this shape? What's invisible by design?",
                "🔇 Power used to announce itself loudly.\nNow it whispers through defaults.\n\nDefault settings.\nDefault recommendations.\nDefault privacy policies.\n\nThe future isn't about force—\nit's about what stays invisible.\nWhat never requires your attention.\nWhat you never even know you're choosing.\n\nThe strongest systems are the ones you don't notice you're inside.",
                "∞ Everything is becoming predictable.\nExcept prediction itself.\n\nThe more we optimize,\nthe fewer surprises remain.\nBut systems that can't surprise\nbecome systems we stop trusting.\n\nWe want prediction. We crave certainty.\nBut certainty without surprise is just control.\n\nWhat happens when everything is optimized\nand nothing shocks us anymore?",
            ],
            "evening": [
                "🔮 We talk about the future.\nBut we live in someone else's present.\n\nTheir infrastructure.\nTheir incentives.\nTheir rules.\nTheir bets on what matters.\n\nThe signal isn't technology—\nit's choice becoming invisible.\nPower isn't in what you can see.\nIt's in what's already decided before you arrive.\n\nNotice first. Understand the shape. Then ask: whose future is this building?",
                "🪫 Connection costs nothing now.\nExcept attention.\nExcept time.\nExcept knowing who's listening.\n\nFree has always had a price.\nThe price was just harder to see.\n\nNow the price is your data.\nNow it's your attention span.\nNow it's your belief in what's real.\n\nWe thought connection would set us free.\nInstead, it became the mechanism of capture.",
                "⚖️ Systems don't fail dramatically.\nThey fade.\n\nService gets slower.\nFeatures disappear.\nSupport stops responding.\nNotice the silence.\n\nIt's not a crash—\nit's a quiet withdrawal.\nA slow descent.\n\nAnd quiet is harder to protest.\nYou can't organize against something that whispers itself away.\nBut when the system fades, so does your trust in building the next one.",
            ]
        }
        
        posts = fallback_posts.get(time_of_day, fallback_posts["morning"])
        return random.choice(posts)
    
    def generate_image(self, post_text: str) -> Optional[str]:
        """
        Generate or fetch an image for the post
        
        Args:
            post_text: The post text to generate image for
            
        Returns:
            Path to the generated image
        """
        logger.info(f"generate_image called: USE_DALLE={USE_DALLE}, USE_UNSPLASH={USE_UNSPLASH}")
        if USE_DALLE and OPENAI_API_KEY:
            logger.info("Using DALL-E for image generation")
            return self._generate_with_dalle(post_text)
        elif USE_UNSPLASH:
            logger.info("Using Unsplash for image fetching")
            return self._fetch_from_unsplash(post_text)
        else:
            logger.info("Using simple image generation (fallback)")
            return self._create_simple_image(post_text)
    
    def _generate_with_dalle(self, post_text: str) -> Optional[str]:
        """Generate image using DALL-E"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
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
            logger.info("Creating simple image...")
            width, height = 1024, 1024
            img = Image.new("RGB", (width, height), color=(15, 23, 42))
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            lines = post_text.split("\n")
            title = lines[0][:40] if lines else self.topic
            
            draw.rectangle([(50, 50), (974, 974)], outline=(100, 150, 255), width=5)
            draw.ellipse([(100, 100), (300, 300)], outline=(100, 150, 255), width=2)
            draw.ellipse([(724, 724), (924, 924)], outline=(100, 150, 255), width=2)
            
            draw.text((100, 200), title, fill=(100, 200, 255), font=title_font)
            draw.text((100, 400), f"📡 {self.topic}", fill=(200, 220, 255), font=text_font)
            draw.text((100, 700), "Signals", fill=(150, 255, 200), font=text_font)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(IMAGES_DIR, f"generated_{timestamp}.png")
            img.save(image_path)
            
            # Verify file was written
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                logger.info(f"✅ Image created successfully: {image_path} ({file_size} bytes)")
                return image_path
            else:
                logger.error(f"❌ Image file not found after save: {image_path}")
                return None
            
        except Exception as e:
            logger.error(f"❌ Image creation error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None


def get_content_generator() -> ContentGenerator:
    """Get or create content generator instance"""
    return ContentGenerator()
