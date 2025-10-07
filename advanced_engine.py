
import numpy as np
from PIL import Image, ImageDraw
import random
import math

class AdvancedHandwritingEngine:
    """
    Advanced handwriting engine with improved letter formation,
    natural connectivity, and realistic stroke generation
    """

    def __init__(self):
        self.stroke_smoothness = 0.7
        self.natural_variation = 0.15
        self.connection_strength = 0.8

    def create_natural_stroke(self, start_point, end_point, control_points=None):
        """Create a natural-looking stroke between two points"""
        if control_points is None:
            # Generate natural control points
            mid_x = (start_point[0] + end_point[0]) / 2
            mid_y = (start_point[1] + end_point[1]) / 2

            # Add slight curve variation
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-3, 3)
            control_points = [(mid_x + offset_x, mid_y + offset_y)]

        # Generate smooth curve points
        curve_points = []
        for t in np.linspace(0, 1, 15):
            if len(control_points) == 1:
                # Quadratic Bezier curve
                cp = control_points[0]
                x = (1-t)**2 * start_point[0] + 2*(1-t)*t * cp[0] + t**2 * end_point[0]
                y = (1-t)**2 * start_point[1] + 2*(1-t)*t * cp[1] + t**2 * end_point[1]
            else:
                # Linear interpolation fallback
                x = start_point[0] + t * (end_point[0] - start_point[0])
                y = start_point[1] + t * (end_point[1] - start_point[1])

            # Add micro-variations for natural look
            x += random.uniform(-0.5, 0.5)
            y += random.uniform(-0.5, 0.5)
            curve_points.append((x, y))

        return curve_points

    def get_letter_strokes(self, letter):
        """
        Get optimized stroke data for each letter with natural entry/exit points
        Returns list of strokes, each stroke is a list of (x, y) coordinates
        """

        # Optimized letter stroke definitions with better proportions
        letter_strokes = {
            'a': [
                # Main circular part
                [(16, 28), (12, 24), (8, 24), (4, 28), (4, 32), (8, 36), (16, 36), (20, 32), (20, 24)],
                # Vertical line
                [(20, 24), (20, 36)]
            ],
            'b': [
                # Main vertical line
                [(4, 8), (4, 36)],
                # Upper bump
                [(4, 20), (8, 18), (14, 18), (18, 22), (18, 26), (14, 30), (4, 30)],
                # Lower bump  
                [(4, 30), (12, 30), (18, 34), (18, 38), (14, 42), (8, 42), (4, 36)]
            ],
            'c': [
                [(18, 22), (16, 18), (10, 18), (6, 22), (6, 32), (10, 36), (16, 36), (18, 32)]
            ],
            'd': [
                [(20, 8), (20, 36)],
                [(20, 24), (16, 18), (10, 18), (6, 22), (6, 32), (10, 36), (16, 36), (20, 32)]
            ],
            'e': [
                [(6, 27), (18, 27), (18, 22), (16, 18), (10, 18), (6, 22), (6, 32), (10, 36), (16, 36), (18, 32)]
            ],
            'f': [
                [(14, 8), (10, 4), (6, 4), (4, 6), (6, 8)],
                [(8, 8), (8, 36)],
                [(4, 20), (12, 20)]
            ],
            'g': [
                [(18, 24), (16, 20), (10, 20), (6, 24), (6, 30), (10, 34), (16, 34), (18, 30), (18, 42), (16, 46), (10, 46), (6, 42)]
            ],
            'h': [
                [(4, 8), (4, 36)],
                [(4, 24), (8, 20), (14, 20), (18, 24), (18, 36)]
            ],
            'i': [
                [(8, 18), (8, 32), (12, 36), (16, 36)],
                [(10, 12), (10, 14)]  # Dot
            ],
            'j': [
                [(12, 18), (12, 40), (10, 44), (6, 44), (4, 42)],
                [(12, 12), (12, 14)]  # Dot
            ],
            'k': [
                [(4, 8), (4, 36)],
                [(4, 26), (16, 18)],
                [(10, 24), (18, 36)]
            ],
            'l': [
                [(8, 8), (8, 32), (12, 36), (16, 36)]
            ],
            'm': [
                [(4, 18), (4, 36)],
                [(4, 22), (6, 18), (10, 18), (12, 22), (12, 36)],
                [(12, 22), (14, 18), (18, 18), (20, 22), (20, 36)]
            ],
            'n': [
                [(4, 18), (4, 36)],
                [(4, 22), (8, 18), (14, 18), (18, 22), (18, 36)]
            ],
            'o': [
                [(6, 22), (6, 32), (10, 36), (14, 36), (18, 32), (18, 22), (14, 18), (10, 18), (6, 22)]
            ],
            'p': [
                [(4, 18), (4, 44)],
                [(4, 22), (10, 18), (16, 18), (18, 22), (18, 28), (16, 32), (10, 32), (4, 28)]
            ],
            'q': [
                [(18, 18), (18, 44)],
                [(18, 24), (14, 18), (8, 18), (4, 22), (4, 32), (8, 36), (14, 36), (18, 32)]
            ],
            'r': [
                [(4, 18), (4, 36)],
                [(4, 22), (8, 18), (14, 18), (16, 20)]
            ],
            's': [
                [(16, 20), (12, 18), (8, 18), (6, 20), (8, 22), (12, 24), (14, 26), (16, 30), (14, 34), (10, 36), (6, 34)]
            ],
            't': [
                [(8, 10), (8, 32), (12, 36), (16, 36)],
                [(4, 18), (12, 18)]
            ],
            'u': [
                [(4, 18), (4, 30), (8, 36), (14, 36), (18, 30), (18, 18), (18, 36)]
            ],
            'v': [
                [(4, 18), (12, 34), (20, 18)]
            ],
            'w': [
                [(2, 18), (8, 34), (12, 26), (16, 34), (22, 18)]
            ],
            'x': [
                [(4, 18), (18, 36)],
                [(18, 18), (4, 36)]
            ],
            'y': [
                [(4, 18), (12, 30)],
                [(20, 18), (12, 30), (8, 42), (4, 46)]
            ],
            'z': [
                [(4, 18), (18, 18), (4, 34), (18, 34)]
            ],
            # Uppercase letters
            'H': [
                [(4, 8), (4, 36)],
                [(20, 8), (20, 36)],
                [(4, 22), (20, 22)]
            ],
            'W': [
                [(2, 8), (8, 36), (12, 20), (16, 36), (22, 8)]
            ],
            'A': [
                [(4, 36), (12, 8), (20, 36)],
                [(8, 24), (16, 24)]
            ],
            # Punctuation with better shapes
            '.': [[(10, 32), (10, 36), (14, 36), (14, 32), (10, 32)]],
            ',': [[(10, 32), (10, 36), (14, 36), (14, 32), (10, 32)], [(12, 36), (10, 42)]],
            '!': [[(10, 8), (10, 26)], [(10, 30), (10, 36)]],
            '?': [[(6, 14), (10, 8), (16, 8), (20, 14), (16, 18), (12, 22), (12, 26)], [(12, 30), (12, 36)]],
            ' ': []
        }

        return letter_strokes.get(letter, letter_strokes.get(letter.lower(), []))

    def apply_natural_variations(self, points, variation_intensity=0.15):
        """Apply natural handwriting variations to points"""
        varied_points = []
        for i, (x, y) in enumerate(points):
            # Reduce variation at stroke endpoints
            edge_factor = min(i / max(len(points) - 1, 1), 
                            (len(points) - i) / max(len(points) - 1, 1))
            edge_factor = min(edge_factor * 2, 1.0)

            variation = variation_intensity * edge_factor
            x_var = random.uniform(-variation, variation) * 2
            y_var = random.uniform(-variation, variation) * 2

            varied_points.append((x + x_var, y + y_var))

        return varied_points

    def render_letter(self, draw, letter, base_x, base_y, size_factor=1.0, 
                     pen_thickness=2, color=(20, 20, 40), slant_angle=0):
        """Render a single letter with natural variations"""
        strokes = self.get_letter_strokes(letter)

        if not strokes:
            return base_x + 24 * size_factor  # Return next x position

        slant_rad = math.radians(slant_angle) if slant_angle else 0

        for stroke in strokes:
            if len(stroke) < 2:
                continue

            # Scale and position the stroke
            scaled_stroke = []
            for x, y in stroke:
                new_x = base_x + (x * size_factor * 0.75)
                new_y = base_y + (y * size_factor * 0.75)

                # Apply slant
                if slant_rad:
                    y_offset = (new_x - base_x) * math.tan(slant_rad) * 0.3
                    new_y += y_offset

                scaled_stroke.append((new_x, new_y))

            # Apply natural variations
            varied_stroke = self.apply_natural_variations(scaled_stroke)

            # Draw the stroke with anti-aliasing simulation
            self.draw_natural_stroke(draw, varied_stroke, pen_thickness, color)

        # Return next character position
        letter_width = 24 * size_factor * 0.85
        if letter.isupper():
            letter_width *= 1.2

        return base_x + letter_width

    def draw_natural_stroke(self, draw, points, thickness, color):
        """Draw a stroke with natural thickness variation"""
        if len(points) < 2:
            return

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            # Vary thickness slightly for natural look
            current_thickness = thickness
            if random.random() < 0.2:
                current_thickness += random.choice([-1, 1])
                current_thickness = max(1, min(current_thickness, thickness + 2))

            # Main stroke
            draw.line([(x1, y1), (x2, y2)], fill=color, width=current_thickness)

            # Add slight transparency effect by drawing thinner overlapping lines
            if current_thickness > 1:
                lighter_color = tuple(min(255, c + 30) for c in color)
                draw.line([(x1, y1), (x2, y2)], fill=lighter_color, width=max(1, current_thickness - 1))
