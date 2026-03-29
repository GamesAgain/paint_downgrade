from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt6.QtGui import QGuiApplication, QColor, QKeySequence

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
        
        # - Canvas connection
        self.canvas.color_picked_from_canvas.connect(self.on_dropper_color_picked)
        
    def set_triggers(self):
        """Set up menu action triggers."""
        # -- File menu triggers --
        self.file_new.triggered.connect(self.new_file)
        self.file_save_as.triggered.connect(self.save_file)
        self.file_exit.triggered.connect(self.close)
        
        # -- Edit menu triggers --
        self.edit_undo.triggered.connect(self.canvas.undo)
        self.edit_redo.triggered.connect(self.canvas.redo)
        
        # -- Help menu triggers --
        self.help_about.triggered.connect(self.show_about)
        
    # =========================================================
    # Create GUI Components
    # =========================================================
    def create_menu_bar(self):
        """Create the menu bar for the main window."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        edit_menu = menu_bar.addMenu('Edit')
        help_menu = menu_bar.addMenu('Help')
        
        # -- File menu --
        self.file_new = file_menu.addAction('New')
        self.file_save_as = file_menu.addAction('Save As')
        self.file_exit = file_menu.addAction('Exit')
        
        self.file_new.setShortcut(QKeySequence("Ctrl+N"))
        self.file_save_as.setShortcut(QKeySequence("Ctrl+S"))
        
        # -- Edit menu --
        self.edit_undo = edit_menu.addAction('Undo')
        self.edit_redo = edit_menu.addAction('Redo')
        
        self.edit_undo.setShortcut(QKeySequence("Ctrl+Z"))
        self.edit_redo.setShortcut(QKeySequence("Ctrl+Y"))
        
        
        # -- Help menu --
        self.help_about = help_menu.addAction('About')
      
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
        # เคลียร์ประวัติการวาดทั้งหมด
        self.canvas.clear_history()
        self.canvas.update()
    
    def save_file(self):
        # เปิดหน้าต่างให้เลือกที่เซฟไฟล์
        filepath, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Image", 
            "untitled_artwork.png", 
            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
        )
        if filepath:
            # ดึงภาพจากหน้าจอ OpenGL ปัจจุบันไปเซฟ
            image = self.canvas.grabFramebuffer()
            image.save(filepath)
    
    
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
        
    def on_dropper_color_picked(self, color_tuple):
        """รับค่าสีจาก Dropper (0.0 - 1.0) มาแปลงและอัปเดต UI"""
        r, g, b = color_tuple
        # แปลงจาก float (0.0-1.0) กลับเป็น int (0-255) สำหรับ QColor
        qcolor = QColor(int(r * 255), int(g * 255), int(b * 255))
        
        # สั่งให้ ColorPicker อัปเดตสีตัวเอง (จะทำให้อัปเดตปุ่มพรีวิวด้วย)
        self.tool_panel.color_picker.set_color(qcolor)
            
    # =========================================================
    # HELP OPERATIONS
    # =========================================================
    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About Paint Project")
        # ใส่ Mockup 7 คนตรงนี้ ไปแก้ชื่อทีหลังได้เลย
        about_text = """
        <h3>Paint Downgrade Project</h3>
        <p>A ultra-super-high-performance OpenGL painting application.</p>
        <hr>
        <b>Development Team:</b>
        <ul>
            <li><b>1. 66011212224 สรายุทธ บุตรวงษ์:</b>Core Architecture</li>
            <li><b>2. 66011212242 ปารเมศ ศรีจันทร์ชัย:</b> Fill tool implementation</li>
            <li><b>3. 66011212198 เพ็ญพิชชา ดวงตา:</b> Dropper tool implementation</li>
            <li><b>4. 66011212101 ธีรพงศ์ เพ็งแข:</b> Circle tool implementation</li>
            <li><b>5. 66011212039 ยศพล หาญยางนอก:</b> Rectangle tool implementation</li>
            <li><b>6. 66011212148 อรรถชัย ชัยบัณฑิต:</b> Triangle tool implementation</li>
            <li><b>7. 66011212259 ธนกร จีนประโคน:</b> Line tool implementation</li>
        </ul>
        """
        msg.setText(about_text)
        msg.exec()