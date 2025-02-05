class Styles:
    # Backgrounds
    WINDOW_BACKGROUND = "background-color: #2d2d2d; color: #ffffff;"

    # Scaling factor for app sizing
    SCALE_FACTOR = 2 # USE AN INT VALUE

    # Labels
    MAIN_LABEL = f"QLabel {{ font: {20 * SCALE_FACTOR}px Calibri; color: #b48ead; font-weight: bold;}}"
    SUB_LABEL = f"QLabel {{ font: {20 * SCALE_FACTOR}px Calibri; color: #b48ead;}}"
    VALUE_TEXT = f"font-size: {16 * SCALE_FACTOR}px; color: #ffffff;"
    LABEL_TEXT = f"font-size: {16 * SCALE_FACTOR}px; color: #a9a9a9;"

    # Buttons
    BUTTON_BASE = f"""
        QPushButton {{
            font-size: {16 * SCALE_FACTOR}px;
            color: #ffffff;
            padding: {5 * SCALE_FACTOR}px;
            border-radius: {5 * SCALE_FACTOR}px;
            border: {1 * SCALE_FACTOR}px solid #ffffff;
        }}
    """
    
    DISABLED_BUTTON = f"""
        QPushButton {{
            font-size: {16 * SCALE_FACTOR}px;
            color: #a9a9a9;
            padding: {5 * SCALE_FACTOR}px;
            border-radius: {5 * SCALE_FACTOR}px;
            border: {1 * SCALE_FACTOR}px solid #a9a9a9;
            background-color: #3c3c3c;
        }}
    """

    HOVER_BUTTON = f"""
        {BUTTON_BASE}
        QPushButton:hover {{background-color: #555555}}        
        """

    # Combobox
    COMBOBOX_BASE = f"""
        font-size: {16 * SCALE_FACTOR}px; 
        width: {130 * SCALE_FACTOR}px; 
        background-color: #3c3c3c; 
        color: #ffffff; 
        border-radius: {5 * SCALE_FACTOR}px; 
        border: {1 * SCALE_FACTOR}px solid #ffffff; 
        padding: {3 * SCALE_FACTOR}px;
        """
    
    # Slider
    SLIDER = f"""
        QSlider::groove:horizontal {{
            background: #3c3c3c;
            height: {10 * SCALE_FACTOR}px;  
        }}
        QSlider::handle:horizontal {{
            background: #b48ead;
            width: {20 * SCALE_FACTOR}px;  
            margin: {-5 * SCALE_FACTOR}px 0;
        }}
"""

    
    @staticmethod
    def create_button_style(brackground_color:str):
        return f"""
            {Styles.BUTTON_BASE}
            QPushButton {{
            background-color: {brackground_color};
            }}
        """
