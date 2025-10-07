
import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import random
import math
import bezier

# Configure the page
st.set_page_config(
    page_title="Ultra Accurate Handwriting Converter - Improved",
    page_icon="✍️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #2E86AB;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #A23B72;
    margin-bottom: 1rem;
}
.stTextArea textarea {
    font-family: 'Georgia', serif;
}
</style>
""", unsafe_allow_html=True)

class ImprovedHandwritingGenerator:
    def __init__(self):
        self.base_font_size = 32
        self.line_spacing = 50
        self.letter_spacing = 2
        self.word_spacing = 15

    def smooth_curve(self, points, smoothness=0.3):
        """Create smooth curves between points using bezier-like interpolation"""
        if len(points) < 3:
            return points

        smooth_points = []
        smooth_points.append(points[0])

        for i in range(1, len(points) - 1):
            prev_point = points[i-1]
            curr_point = points[i]
            next_point = points[i+1]

            # Create intermediate points for smoother curves
            for t in np.linspace(0, 1, 3):
                if t == 0:
                    continue

                # Catmull-Rom spline interpolation
                x = (
                    smoothness * (next_point[0] - prev_point[0]) * t +
                    curr_point[0]
                )
                y = (
                    smoothness * (next_point[1] - prev_point[1]) * t +
                    curr_point[1]
                )

                smooth_points.append((x, y))

        smooth_points.append(points[-1])
        return smooth_points

    def add_natural_variations(self, points, variation_factor=0.15):
        """Add subtle natural handwriting variations"""
        varied_points = []
        for i, (x, y) in enumerate(points):
            # Less variation at start/end of strokes
            edge_factor = min(i / len(points), (len(points) - i) / len(points), 0.5) * 2
            current_variation = variation_factor * edge_factor

            x_var = random.uniform(-current_variation, current_variation) * 3
            y_var = random.uniform(-current_variation, current_variation) * 3
            varied_points.append((x + x_var, y + y_var))
        return varied_points

    def create_improved_letter_paths(self, letter, base_x, base_y, size_variation=1.0):
        """Create more realistic handwritten letter paths with better connectivity"""

        # Improved letter paths with more natural curves and connections
        paths = {
            'a': [
                [(12, 25), (8, 20), (4, 25), (4, 32), (8, 36), (16, 36), (20, 32), (20, 20)],
                [(20, 20), (20, 36)]
            ],
            'b': [
                [(4, 8), (4, 36)],
                [(4, 20), (12, 18), (16, 22), (12, 26), (4, 26)],
                [(4, 26), (14, 26), (18, 30), (18, 32), (14, 36), (4, 36)]
            ],
            'c': [
                [(18, 22), (14, 18), (8, 18), (4, 22), (4, 32), (8, 36), (14, 36), (18, 32)]
            ],
            'd': [
                [(20, 8), (20, 36)],
                [(20, 20), (16, 18), (10, 18), (6, 22), (6, 32), (10, 36), (16, 36), (20, 32)]
            ],
            'e': [
                [(4, 27), (18, 27), (18, 22), (14, 18), (8, 18), (4, 22), (4, 32), (8, 36), (14, 36), (18, 32)]
            ],
            'f': [
                [(16, 8), (12, 4), (8, 4), (6, 6)],
                [(8, 4), (8, 36)],
                [(4, 20), (14, 20)]
            ],
            'g': [
                [(18, 20), (14, 18), (8, 18), (4, 22), (4, 30), (8, 34), (14, 34), (18, 30), (18, 42), (14, 46), (8, 46), (4, 42)]
            ],
            'h': [
                [(4, 8), (4, 36)],
                [(4, 24), (8, 20), (14, 20), (18, 24), (18, 36)]
            ],
            'i': [
                [(8, 18), (8, 32), (10, 36), (14, 36)],
                [(8, 12), (8, 14)]
            ],
            'j': [
                [(12, 18), (12, 40), (8, 44), (4, 44), (2, 42)],
                [(12, 12), (12, 14)]
            ],
            'k': [
                [(4, 8), (4, 36)],
                [(4, 26), (16, 18)],
                [(10, 24), (18, 36)]
            ],
            'l': [
                [(8, 8), (8, 32), (10, 36), (14, 36)]
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
                [(4, 22), (4, 32), (8, 36), (14, 36), (18, 32), (18, 22), (14, 18), (8, 18), (4, 22)]
            ],
            'p': [
                [(4, 18), (4, 44)],
                [(4, 22), (10, 18), (16, 18), (18, 22), (18, 26), (16, 30), (10, 30), (4, 26)]
            ],
            'q': [
                [(18, 18), (18, 44)],
                [(18, 22), (14, 18), (8, 18), (4, 22), (4, 32), (8, 36), (14, 36), (18, 32)]
            ],
            'r': [
                [(4, 18), (4, 36)],
                [(4, 22), (8, 18), (12, 18), (14, 20)]
            ],
            's': [
                [(16, 20), (12, 18), (8, 18), (6, 20), (8, 22), (12, 24), (14, 26), (16, 30), (12, 34), (8, 36), (6, 34)]
            ],
            't': [
                [(8, 10), (8, 32), (10, 36), (14, 36)],
                [(4, 18), (12, 18)]
            ],
            'u': [
                [(4, 18), (4, 30), (8, 36), (14, 36), (18, 30), (18, 18)],
                [(18, 28), (18, 36)]
            ],
            'v': [
                [(4, 18), (11, 34), (18, 18)]
            ],
            'w': [
                [(2, 18), (7, 34), (11, 26), (15, 34), (20, 18)]
            ],
            'x': [
                [(4, 18), (18, 36)],
                [(18, 18), (4, 36)]
            ],
            'y': [
                [(4, 18), (11, 30)],
                [(18, 18), (11, 30), (8, 42), (4, 46), (2, 44)]
            ],
            'z': [
                [(4, 18), (16, 18), (4, 34), (16, 34)]
            ],
            # Uppercase letters
            'A': [
                [(4, 36), (12, 8), (20, 36)],
                [(8, 24), (16, 24)]
            ],
            'B': [
                [(4, 8), (4, 36), (14, 36), (18, 32), (18, 28), (14, 24), (4, 24)],
                [(4, 24), (14, 24), (18, 20), (18, 16), (14, 8), (4, 8)]
            ],
            'C': [
                [(20, 14), (16, 8), (8, 8), (4, 14), (4, 30), (8, 36), (16, 36), (20, 30)]
            ],
            'H': [
                [(4, 8), (4, 36)],
                [(20, 8), (20, 36)],
                [(4, 22), (20, 22)]
            ],
            'W': [
                [(2, 8), (6, 36), (12, 20), (18, 36), (22, 8)]
            ],
            # Numbers
            '0': [
                [(4, 14), (4, 30), (8, 36), (16, 36), (20, 30), (20, 14), (16, 8), (8, 8), (4, 14)]
            ],
            '1': [
                [(8, 10), (12, 8), (12, 36)],
                [(8, 36), (16, 36)]
            ],
            '2': [
                [(4, 14), (8, 8), (16, 8), (20, 14), (20, 18), (4, 36), (20, 36)]
            ],
            # Punctuation
            '.': [[(8, 32), (8, 36), (12, 36), (12, 32), (8, 32)]],
            ',': [[(8, 32), (8, 36), (12, 36), (12, 32), (8, 32)], [(10, 36), (8, 42)]],
            '!': [[(8, 8), (8, 28)], [(8, 32), (8, 36), (12, 36), (12, 32), (8, 32)]],
            '?': [[(4, 14), (8, 8), (16, 8), (20, 14), (16, 18), (12, 22), (12, 26)], [(12, 32), (12, 36)]],
            ' ': []
        }

        if letter not in paths:
            letter = letter.lower()
            if letter not in paths:
                return []

        letter_strokes = paths[letter]
        if not letter_strokes:
            return []

        all_points = []
        for stroke in letter_strokes:
            if not stroke:
                continue

            # Scale and position the stroke
            scaled_stroke = []
            for x, y in stroke:
                new_x = base_x + (x * size_variation * 0.8)
                new_y = base_y + (y * size_variation * 0.8)
                scaled_stroke.append((new_x, new_y))

            # Add natural variations and smooth the stroke
            if len(scaled_stroke) > 1:
                varied_stroke = self.add_natural_variations(scaled_stroke)
                smooth_stroke = self.smooth_curve(varied_stroke)
                all_points.extend(smooth_stroke)
                all_points.append(None)  # Stroke separator

        return all_points

    def generate_handwriting(self, text, width=800, height=600, 
                           pen_thickness=2, slant_angle=0, 
                           size_variation=1.0, roughness=0.3,
                           line_height=1.5):
        """Generate improved handwritten text"""

        # Create blank image with slight off-white background
        bg_color = (255, 255, 252)  # Slightly warm white
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Starting position
        current_x = 40
        current_y = 60
        max_line_height = self.base_font_size * size_variation * line_height

        words = text.replace('\n', ' \n ').split()

        for word in words:
            if word == '\n':
                current_y += max_line_height
                current_x = 40
                continue

            word_width = len(word) * (24 * size_variation)

            # Line wrapping
            if current_x + word_width > width - 60:
                current_y += max_line_height
                current_x = 40

            # Process each character in the word
            for char_idx, char in enumerate(word):
                if char == ' ':
                    current_x += self.word_spacing * size_variation
                    continue

                # Get letter path
                letter_points = self.create_improved_letter_paths(
                    char, current_x, current_y, size_variation
                )

                if letter_points:
                    # Draw each stroke
                    current_stroke = []
                    pen_color = (20, 20, 40)  # Dark blue-black

                    for point in letter_points:
                        if point is None:  # End of stroke
                            if len(current_stroke) > 1:
                                self.draw_smooth_stroke(
                                    draw, current_stroke, pen_thickness, 
                                    pen_color, slant_angle, current_x
                                )
                            current_stroke = []
                        else:
                            current_stroke.append(point)

                    # Draw final stroke if exists
                    if len(current_stroke) > 1:
                        self.draw_smooth_stroke(
                            draw, current_stroke, pen_thickness, 
                            pen_color, slant_angle, current_x
                        )

                # Move to next character position
                char_width = 24 * size_variation
                if char.isupper():
                    char_width *= 1.2
                current_x += char_width + (self.letter_spacing * size_variation)

            # Add word spacing
            current_x += self.word_spacing * size_variation * 0.7

        return img

    def draw_smooth_stroke(self, draw, points, thickness, color, slant_angle, base_x):
        """Draw a smooth stroke with consistent thickness"""
        if len(points) < 2:
            return

        # Apply slant transformation
        if slant_angle != 0:
            slant_rad = math.radians(slant_angle)
            slanted_points = []
            for x, y in points:
                y_offset = (x - base_x) * math.tan(slant_rad) * 0.3
                slanted_points.append((x, y + y_offset))
            points = slanted_points

        # Draw the stroke with multiple overlapping lines for smoothness
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            # Main stroke
            draw.line([(x1, y1), (x2, y2)], fill=color, width=thickness)

            # Add slight thickness variation for more natural look
            if random.random() < 0.3:
                thickness_var = thickness + random.choice([-1, 1])
                thickness_var = max(1, thickness_var)
                draw.line([(x1, y1), (x2, y2)], fill=color, width=thickness_var)

def main():
    st.markdown('<h1 class="main-header">✍️ Ultra Accurate Handwriting Converter - Improved</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
        Transform your digital text into realistic, legible handwriting with enhanced letter formation and natural flow
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize the handwriting generator
    generator = ImprovedHandwritingGenerator()

    # Sidebar for controls
    with st.sidebar:
        st.markdown('<h2 class="sub-header">🎨 Writing Controls</h2>', unsafe_allow_html=True)

        # Text input with better default
        input_text = st.text_area(
            "Enter your text:",
            value="Hello World!\nThis is much better handwriting.",
            height=150,
            help="Enter the text you want to convert to handwriting"
        )

        st.markdown("---")

        # Predefined styles
        st.markdown("**Quick Styles**")
        style_preset = st.selectbox(
            "Choose a style preset:",
            ["Custom", "Clean & Neat", "Casual Writing", "Elegant Script", "Quick Notes"]
        )

        # Style presets
        if style_preset == "Clean & Neat":
            pen_thickness = 2
            size_variation = 0.9
            slant_angle = 0
            roughness = 0.2
            line_height = 1.6
        elif style_preset == "Casual Writing":
            pen_thickness = 2
            size_variation = 1.0
            slant_angle = 3
            roughness = 0.3
            line_height = 1.5
        elif style_preset == "Elegant Script":
            pen_thickness = 2
            size_variation = 1.1
            slant_angle = 8
            roughness = 0.25
            line_height = 1.7
        elif style_preset == "Quick Notes":
            pen_thickness = 3
            size_variation = 0.8
            slant_angle = -2
            roughness = 0.4
            line_height = 1.4
        else:  # Custom
            st.markdown("**Custom Settings**")
            pen_thickness = st.slider("Pen Thickness", 1, 4, 2)
            size_variation = st.slider("Letter Size", 0.7, 1.4, 1.0, 0.1)
            slant_angle = st.slider("Slant Angle", -15, 15, 0)
            roughness = st.slider("Writing Variation", 0.1, 0.5, 0.3, 0.05)
            line_height = st.slider("Line Spacing", 1.2, 2.0, 1.5, 0.1)

        st.markdown("**Paper Settings**")
        paper_width = st.slider("Paper Width", 600, 1200, 900, 50)
        paper_height = st.slider("Paper Height", 400, 800, 650, 50)

        # Generate button
        generate_btn = st.button("🖊️ Generate Improved Handwriting", type="primary")

    # Main content area
    col1, col2 = st.columns([2.5, 1])

    with col1:
        if generate_btn and input_text:
            with st.spinner("Generating beautiful handwritten text..."):
                try:
                    # Generate the handwriting
                    handwritten_img = generator.generate_handwriting(
                        text=input_text,
                        width=paper_width,
                        height=paper_height,
                        pen_thickness=pen_thickness,
                        slant_angle=slant_angle,
                        size_variation=size_variation,
                        roughness=roughness,
                        line_height=line_height
                    )

                    # Display the result
                    st.markdown('<h3 class="sub-header">📝 Your Beautiful Handwriting</h3>', unsafe_allow_html=True)
                    st.image(handwritten_img, caption="Generated handwritten text", use_column_width=True)

                    # Download option
                    buf = io.BytesIO()
                    handwritten_img.save(buf, format='PNG', quality=95, dpi=(300, 300))
                    byte_im = buf.getvalue()

                    st.download_button(
                        label="📥 Download High-Quality Image",
                        data=byte_im,
                        file_name="beautiful_handwriting.png",
                        mime="image/png"
                    )

                except Exception as e:
                    st.error(f"Error generating handwriting: {str(e)}")
                    st.info("Please try adjusting the settings or using shorter text.")

        elif not input_text:
            st.info("👈 Please enter some text in the sidebar to generate handwriting!")
        else:
            st.info("👈 Click the 'Generate Improved Handwriting' button to see the results!")

    with col2:
        st.markdown('<h3 class="sub-header">✨ New Improvements</h3>', unsafe_allow_html=True)

        improvements = [
            "🎯 Much more legible letter formation",
            "🔗 Better letter connectivity and flow",
            "📐 Smooth curves and natural strokes",
            "🎨 Realistic pen pressure variation",
            "📝 Improved spacing and alignment",
            "🏷️ Style presets for different occasions",
            "📊 High-quality output (300 DPI)",
            "🔤 Enhanced uppercase and punctuation"
        ]

        for improvement in improvements:
            st.markdown(f"• {improvement}")

        st.markdown("---")

        st.markdown('<h4>💡 Tips for Best Results</h4>', unsafe_allow_html=True)
        tips = [
            "Try the 'Clean & Neat' preset first",
            "Use moderate text length for best formatting",
            "Experiment with slight slant angles (3-8°)",
            "Adjust line spacing for better readability"
        ]

        for tip in tips:
            st.markdown(f"• {tip}")

        st.markdown("---")
        st.markdown("**Sample Text Ideas:**")
        sample_texts = [
            "The quick brown fox jumps over the lazy dog",
            "Dear friend, I hope this letter finds you well",
            "Meeting notes: Project deadline is next Friday"
        ]

        for sample in sample_texts:
            if st.button(f"Use: {sample[:25]}...", key=sample):
                st.session_state.sample_text = sample

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; margin-top: 2rem;">
        <p>Ultra Accurate Handwriting Converter v2.0 - Improved Edition | Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
