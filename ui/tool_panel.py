from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QGroupBox, QSlider, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon

from ui.color_picker import ColorPicker
from utils.load_icon import load_icon_path

ICON_SIZE = QSize(20, 20)

class ToolPanel(QWidget):
    line_width_changed = pyqtSignal(int)
    color_changed = pyqtSignal(tuple)
    tool_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.setFixedWidth(160)
        self.line_width = 1
        self.color = (0, 0, 0)
        
        self.init_ui()
    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create sections
        drawing_tools_section = self.create_drawing_tools_section()
        shape_tools_section = self.create_shape_tools_section()
        line_width_section = self.create_line_width_section()
        color_picker_section = self.create_color_picker_section()
        
        # Add sections to main layout
        main_layout.addWidget(drawing_tools_section)
        main_layout.addWidget(shape_tools_section)
        main_layout.addWidget(line_width_section)
        main_layout.addWidget(color_picker_section)
        
        # Set theme and connect signals
        self.set_theme_icon()
        self.set_connect_tool_signals()
        
    def create_drawing_tools_section(self):
        box = QGroupBox("Drawing Tools")
        layout = QGridLayout()
        
        # -- Pen Tool --
        self.pen_button = QPushButton()
        self.pen_button.setCheckable(True)
        self.pen_button.setChecked(True) # default selected tool
        layout.addWidget(self.pen_button, 0, 0)
        
        # -- Fill Tool --
        self.fill_button = QPushButton()
        self.fill_button.setCheckable(True)
        layout.addWidget(self.fill_button, 0, 1)
        
        # -- Eraser Tool --
        self.eraser_button = QPushButton()
        self.eraser_button.setCheckable(True)
        layout.addWidget(self.eraser_button, 1, 0)
        
        # -- Dropper Tool --
        self.dropper_button = QPushButton()
        self.dropper_button.setCheckable(True)
        layout.addWidget(self.dropper_button, 1, 1)
    
        box.setLayout(layout)
        return box
    
    def create_shape_tools_section(self):
        box = QGroupBox("Shape Tools")
        layout = QGridLayout()
        
        # -- Line Tool --
        self.line_button = QPushButton()
        self.line_button.setCheckable(True)
        layout.addWidget(self.line_button, 0, 0)
        
        # -- Rectangle Tool --
        self.rectangle_button = QPushButton()
        self.rectangle_button.setCheckable(True)
        layout.addWidget(self.rectangle_button, 0, 1)
        
        # -- Circle Tool --
        self.circle_button = QPushButton()
        self.circle_button.setCheckable(True)
        layout.addWidget(self.circle_button, 1, 0)
        
        # -- Triangle Tool --
        self.triangle_button = QPushButton()
        self.triangle_button.setCheckable(True)
        layout.addWidget(self.triangle_button, 1, 1)
        
        box.setLayout(layout)
        return box
    
    def create_line_width_section(self):
        box = QGroupBox("Line Width")
        layout = QVBoxLayout()
        
        # -- Line Width Input --
        line_width = QWidget()
        hlayout = QHBoxLayout(line_width)
        self.line_width_label = QLabel("Line Width:")
        self.line_width_edit = QLineEdit("1")
        self.line_width_edit.setFixedWidth(30)
        hlayout.addWidget(self.line_width_label)
        hlayout.addWidget(self.line_width_edit)
        
        # -- Line Width Slider --
        self.line_width_slider = QSlider(Qt.Orientation.Horizontal)
        self.line_width_slider.setMinimum(1)
        self.line_width_slider.setMaximum(10)
        self.line_width_slider.setValue(1)
        
        # -- Connect Signals --
        self.line_width_slider.valueChanged.connect(self.on_line_width_changed)
        self.line_width_edit.textChanged.connect(self.on_line_width_text_changed)
        layout.addWidget(line_width)
        layout.addWidget(self.line_width_slider)
        
        box.setLayout(layout)
        return box
        
    def create_color_picker_section(self):
        box = QGroupBox("Color Tools")
        layout = QVBoxLayout()
        
        self.color_picker = ColorPicker()
        layout.addWidget(self.color_picker)
        
        box.setLayout(layout)
        return box
    
    def set_connect_tool_signals(self):
        self.tool_buttons = [
            self.pen_button, self.fill_button, 
            self.eraser_button, self.dropper_button,
            self.line_button, self.rectangle_button,
            self.circle_button, self.triangle_button
        ]
        
        self.pen_button.clicked.connect(lambda checked, t='pen': self.select_tool(t))
        self.fill_button.clicked.connect(lambda checked, t='fill': self.select_tool(t))
        self.eraser_button.clicked.connect(lambda checked, t='eraser': self.select_tool(t))
        self.dropper_button.clicked.connect(lambda checked, t='dropper': self.select_tool(t))
        self.line_button.clicked.connect(lambda checked, t='line': self.select_tool(t))
        self.rectangle_button.clicked.connect(lambda checked, t='rectangle': self.select_tool(t))
        self.circle_button.clicked.connect(lambda checked, t='circle': self.select_tool(t))
        self.triangle_button.clicked.connect(lambda checked, t='triangle': self.select_tool(t))
        
        # Connect color picker signal
        self.color_picker.color_changed.connect(self.color_changed.emit)
    
    def set_theme_icon(self):
        self.icon_path = load_icon_path()
        
        # (ส่วนตั้งค่า Icon เหมือนเดิม)
        self.pen_button.setIcon(QIcon(self.icon_path + "pencil_icon.svg"))
        self.pen_button.setIconSize(ICON_SIZE)
        self.pen_button.setToolTip("Pen Tool (P)")
        
        self.fill_button.setIcon(QIcon(self.icon_path + "bucket_icon.svg"))
        self.fill_button.setIconSize(ICON_SIZE)
        self.fill_button.setToolTip("Fill Tool (F)")
        
        self.eraser_button.setIcon(QIcon(self.icon_path + "eraser_icon.svg"))
        self.eraser_button.setIconSize(ICON_SIZE)
        self.eraser_button.setToolTip("Eraser Tool (E)")
        
        self.dropper_button.setIcon(QIcon(self.icon_path + "dropper_icon.svg"))
        self.dropper_button.setIconSize(ICON_SIZE)
        self.dropper_button.setToolTip("Color Dropper Tool (D)")
        
        self.line_button.setIcon(QIcon(self.icon_path + "line_icon.svg"))
        self.line_button.setIconSize(ICON_SIZE)
        self.line_button.setToolTip("Line Tool")
        
        self.rectangle_button.setIcon(QIcon(self.icon_path + "square_icon.svg"))
        self.rectangle_button.setIconSize(ICON_SIZE)
        self.rectangle_button.setToolTip("Rectangle Tool")
        
        self.circle_button.setIcon(QIcon(self.icon_path + "circle_icon.svg"))
        self.circle_button.setIconSize(ICON_SIZE)
        self.circle_button.setToolTip("Circle Tool")
        
        self.triangle_button.setIcon(QIcon(self.icon_path + "triangle_icon.svg"))
        self.triangle_button.setIconSize(ICON_SIZE)
        self.triangle_button.setToolTip("Triangle Tool")
            
    # Line Width Handlers
    def on_line_width_changed(self, width):
        self.line_width_edit.setText(str(width))
        self.line_width_changed.emit(width)
        
    def on_line_width_text_changed(self, text):
        try:
            width = int(text)
            self.line_width_slider.setValue(width)
            self.line_width_changed.emit(width)
        except ValueError:
            pass
        
    def select_tool(self, tool_name: str):
        # 1. Uncheck ทุกปุ่ม
        for button in self.tool_buttons:
            button.setChecked(False)
        
        # 2. Check ปุ่มที่เลือก
        if tool_name == 'pen':
            self.pen_button.setChecked(True)
        elif tool_name == 'fill':
            self.fill_button.setChecked(True)
        elif tool_name == 'eraser':
            self.eraser_button.setChecked(True)
        elif tool_name == 'dropper':
            self.dropper_button.setChecked(True)
        elif tool_name == 'line':
            self.line_button.setChecked(True)
        elif tool_name == 'rectangle':
            self.rectangle_button.setChecked(True)
        elif tool_name == 'circle':
            self.circle_button.setChecked(True)
        elif tool_name == 'triangle':
            self.triangle_button.setChecked(True)
        
        # 3. ส่ง signal ไปบอก canvas ให้เปลี่ยน tool
        self.tool_selected.emit(tool_name)