from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QColorDialog, QGridLayout)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor


class ColorPicker(QWidget):
    """
    Color selection widget for the paint project
    """
    
    # Signal emitted when color changes (ส่งค่าเป็น Tuple ทศนิยม 0.0 - 1.0)
    color_changed = pyqtSignal(tuple)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_color = QColor(0, 0, 0)  # Default black
        
        # Predefined colors
        self.predefined_colors = [
            QColor(0, 0, 0),        # Black
            QColor(255, 255, 255),  # White
            QColor(255, 0, 0),      # Red
            QColor(0, 255, 0),      # Green
            QColor(0, 0, 255),      # Blue
            QColor(255, 255, 0),    # Yellow
            QColor(255, 0, 255),    # Magenta
            QColor(0, 255, 255),    # Cyan
            QColor(128, 128, 128),  # Gray
            QColor(255, 165, 0),    # Orange
            QColor(128, 0, 128),    # Purple
            QColor(165, 42, 42),    # Brown
            QColor(255, 192, 203),  # Pink
            QColor(255, 215, 0),    # Gold
            QColor(0, 128, 0),      # Dark Green
            QColor(75, 0, 130),     # Indigo
            QColor(220, 20, 60),    # Crimson
            QColor(255, 105, 180),  # Hot Pink
            QColor(139, 69, 19),    # SaddleBrown
            QColor(128, 128, 0),    # Olive
            QColor(139, 0, 0),      # Dark Red
            QColor(0, 100, 0),      # Dark Green
            QColor(0, 0, 139),      # Dark Blue
            QColor(128, 0, 128),    # Dark Purple
        ]
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the color picker UI."""
        layout = QVBoxLayout()
        
        # Current color preview
        self.color_button = QPushButton()
        self.color_button.setFixedSize(60, 30)
        self.color_button.clicked.connect(self.open_color_dialog)
        self.update_color_button()
        
        # Color preview layout
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("Current:"))
        preview_layout.addWidget(self.color_button)
        preview_layout.addStretch()
        layout.addLayout(preview_layout)
        
        # Predefined colors grid
        colors_label = QLabel("Quick Colors:")
        layout.addWidget(colors_label)
        
        colors_layout = QGridLayout()
        colors_layout.setSpacing(2)
        
        columns = 4
        for index, color in enumerate(self.predefined_colors):
            row = index // columns
            col = index % columns
            color_button = self.create_color_swatch(color)
            colors_layout.addWidget(color_button, row, col)
        
        layout.addLayout(colors_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_color_swatch(self, color: QColor) -> QPushButton:
        """Create a color swatch button."""
        button = QPushButton()
        button.setFixedSize(25, 25)
        button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
        
        button.clicked.connect(lambda checked, c=color: self.set_color(c))
        
        return button
    
    def update_color_button(self):
        """Update the color preview button."""
        self.color_button.setStyleSheet(
            f"background-color: {self.current_color.name()}; "
            f"border: 2px solid black;"
        )
    
    def open_color_dialog(self):
        """Open the color selection dialog."""
        color = QColorDialog.getColor(self.current_color, self, "Select Color")
        if color.isValid():
            self.set_color(color)
    
    def set_color(self, color: QColor):
        """Set the current color and emit normalized RGB."""
        self.current_color = color
        self.update_color_button()
        
        r, g, b, _ = color.getRgbF()
        self.color_changed.emit((r, g, b))
    
    def get_color(self) -> QColor:
        """Get the current color."""
        return self.current_color