#!/usr/bin/env python3
"""
Create a professional WARP Client icon using PIL
"""
from PIL import Image, ImageDraw
import os

def create_warp_icon(size=512):
    """Create a professional WARP client icon"""
    
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors - sleek cyber theme
    bg_color = (20, 25, 40, 255)  # Dark blue-gray
    primary_color = (0, 230, 118, 255)  # Bright green (Matrix-like)
    secondary_color = (255, 107, 0, 255)  # Orange accent
    border_color = (100, 255, 200, 255)  # Light cyan
    
    # Draw main background circle
    center = size // 2
    radius = min(size // 2 - 20, center - 20)
    
    if radius > 10:  # Only draw if we have space
        # Create solid background circle
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    fill=bg_color)
        
        # Draw outer ring
        ring_width = max(2, size // 64)
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    outline=border_color, width=ring_width)
    
    # Draw WARP symbol - stylized "W"
    w_width = size // 3
    w_height = int(size // 2.5)
    w_x = center - w_width // 2
    w_y = center - w_height // 2
    
    # Draw stylized "W" 
    line_width = max(2, size // 40)
    points = [
        (w_x, w_y),
        (w_x + w_width // 4, w_y + w_height),
        (w_x + w_width // 2, w_y + w_height // 2),
        (w_x + 3 * w_width // 4, w_y + w_height),
        (w_x + w_width, w_y)
    ]
    
    # Draw the W with thick lines
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=primary_color, width=line_width)
    
    # Add circuit-like details around the W (only for larger sizes)
    if size >= 64:
        circuit_size = max(2, size // 80)
        circuit_points = [
            # Top circuits
            (center - w_width//3, w_y - 20),
            (center + w_width//3, w_y - 20),
            # Side circuits
            (w_x - 30, center),
            (w_x + w_width + 30, center),
            # Bottom circuits
            (center - w_width//4, w_y + w_height + 20),
            (center + w_width//4, w_y + w_height + 20),
        ]
        
        for point in circuit_points:
            if 0 <= point[0] <= size and 0 <= point[1] <= size:
                # Draw small circuit nodes
                draw.ellipse([point[0]-circuit_size, point[1]-circuit_size, 
                            point[0]+circuit_size, point[1]+circuit_size], 
                            fill=secondary_color)
    
    # Add tech-style corner elements (only for larger sizes)
    if size >= 128:
        corner_size = size // 17
        corner_width = max(2, size // 170)
        corners = [
            (10, 10), (size-corner_size-10, 10), 
            (10, size-corner_size-10), (size-corner_size-10, size-corner_size-10)
        ]
        
        for corner in corners:
            # L-shaped corner brackets
            draw.line([corner, (corner[0] + corner_size, corner[1])], 
                     fill=border_color, width=corner_width)
            draw.line([corner, (corner[0], corner[1] + corner_size)], 
                     fill=border_color, width=corner_width)
    
    return img

def create_multiple_sizes():
    """Create icons in multiple sizes for system integration"""
    sizes = [16, 24, 32, 48, 64, 128, 256, 512]
    
    for size in sizes:
        icon = create_warp_icon(size)
        icon.save(f'/home/nike/mini-warp-client/assets/icons/warp_client_{size}.png')
        print(f"Created {size}x{size} icon")
    
    # Main icon as PNG
    main_icon = create_warp_icon(256)  # Good balance of detail and size
    main_icon.save('/home/nike/mini-warp-client/assets/icons/warp_client.png')
    
    print("All icons created successfully!")

if __name__ == "__main__":
    create_multiple_sizes()
