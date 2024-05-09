mainStyle = '''
            #main_frame {
            background:#1B262C;
            border-radius: 10px;
            }
        
            #main_widget {
            border-radius:10px;
            padding: 0px
            }
            
            #title_widget {
            background-color: #2C394B;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px
            }
            
            
            #left_panel {
            background: #1B262C;
            border-bottom-left-radius:10px;
            }
            
            #logo_text {
            color: white;
            font-size: 12pt;
            
            }
            
            #left_logo_text {
            font-size: 10pt;
            color: white;
            
            }
            
            #export_pdf_button, #save_text_button, #extrakt_button{
            border-radius: 10px;
            background: #2C394B;
            color: white;
            text-align:left;
            letter-spacing: 1px;
            padding-left: 10px;
            }
            
            QToolTip { 
            color: #ffffff; 
            background-color: #2C394B; 
            border: 8px;
            padding:5px;
            }
            
            #left_extrakt_icon {
            background-color: #2C394B;
            border-radius: 30px;
            padding:20px;
            max-width:120px;
            max-height:120px;
            text-align:center;
            }
            
            #left_extrakt_icon:hover {
            background-color: #6666FF;
            text-align:center;
            }
            
            #about_btn {
            border-radius: 10px;
            background: #2C394B;
            color: white;
            text-align:left;
            letter-spacing: 1px;
            padding-left: 10px;
            }
            
            #about_btn:hover{
            border-radius: 10px;
            background: #6666FF;
            color: white;
            padding-left: 10px;
            }
            
            #export_pdf_button:hover,#save_text_button:hover,#extrakt_button:hover{
            border-radius: 10px;
            background: #6666FF;
            color: white;
            padding-left: 10px;
            }
            
            #right_panel {
            background: #1B262C;  
            border-bottom-right-radius:10px; 
               
            }
            
            #select_files,#select_lang{
            background: #2C394B;
            background-color: #2C394B;
            border-radius: 10px;
            color: white;
            padding:10px;
            
            }
            
            #select_files::drop-down,#select_lang::drop-down {
            subcontrol-origin: padding;  
            width: 25px;
            font-size:10pt;
            padding-right:5px;
            font-weight: bold;
            border-left-color: #2C394B;
            
            }
        
            #select_files::down-arrow, #select_lang::down-arrow {
            image: url(images/chevron-down_white.png);
            }
            
            #select_files:!editable:on, #select_lang:!editable:on, 
            #select_files::drop-down:editable:on, #select_lang::drop-down:editable:on {
            background:#6666FF;
            }
            
          QListView {
          background:  #2C394B;
          color: white;
          padding:5px;
          font-size:10pt;
          font-weight:bold;
            }
            
            
            QListView::item:hover {
              background: #6666FF;
            }
                
            #env_edit_text {
            border-radius: 10px;
            background: #2C394B;
            color: #ccc;
            font-size:10pt;
            font-family:'SansSerif';
            letter-spacing: 1px;
            padding: 10px;
            }
            
            #browse_button {
            border-radius: 10px;
            background: #2C394B;
            color: white;
            text-align:left;
            letter-spacing: 1px;
            padding-left: 10px;
            }
            
            #browse_button:hover {
            border-radius: 10px;
            background: #6666FF;
            color: white;
            padding-left: 10px;
            }
            
            #plain_text {
            border-radius: 10px;
            background: #2C394B;
            color: white;
            font-family:'SansSerif';
            font-size:10pt;
            letter-spacing:1.2px;
            padding: 10px;
            }
            
            #search_text_1 {
            color: white;
            font-family:'Forte';
            font-size:16pt;
            font-weight:bold;
            letter-spacing:1.5px;
            }
            
            #search_text_2 , #extract_text_1 {
            font-size:10pt;
            color: #ccc;
            }
            
            #progress_text {
            font-size:10pt;
            color: #92D672;
            }
            #separator {
            color: rgba(44,57,75,0.5);
            }
            
            #menu_separator {
            color: rgba(44,57,75,0.5);
            }
            
           #min_button {
            min-width: 30px;
            min-height: 30px;
            background: #6666FF;
            color: white;
            font-size: 12pt;
            font-weight: bold;
            border-radius: 10px;
            }
            
            #min_button:hover {
            color: #ffffff;
            background: orange;
            font-size: 8pt;
            font-weight: bold;
            border-radius: 10px;
            }
            
            #close_button {
            min-width: 30px;
            min-height: 30px;
            background: #6666FF;
            color: white;
            font-family: "Webdings";
            font-size: 8pt;
            font-weight: bold;
            border-radius: 10px;
            }
            
            #close_button:hover {
            color: #ffffff;
            background: red;
            font-family: "Webdings";
            font-size: 8pt;
            font-weight: bold;
            border-radius: 10px;
            }
        
        #logo_text {
        font-size: 10pt;
        letter-spacing:1px;
        font-weight: bold;
        }
        
        #status_bar {
        background-color: #2C394B;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px
        }
        
        #status_label{
        color:#ccc;
        padding: 10px;
        font-size:8pt;
        }
            '''

splashStyle = '''
        #splash_logo_text {
            font-size: 12pt;
            color: #ccc;
            letter-spacing:1px;
            font-weight: bold;
        }
        #desc_label {
            font-size: 8pt;
            color: rgba(102, 102, 255, 0.8);
            opacity: 0.2;
        }
        
        #version_label {
            font-size: 8pt;
            color: rgba(232, 232, 235, 0.5);
        }
        
        #loading_label {
            font-size: 30px;
            color: #e8e8eb;
        }
        #splash_frame {
            background-color: #1B262C;
            color: #c8c8c8;
            box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
            border-radius: 10px
        }
        QProgressBar {
            background-color: #000000;
            color: #6666FF;
            border-style: none;
            border-radius: 5px;
            
        }
        QProgressBar::chunk {
            border-radius: 5px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #6666FF);
        }
'''