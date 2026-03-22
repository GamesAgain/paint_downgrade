from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QGuiApplication

from ui.canvas_panel import CanvasPanel
from ui.tool_panel import ToolPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint Project")
        self.setMinimumSize(1000, 700)
        
        self.init_ui() # Initialize UI components
        self.set_triggers() # Set up signal-slot connections
    
    def init_ui(self):
        # -- Create menu bar --
        self.create_menu_bar()
        
        # -- Create central widget --
        self.create_central_widget()
        
        # - Set up connections
        self.set_connections()
        
    def set_connections(self):
        """Set up signal-slot connections."""
        # - Theme change connection
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.on_theme_changed)
        self.tool_panel.tool_selected.connect(self.on_tool_selected)
        self.tool_panel.color_changed.connect(self.on_color_changed)
        self.tool_panel.line_width_changed.connect(self.on_width_changed)
        
    def set_triggers(self):
        """Set up menu action triggers."""
        # -- File menu triggers --
        self.file_new.triggered.connect(self.new_file)
        self.file_open.triggered.connect(self.open_file)
        self.file_save.triggered.connect(self.save_file)
        self.file_save_as.triggered.connect(self.save_as_file)
        self.file_exit.triggered.connect(self.close)
        
        # -- Edit menu triggers --
        # TODO: Implement edit menu triggers
        
    # =========================================================
    # Create GUI Components
    # =========================================================
    def create_menu_bar(self):
        """Create the menu bar for the main window."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        edit_menu = menu_bar.addMenu('Edit')
        view_menu = menu_bar.addMenu('View')
        help_menu = menu_bar.addMenu('Help')
        
        # -- File menu --
        self.file_new = file_menu.addAction('New')
        self.file_open = file_menu.addAction('Open')
        self.file_save = file_menu.addAction('Save')
        self.file_save_as = file_menu.addAction('Save As')
        self.file_exit = file_menu.addAction('Exit')
        
        # -- Edit menu --
        edit_copy = edit_menu.addAction('Copy')
        edit_cut = edit_menu.addAction('Cut')
        edit_paste = edit_menu.addAction('Paste')
        edit_undo = edit_menu.addAction('Undo')
        edit_redo = edit_menu.addAction('Redo')
        
        # -- View menu --
        view_zoom = view_menu.addMenu('Zoom')
        view_zoom_in = view_zoom.addAction('Zoom In')
        view_zoom_out = view_zoom.addAction('Zoom Out')
        view_zoom_reset = view_zoom.addAction('Zoom Reset')
        view_fullscreen = view_menu.addAction('Fullscreen')
        
        # -- Help menu --
        help_about = help_menu.addAction('About')
      
    def create_central_widget(self):
        """Create the central widget with canvas and tools."""
        # Create main widget and layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Create panels
        self.tool_panel = ToolPanel()
        self.canvas = CanvasPanel()
        
        # Add panels to main layout
        main_layout.addWidget(self.tool_panel)
        main_layout.addWidget(self.canvas, 1)
        
        # Set as central widget
        self.setCentralWidget(central_widget)
        
    # =========================================================
    # FILE OPERATIONS
    # =========================================================
    def new_file(self):
        print("New file")
    
    def open_file(self):
        print("Open file")
    
    def save_file(self):
        print("Save file")
    
    def save_as_file(self):
        print("Save as file")
    
    # =========================================================
    # THEME HANDLING
    # =========================================================
    def on_theme_changed(self):
        """Handle system theme changes"""
        self.tool_panel.set_theme_icon()
    
    # =========================================================
    # TOOL HANDLING
    # =========================================================
    def on_tool_selected(self, tool_name: str):
        """Handle tool selection from tool panel"""
        print(f"Main: Tool selected forwarded -> {tool_name}")
        self.canvas.on_tool_selected(tool_name)
        
    def on_color_changed(self, color):
        """Handle color change from color picker"""
        self.canvas.on_color_changed(color)
        
    def on_width_changed(self, width):
        """Handle width change from tool panel"""
        self.canvas.current_width = width