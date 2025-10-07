"""
Enhanced Configuration for Ultra Accurate Handwriting Converter - Improved
"""

# Enhanced application settings
DEFAULT_SETTINGS = {
    # Paper settings - improved defaults
    "paper_width": 900,
    "paper_height": 650,
    "paper_color": (255, 255, 252),  # Warm white
    "dpi": 300,  # High quality output

    # Handwriting style - more realistic defaults
    "pen_thickness": 2,
    "size_variation": 1.0,
    "slant_angle": 0,
    "roughness": 0.3,
    "line_height": 1.5,

    # Enhanced spacing settings
    "line_spacing": 50,
    "letter_spacing": 2,
    "word_spacing": 15,
    "margin_top": 60,
    "margin_left": 40,
    "margin_right": 40,

    # Advanced features enabled
    "smooth_curves": True,
    "natural_variations": True,
    "pressure_simulation": True,
    "stroke_connectivity": True
}

# Improved writing style presets
WRITING_STYLES = {
    "clean_neat": {
        "name": "Clean & Neat",
        "pen_thickness": 2,
        "size_variation": 0.9,
        "slant_angle": 0,
        "roughness": 0.2,
        "line_height": 1.6,
        "description": "Perfect for formal documents and clear communication"
    },
    "casual": {
        "name": "Casual Writing",
        "pen_thickness": 2,
        "size_variation": 1.0,
        "slant_angle": 3,
        "roughness": 0.3,
        "line_height": 1.5,
        "description": "Natural everyday handwriting style"
    },
    "elegant": {
        "name": "Elegant Script",
        "pen_thickness": 2,
        "size_variation": 1.1,
        "slant_angle": 8,
        "roughness": 0.25,
        "line_height": 1.7,
        "description": "Beautiful script for special occasions"
    },
    "quick_notes": {
        "name": "Quick Notes",
        "pen_thickness": 3,
        "size_variation": 0.8,
        "slant_angle": -2,
        "roughness": 0.4,
        "line_height": 1.4,
        "description": "Fast note-taking style"
    }
}

# Enhanced character mappings with better paths
IMPROVED_LETTER_PATHS = {
    # More natural letter formations with proper entry/exit points
    "connectivity_points": {
        "a": {"entry": (4, 25), "exit": (20, 36)},
        "b": {"entry": (4, 8), "exit": (18, 32)},
        "c": {"entry": (18, 22), "exit": (18, 32)},
        "d": {"entry": (6, 22), "exit": (20, 36)},
        "e": {"entry": (4, 27), "exit": (18, 32)},
        # ... more connectivity data
    }
}

# Quality enhancement settings
QUALITY_ENHANCEMENTS = {
    "anti_aliasing": True,
    "high_dpi_output": True,
    "smooth_stroke_rendering": True,
    "natural_pressure_variation": True,
    "improved_letter_spacing": True
}

# Paper texture options
PAPER_TEXTURES = {
    "smooth": {"texture_intensity": 0.0, "grain": 0},
    "light": {"texture_intensity": 0.05, "grain": 1},
    "medium": {"texture_intensity": 0.1, "grain": 2},
    "heavy": {"texture_intensity": 0.15, "grain": 3}
}
