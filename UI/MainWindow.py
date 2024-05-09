from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QIcon, QMovie
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, \
    QSizePolicy, QLabel, QFrame, QLineEdit, QComboBox, QPlainTextEdit, QProgressBar

from Utils.Const import *
from Utils.StyleSheets.MainWindowStyle import mainStyle
from Utils.StyleSheets.ScrollBarStyle import VScrollStyle


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.openfile = True
        self.progressValue = 0
        self.multiExport = False
        self.isExtracting = False
        self.isPdf = False
        self.files_list = []
        self.extractResults = {}

        self.setWindowIcon(QIcon('images/logo_32_blue.png'))
        self.setObjectName('main_widget')
        self.setWindowTitle(AppName)
        self.setMinimumSize(QSize(1200, 768))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet(mainStyle)

        from Controllers.main_controller import MainController
        self.mcontrol = MainController(self)

        self.mcontrol.centerWindow()

        layout = QVBoxLayout()

        self.setLayout(layout)

        # main screen frame
        self.frame = QFrame(self)
        self.frame.setObjectName('main_frame')
        self.frame.setMinimumSize(1200, 768)
        layout.addWidget(self.frame)
        self.setCentralWidget(self.frame)
        # Main Layout
        self.main_layout = QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(10, 50, 0, 0)

        # Logo Widget
        self.logo_layout = QHBoxLayout(self.frame)
        self.logo_text = QLabel(AppName)
        self.logo_text.setObjectName('logo_text')

        self.logo_icon = QLabel()
        self.logo_icon.setObjectName('logo_icon')

        self.logo_pix = QPixmap('images/logo_24_blue.png')
        self.logo_icon.setPixmap(self.logo_pix)
        self.logo_layout.addWidget(self.logo_icon)
        self.logo_layout.addWidget(self.logo_text)

        self.closeButton = QPushButton('r')
        self.closeButton.setObjectName('close_button')
        self.closeButton.setToolTip('Close window')
        self.closeButton.clicked.connect(self.mcontrol.closeWindow)

        self.minButton = QPushButton()
        self.minButton.setIcon(QIcon('images/chevron-down_white.png'))
        self.minButton.setToolTip('Minimize window')
        self.minButton.setIconSize(QSize(24, 24))
        self.minButton.setObjectName('min_button')
        self.minButton.clicked.connect(self.mcontrol.minimizeWindow)

        self.title_widget = QWidget(self.frame)
        self.title_widget.setObjectName('title_widget')
        self.title_widget.setMinimumSize(1200, 50)

        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setObjectName('title_layout')
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_layout.addLayout(self.logo_layout)
        self.title_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.title_layout.addWidget(self.minButton)
        self.title_layout.addSpacing(5)
        self.title_layout.addWidget(self.closeButton)
        self.main_layout.addLayout(self.title_layout)

        self.body_layout = QHBoxLayout()
        self.main_layout.addLayout(self.body_layout)

        # Logo widget
        left_panel = QWidget(self.frame)
        left_panel.setObjectName('left_panel')
        left_panel.setContentsMargins(0, 50, 0, 0)
        self.left_layout = QVBoxLayout(left_panel)
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left_logo_text = QLabel('Click to extract text')
        self.left_logo_text.setObjectName('left_logo_text')
        self.left_logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.extrakt_button = QPushButton()
        self.extrakt_button.setObjectName('left_extrakt_icon')
        self.extrakt_button.setToolTip('Click to start extraction.')
        self.extrakt_button.setIcon(QIcon('images/extrakt_icon.png'))
        self.extrakt_button.setIconSize(QSize(80,80))
        self.left_layout.addWidget(self.extrakt_button,0,Qt.AlignmentFlag.AlignCenter)
        # self.left_layout.addWidget(self.left_logo_text)
        self.extrakt_button.clicked.connect(self.mcontrol.extrakt_thread)

        self.menu_layout = QVBoxLayout(left_panel)
        self.menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addLayout(self.menu_layout)

        menu_separator = QFrame(self.frame)
        menu_separator.setObjectName('menu_separator')
        menu_separator.setFrameShape(QFrame.Shape.HLine)
        self.menu_layout.addSpacing(20)
        self.menu_layout.addWidget(menu_separator)

        self.menu_layout.addSpacing(20)

        """
        self.lang_box = QComboBox(self.frame)
        self.lang_box.setObjectName('select_lang')
        self.lang_box.setMinimumSize(250, 50)
        #print(os.environ['XRAKT_LANGUAGE'])
        if os.environ.get('XRAKT_LANGUAGE'):
            val_index = list(languages.values()).index(os.environ.get('XRAKT_LANGUAGE'))
            key_name = list(languages)[val_index]
            self.lang_box.setPlaceholderText(key_name)
        else:
            self.lang_box.setPlaceholderText('Choose Language (Default : English)')
        self.lang_box.addItems(sorted(languages))
        self.lang_box.currentTextChanged.connect(self.mcontrol.selectLang)
        self.menu_layout.addWidget(self.lang_box)
        """

        self.export_options = QComboBox(self.frame)
        self.export_options.setObjectName('select_lang')
        self.export_options.setToolTip('Choose to export in single or multiple files.')
        self.export_options.setFixedSize(280, 50)
        self.export_options.setPlaceholderText('Choose export option (Default : Single file)')
        self.export_options.addItem("Single file")
        self.export_options.addItem("Multiple files")
        self.export_options.currentIndexChanged.connect(self.mcontrol.selectExportOptions)
        self.menu_layout.addSpacing(10)
        self.menu_layout.addWidget(self.export_options)
        self.export_options.hide()

        self.export_pdf = QPushButton('Export as pdf')
        self.export_pdf.setMinimumSize(280, 50)
        self.export_pdf.setIcon(QIcon('images/pdf_file.png'))
        self.export_pdf.setIconSize(QSize(36, 36))
        self.export_pdf.setObjectName('export_pdf_button')
        self.export_pdf.setToolTip('Export result in single or multiple pdf files.')
        self.menu_layout.addSpacing(10)
        self.menu_layout.addWidget(self.export_pdf)
        self.export_pdf.clicked.connect(self.mcontrol.exportPdf)

        # Save as Text Button
        self.save_txt_button = QPushButton('Save as text file', )
        self.save_txt_button.setToolTip('Save result in a single or multiple text files.')
        self.save_txt_button.setObjectName('save_text_button')
        self.save_txt_button.setMinimumSize(280, 50)
        self.save_txt_button.setIcon(QIcon('images/text_file.png'))
        self.save_txt_button.setIconSize(QSize(36, 36))
        self.menu_layout.addSpacing(10)
        self.menu_layout.addWidget(self.save_txt_button)
        self.save_txt_button.clicked.connect(self.mcontrol.saveText)

        self.about_btn = QPushButton('About')
        self.about_btn.setMinimumSize(280, 50)
        self.about_btn.setObjectName('about_btn')
        self.about_btn.setToolTip('Show About')
        self.about_btn.setIcon(QIcon('images/information.png'))
        self.about_btn.setIconSize(QSize(36, 36))
        self.menu_layout.addSpacing(10)
        self.menu_layout.addWidget(self.about_btn)
        self.about_btn.clicked.connect(self.mcontrol.openAbout)

        # Content Panel
        right_panel = QWidget(self.frame)
        right_panel.setObjectName('right_panel')

        layout_separator = QFrame(self.frame)
        layout_separator.setObjectName('separator')
        layout_separator.setFrameShape(QFrame.Shape.VLine)
        self.body_layout.addWidget(left_panel, 1)
        self.body_layout.addWidget(layout_separator)

        # Env Path
        self.right_layout = QVBoxLayout(right_panel)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.env_path = QLineEdit()

        self.location_layout = QHBoxLayout()

        self.file_folder = QComboBox(self.frame)
        self.file_folder.setObjectName('select_files')
        self.file_folder.setToolTip('Choose to select single or multiple files.')
        self.file_folder.setFixedSize(120, 50)
        self.file_folder.addItem("Single file")
        self.file_folder.addItem("Multiple files")
        self.file_folder.currentIndexChanged.connect(self.mcontrol.selectFileBox)

        self.location_layout.addWidget(self.file_folder)

        self.env_path.setObjectName('env_edit_text')
        self.env_path.setFixedSize(600,50)
        self.env_path.setPlaceholderText('Select image file or folder location...')

        self.location_layout.addWidget(self.env_path)

        self.browse_button = QPushButton('Browse')
        self.browse_button.setToolTip('Select one or more files')
        self.browse_button.setObjectName('browse_button')
        self.browse_button.setFixedSize(120, 50)
        self.browse_button.setIcon(QIcon('images/folder.png'))
        self.browse_button.setIconSize(QSize(36, 36))
        self.browse_button.clicked.connect(self.mcontrol.openExplorer)

        self.right_layout.addLayout(self.location_layout)
        self.location_layout.addWidget(self.browse_button)

        self.right_layout.addSpacing(10)

        # Plain text Widget
        # ------------------------------------------
        self.plain_text = QPlainTextEdit(self.frame)
        self.plain_text.setObjectName('plain_text')
        self.plain_text.setFixedSize(850, 580)
        self.plain_text.setLineWrapMode(self.plain_text.LineWrapMode.WidgetWidth)
        self.plain_text.setVerticalScrollBar(self.plain_text.setStyleSheet(VScrollStyle))
        self.plain_text.setPlaceholderText('Results will be displayed here...')
        self.plain_text.setReadOnly(True)
        #self.plain_text.textChanged.connect(lambda: self.mcontrol.hideShow(RightLayout.RESULT))
        self.plain_text.hide()

        # Search Layout
        # ------------------------------------------
        self.search_layout = QVBoxLayout(self.frame)
        self.search_frame = QFrame()
        self.search_frame.setLayout(self.search_layout)

        self.search_img = QLabel()
        self.search_img.setObjectName('search_img')
        self.search_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_img.setPixmap(QPixmap('images/search.png'))

        self.search_text_1 = QLabel(SearchText)
        self.search_text_1.setObjectName('search_text_1')

        self.search_text_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search_text_2 = QLabel(SearchText2)
        self.search_text_2.setObjectName('search_text_2')
        self.search_text_2.setWordWrap(True)
        self.search_text_2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.search_layout.addWidget(self.search_img)
        self.search_layout.addWidget(self.search_text_1)
        self.search_layout.addWidget(self.search_text_2)
        # self.search_frame.hide()

        # Vertical Right Layout
        self.rightVLayout = QVBoxLayout(self.frame)
        self.rightVLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Extracting Layout
        # ------------------------------------------
        self.extract_layout = QVBoxLayout()
        self.extract_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.extract_frame = QFrame()
        self.extract_frame.setLayout(self.extract_layout)

        self.extract_img = QLabel()
        self.extract_img.setObjectName('search_img')
        self.extract_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie("images/loader_folder.gif")
        self.extract_img.setScaledContents(True)
        self.extract_img.setFixedSize(300, 300)
        self.movie.start()
        self.extract_img.setMovie(self.movie)
        self.extract_text_1 = QLabel('Extracting from: None')
        self.extract_text_1.setObjectName('extract_text_1')
        self.extract_text_1.resize(QSize(400, 400))
        self.extract_text_1.setWordWrap(True)
        self.extract_text_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.extract_layout.addWidget(self.extract_img)
        self.extract_layout.addWidget(self.extract_text_1)
        self.extract_layout.addSpacing(30)
        self.extract_frame.hide()

        self.fileProgress = QProgressBar()
        self.fileProgress.setFixedSize(self.width() // 4, 4)
        self.fileProgress.adjustSize()
        self.fileProgress.setTextVisible(False)
        self.fileProgress.setRange(0, len(self.files_list))
        self.fileProgress.setValue(0)

        self.progressVLayout = QVBoxLayout()
        self.progressVLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressHLayout = QHBoxLayout()
        self.progressHLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.extract_text_2 = QLabel('No Files')
        self.extract_text_2.setObjectName('extract_text_1')
        self.extract_text_2.setWordWrap(True)
        self.extract_text_2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.progressText = QLabel('0% completed')
        self.progressText.setObjectName('progress_text')
        self.progressText.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progressHLayout.addWidget(self.extract_text_2)

        self.progressHLayout.addWidget(self.progressText)
        self.extract_layout.addWidget(self.fileProgress)
        self.extract_layout.addLayout(self.progressHLayout)
        self.rightVLayout.addLayout(self.extract_layout)

        # ------------------------------------------
        self.right_layout.addWidget(self.plain_text)
        self.right_layout.addWidget(self.search_frame)
        self.right_layout.addWidget(self.extract_frame)
        self.right_layout.addSpacing(10)
        self.body_layout.addWidget(right_panel, 3)

        # Status Bar
        status_bar_widget = QWidget(self.frame)
        status_bar_widget.setObjectName('status_bar')
        status_bar_widget.setGeometry(0, 733, 0, 0)
        status_bar_widget.setMinimumSize(1200, 35)
        status_bar_layout = QHBoxLayout(status_bar_widget)
        status_bar_layout.setContentsMargins(0, 0, 0, 0)

        status_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label1 = QLabel('Status : Not Run')
        status_label2 = QLabel(AppVersion)
        self.status_label1.setObjectName('status_label')
        status_label2.setObjectName('status_label')
        status_bar_layout.addWidget(self.status_label1)
        status_bar_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        status_bar_layout.addWidget(status_label2)

        self.main_layout.addLayout(status_bar_layout)
        self.mcontrol.initThread()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = QPoint()

    def mouseMoveEvent(self, event):
        try:
            if not self.__press_pos.isNull():
                self.move(self.pos() + (event.pos() - self.__press_pos))

        except:
            pass
