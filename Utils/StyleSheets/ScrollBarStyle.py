VScrollStyle = """
                QScrollBar:vertical {
                background: none; 
                width:8px;
                border-radius:4px;   
                margin: 40px 0px 40px 0px;
                }
                
                QScrollBar::handle:vertical {
                background:#6666FF;
                border-radius:4px;   
                min-height: 50px;
                }
                
                QScrollBar::handle:vertical:hover {
                background:orange;
                border-radius:4px;   
                min-height: 0px;
                }
                
                QScrollBar::add-line:vertical {
                background: none;
                height: 26px;
                border-radius:4px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                }
                
                QScrollBar::sub-line:vertical {
                background: none;
                height: 26px;
                border-radius:4px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                }

                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                }


                QScrollBar:horizontal {
                background: none;
                height:8px;
                border-radius:4px;   
                margin: 0px 40px 0px 40px;
                }
                
                QScrollBar::handle:horizontal {
                background:#6666FF;
                border-radius:4px;   
                min-width: 50px;
                }
                
                
                QScrollBar::handle:horizontal:hover {
                background:orange;
                border-radius:4px;   
                min-width: 50px;
                }
                
                QScrollBar::add-line:horizontal {
                background: none;
                width: 26px;
                border-radius:4px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                }
                
                QScrollBar::sub-line:horizontal {
                border-radius:4px;
                background: none;
                width: 26px;
                subcontrol-position: top left;
                subcontrol-origin: margin;
                position: absolute;
                }

                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
                }"""

