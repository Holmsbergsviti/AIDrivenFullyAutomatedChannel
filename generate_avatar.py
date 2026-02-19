"""
Generate the Signals of the Future channel avatar
Glowing dot with signal waves on black background
"""

from PIL import Image, ImageDraw
import math
import os

def generate_avatar():
    """Generate the avatar image"""
    
    # Image size
    size = 512
    img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
    draw = ImageDraw.Draw(img, 'RGBA')
    
    center_x = size // 2
    center_y = size // 2 - 20  # Slightly above center
    
    # Draw signal waves (circles fading out)
    wave_colors = [
        (100, 150, 255, 40),   # Subtle blue, very transparent
        (100, 150, 255, 25),
        (100, 150, 255, 15),
        (100, 150, 255, 8),
    ]
    
    wave_radii = [80, 120, 160, 200]
    
    for i, (radius, color) in enumerate(zip(wave_radii, wave_colors)):
        draw.ellipse(
            [(center_x - radius, center_y - radius), 
             (center_x + radius, center_y + radius)],
            outline=color,
            width=2
        )
    
    # Draw glowing dot (main element)
    # Outer glow (soft electric blue)
    glow_radius = 25
    glow_color = (100, 150, 255, 100)
    draw.ellipse(
        [(center_x - glow_radius, center_y - glow_radius),
         (center_x + glow_radius, center_y + glow_radius)],
        fill=glow_color
    )
    
    # Inner glow (brighter)
    inner_glow_radius = 18
    inner_glow_color = (150, 200, 255, 150)
    draw.ellipse(
        [(center_x - inner_glow_radius, center_y - inner_glow_radius),
         (center_x + inner_glow_radius, center_y + inner_glow_radius)],
        fill=inner_glow_color
    )
    
    # Core dot (white)
    core_radius = 10
    draw.ellipse(
        [(center_x - core_radius, center_y - core_radius),
         (center_x + core_radius, center_y + core_radius)],
        fill=(255, 255, 255, 255)
    )
    
    # Add subtle electric blue tint to core
    core_tint_radius = 8
    draw.ellipse(
        [(center_x - core_tint_radius, center_y - core_tint_radius),
         (center_x + core_tint_radius, center_y + core_tint_radius)],
        fill=(180, 220, 255, 80)
    )
    
    # Save
    avatar_path = os.path.join(
        os.path.dirname(__file__), 
        'avatar.png'
    )
    img.save(avatar_path)
    print(f"✅ Avatar generated: {avatar_path}")
    return avatar_path


if __name__ == "__main__":
    generate_avatar()
