class Styles:
    # Backgrounds
    WINDOW_BACKGROUND = "background-color: #2d2d2d; color: #ffffff;"

    # Labels
    MAIN_LABEL = "QLabel { font: 20px Calibri; color: #b48ead; font-weight: bold;}"
    SUB_LABEL = "QLabel { font: 20px Calibri; color: #b48ead;}"
    VALUE_TEXT = "font-size: 16px; color: #ffffff;"
    LABEL_TEXT = "font-size: 16px; color: #a9a9a9;"

    # Buttons
    BUTTON_BASE = """
        QPushButton {
            font-size: 16px;
            color: #ffffff;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #ffffff;
            }
        """
    
    DISABLED_BUTTON = """
        QPushButton {
            font-size: 16px;
            color: #a9a9a9;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #a9a9a9;
            background-color: #3c3c3c;
            }
        """

    HOVER_BUTTON = f"""
        {BUTTON_BASE}
        QPushButton:hover {{background-color: #555555}}        
        """

    # Combobox
    COMBOBOX_BASE = """
        font-size: 16px; 
        width: 130px; 
        background-color: #3c3c3c; 
        color: #ffffff; 
        border-radius: 5px; 
        border: 1px solid #ffffff; 
        padding: 3px;
        """
    
    @staticmethod
    def create_button_style(brackground_color:str):
        return f"""
            {Styles.BUTTON_BASE}
            QPushButton {{
            background-color: {brackground_color};
            }}
        """
