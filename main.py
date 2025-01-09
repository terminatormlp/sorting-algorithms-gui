import math
import sys
import random
import time
from typing import List, Type
from enum import Enum, auto
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QSpinBox, QLabel, QFrame, QSlider,
    QStyle, QStyleFactory, QMessageBox, QGroupBox, QRadioButton,
    QStatusBar, QToolBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QSize
from PyQt6.QtGui import (
    QPainter, QColor, QPalette, QPen, QAction
)
import inspect
from typing import List, Type
from algorithms import *
from plugin_loader import PluginLoader

def discover_sorting_algorithms() -> List[Type]:
    """
    Automatically discovers all sorting algorithm classes defined in algorithms.py
    Returns a list of sorting algorithm classes that inherit from SortingAlgorithm
    """
    algorithms = []
    
    # Get all objects from algorithms module
    for name, obj in inspect.getmembers(sys.modules['algorithms']):
        # Check if it's a class and inherits from SortingAlgorithm
        if (inspect.isclass(obj) and 
            obj != SortingAlgorithm and  # Exclude the base class
            issubclass(obj, SortingAlgorithm)):
            algorithms.append(obj)
    
    return sorted(algorithms, key=lambda x: x().name())  # Sort by algorithm name

# Enums for visualization styles
class VisualizationStyle(Enum):
    BARS = auto()
    DOTS = auto()
    SCATTER = auto()
    CIRCULAR = auto()

class ColorTheme(Enum):
    CLASSIC = {
        "background": QColor(40, 44, 52),
        "primary": QColor(97, 175, 239),
        "secondary": QColor(152, 195, 121),
        "highlight": QColor(224, 108, 117),
        "text": QColor(171, 178, 191)
    }
    SUNSET = {
        "background": QColor(44, 62, 80),
        "primary": QColor(231, 76, 60),
        "secondary": QColor(241, 196, 15),
        "highlight": QColor(230, 126, 34),
        "text": QColor(236, 240, 241)
    }
    FOREST = {
        "background": QColor(27, 40, 56),
        "primary": QColor(46, 204, 113),
        "secondary": QColor(52, 152, 219),
        "highlight": QColor(155, 89, 182),
        "text": QColor(236, 240, 241)
    }

# Enhanced visualization widget
class VisualizerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = None
        self.style = VisualizationStyle.BARS
        self.theme = ColorTheme.CLASSIC
        self.setMinimumSize(800, 500)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setAutoFillBackground(True)
        self.updateTheme()
    
    def updateTheme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self.theme.value["background"])
        self.setPalette(palette)
    
    def setState(self, state: SortingState):
        self.state = state
        self.update()
    
    def setStyle(self, style: VisualizationStyle):
        self.style = style
        self.update()
    
    def setTheme(self, theme: ColorTheme):
        self.theme = theme
        self.updateTheme()
        self.update()
    
    def paintEvent(self, event):
        if not self.state:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.style == VisualizationStyle.BARS:
            self.drawBars(painter)
        elif self.style == VisualizationStyle.DOTS:
            self.drawDots(painter)
        elif self.style == VisualizationStyle.SCATTER:
            self.drawScatter(painter)
        elif self.style == VisualizationStyle.CIRCULAR:
            self.drawCircular(painter)
    
    def drawBars(self, painter: QPainter):
        width = self.width()
        height = self.height()
        n = len(self.state.array)
        
        # Calculate padding and convert to integer
        PADDING = int(min(max(10, width * 0.02), 20))
        available_width = width - (2 * PADDING)
        
        # Calculate bar width and ensure it's at least 1 pixel
        bar_width = max(1, int(available_width / n))
        gap = min(1, int(bar_width * 0.1))  # Gap is 10% of bar width, but not more than 1 pixel
        
        # Scale height to use full available space
        max_val = max(self.state.array)
        available_height = height - 60  # Reserve space for labels
        height_scale = available_height / max_val
        
        for i in range(n):
            val = self.state.array[i]
            bar_height = int(val * height_scale)
            x = int(PADDING + (i * bar_width))
            y = int(height - 30 - bar_height)
            
            # Set color based on state
            if i in self.state.sorted_indices:
                color = self.theme.value["secondary"]
            elif i in self.state.highlighted_indices:
                color = self.theme.value["highlight"]
            elif i in self.state.compared_indices:
                color = self.theme.value["highlight"]
            else:
                color = self.theme.value["primary"]
            
            # Draw bar with integer coordinates
            painter.fillRect(x + gap, y, max(1, bar_width - 2*gap), bar_height, color)
            
            # Only draw values if there's enough space
            if bar_width > 15:
                painter.setPen(self.theme.value["text"])
                painter.drawText(x, y - 15, bar_width, 20,
                               Qt.AlignmentFlag.AlignCenter, str(val))

    def drawDots(self, painter: QPainter):
        width = self.width()
        height = self.height()
        n = len(self.state.array)
        
        # Use full width with minimal padding
        PADDING = int(min(max(10, width * 0.02), 20))
        available_width = width - (2 * PADDING)
        spacing = available_width / (n - 1) if n > 1 else available_width
        
        max_val = max(self.state.array)
        available_height = height - 60
        height_scale = available_height / max_val
        
        # Adjust dot size based on spacing but keep it reasonable
        dot_size = int(min(spacing * 0.8, 20))
        
        for i, val in enumerate(self.state.array):
            y = int(height - 30 - (val * height_scale))
            x = int(PADDING + (i * spacing))
            
            if i in self.state.sorted_indices:
                color = self.theme.value["secondary"]
            elif i in self.state.highlighted_indices:
                color = self.theme.value["highlight"]
            elif i in self.state.compared_indices:
                color = self.theme.value["highlight"]
            else:
                color = self.theme.value["primary"]
            
            # Draw connecting lines first
            if i > 0:
                prev_y = int(height - 30 - (self.state.array[i-1] * height_scale))
                prev_x = int(PADDING + ((i-1) * spacing))
                painter.setPen(QPen(color.lighter(), 1))
                painter.drawLine(prev_x, prev_y, x, y)
            
            # Draw dots with integer coordinates
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(x - dot_size//2, y - dot_size//2, dot_size, dot_size)

    def drawScatter(self, painter: QPainter):
        width = self.width()
        height = self.height()
        n = len(self.state.array)
        
        # Use full width with minimal padding
        PADDING = int(min(max(10, width * 0.02), 20))
        available_width = width - (2 * PADDING)
        
        max_val = max(self.state.array)
        available_height = height - 60
        height_scale = available_height / max_val
        
        # Adjust dot size based on available space
        dot_size = int(min(available_width / n * 0.8, 15))
        
        for i, val in enumerate(self.state.array):
            x = int(PADDING + (i * available_width / (n-1) if n > 1 else available_width/2))
            y = int(height - 30 - (val * height_scale))
            
            if i in self.state.sorted_indices:
                color = self.theme.value["secondary"]
            elif i in self.state.highlighted_indices:
                color = self.theme.value["highlight"]
            elif i in self.state.compared_indices:
                color = self.theme.value["highlight"]
            else:
                color = self.theme.value["primary"]
            
            # Draw vertical guide line
            painter.setPen(QPen(self.theme.value["text"], 1, Qt.PenStyle.DotLine))
            painter.drawLine(x, height - 30, x, y)
            
            # Draw dot with integer coordinates
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(x - dot_size//2, y - dot_size//2, dot_size, dot_size)

    def drawCircular(self, painter: QPainter):
        width = self.width()
        height = self.height()
        n = len(self.state.array)
        
        # Calculate center and radius
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2 - 40
        
        max_val = max(self.state.array)
        
        # Calculate angle step to distribute elements evenly
        angle_step = 2 * math.pi / n
        
        for i, val in enumerate(self.state.array):
            # Calculate normalized bar height
            bar_height = int((val / max_val) * radius)
            
            # Calculate angle for current element
            angle = i * angle_step
            
            if i in self.state.sorted_indices:
                color = self.theme.value["secondary"]
            elif i in self.state.highlighted_indices:
                color = self.theme.value["highlight"]
            elif i in self.state.compared_indices:
                color = self.theme.value["highlight"]
            else:
                color = self.theme.value["primary"]
            
            # Calculate start and end points with integer coordinates
            inner_x = int(center_x + ((radius - bar_height) * math.cos(angle)))
            inner_y = int(center_y + ((radius - bar_height) * math.sin(angle)))
            outer_x = int(center_x + (radius * math.cos(angle)))
            outer_y = int(center_y + (radius * math.sin(angle)))
            
            # Draw line
            painter.setPen(QPen(color, max(1, radius//100)))
            painter.drawLine(inner_x, inner_y, outer_x, outer_y)
            
            # Draw dot at end point
            dot_size = max(4, radius//50)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(inner_x - dot_size//2, inner_y - dot_size//2, 
                              dot_size, dot_size)

# Enhanced main window with modern UI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Sorting Algorithm Visualizer")
        self.setMinimumSize(1200, 800)
        
        # Initialize plugin loader
        self.plugin_loader = PluginLoader()
        
        # Load built-in and plugin algorithms
        self.algorithms = self._load_all_algorithms()
        self.current_array = []
        self.worker = None
        self.current_theme = ColorTheme.CLASSIC
        
        # Set application style
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        
        # Create UI
        self.setup_ui()
        self.setup_toolbar()
        self.setup_statusbar()
        
        # Generate initial array
        self.generate_array()
        
        # Connect visualization settings signals
        self.style_selector.currentIndexChanged.connect(self.update_visualization_style)
        self.theme_selector.currentIndexChanged.connect(self.update_visualization_theme)
    def _load_all_algorithms(self) -> List[Type[SortingAlgorithm]]:
            """Load both built-in and plugin algorithms"""
            # First, load built-in algorithms
            builtin_algorithms = [] # i had in previous version, however now they all are in plugins
            
            # Then load plugins
            plugin_algorithms = self.plugin_loader.discover_algorithms()
            
            # Combine and sort all algorithms
            all_algorithms = builtin_algorithms + plugin_algorithms
            return sorted(all_algorithms, key=lambda x: x().name())

    def update_visualization_style(self):
        style_name = self.style_selector.currentText()
        style = VisualizationStyle[style_name]
        self.visualizer.setStyle(style)
        self.statusbar.showMessage(f"Visualization style changed to {style_name}")

    def update_visualization_theme(self):
        theme_name = self.theme_selector.currentText()
        theme = ColorTheme[theme_name]
        self.visualizer.setTheme(theme)
        self.current_theme = theme
        self.statusbar.showMessage(f"Theme changed to {theme_name}")


    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(32, 32))
        
        # Add toolbar actions
        new_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon),
                           "New Array", self)
        new_action.triggered.connect(self.generate_array)
        toolbar.addAction(new_action)
        
        self.addToolBar(toolbar)
    
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create control panel
        control_panel = QVBoxLayout()
        
        # Algorithm selection group
        algo_group = QGroupBox("Algorithm Settings")
        algo_layout = QVBoxLayout()
        
        self.algorithm_selector = QComboBox()
        for algo in self.algorithms:
            self.algorithm_selector.addItem(algo().name())
        algo_layout.addWidget(self.algorithm_selector)
        
        # Algorithm info
        self.algo_info = QLabel()
        self.algo_info.setWordWrap(True)
        algo_layout.addWidget(self.algo_info)
        self.algorithm_selector.currentIndexChanged.connect(self.update_algorithm_info)
        
        algo_group.setLayout(algo_layout)
        control_panel.addWidget(algo_group)
        
        # Array settings group
        array_group = QGroupBox("Array Settings")
        array_layout = QVBoxLayout()
        
        # Array size control
        size_layout = QHBoxLayout()
        self.size_spinner = QSpinBox()
        self.size_spinner.setRange(10, 500)
        self.size_spinner.setValue(50)
        size_layout.addWidget(QLabel("Size:"))
        size_layout.addWidget(self.size_spinner)
        array_layout.addLayout(size_layout)
        
        # Array type selection
        self.random_array = QRadioButton("Random")
        self.nearly_sorted = QRadioButton("Nearly Sorted")
        self.reversed_array = QRadioButton("Reversed")
        self.random_array.setChecked(True)
        array_layout.addWidget(self.random_array)
        array_layout.addWidget(self.nearly_sorted)
        array_layout.addWidget(self.reversed_array)
        
        array_group.setLayout(array_layout)
        control_panel.addWidget(array_group)
        
        # Visualization settings group
        vis_group = QGroupBox("Visualization Settings")
        vis_layout = QVBoxLayout()
        
        # Style selection
        self.style_selector = QComboBox()
        for style in VisualizationStyle:
            self.style_selector.addItem(style.name)
        vis_layout.addWidget(QLabel("Style:"))
        vis_layout.addWidget(self.style_selector)
        
        # Theme selection
        self.theme_selector = QComboBox()
        for theme in ColorTheme:
            self.theme_selector.addItem(theme.name)
        vis_layout.addWidget(QLabel("Theme:"))
        vis_layout.addWidget(self.theme_selector)
        
        # Speed control
        speed_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        speed_layout.addWidget(QLabel("Speed:"))
        speed_layout.addWidget(self.speed_slider)
        vis_layout.addLayout(speed_layout)
        
        vis_group.setLayout(vis_layout)
        control_panel.addWidget(vis_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate New Array")
        self.generate_button.clicked.connect(self.generate_array)
        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.start_sorting)
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.sort_button)
        control_panel.addLayout(button_layout)
        
        # Add stretch to push controls to the top
        control_panel.addStretch()
        
        # Create statistics panel
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        self.stats_label = QLabel()
        stats_layout.addWidget(self.stats_label)
        stats_group.setLayout(stats_layout)
        control_panel.addWidget(stats_group)
        
        # Add control panel to main layout
        panel_widget = QWidget()
        panel_widget.setLayout(control_panel)
        panel_widget.setFixedWidth(300)
        main_layout.addWidget(panel_widget)
        
        # Create visualizer
        visualization_layout = QVBoxLayout()
        self.visualizer = VisualizerWidget()
        visualization_layout.addWidget(self.visualizer)
        
        # Add visualization area to main layout
        vis_widget = QWidget()
        vis_widget.setLayout(visualization_layout)
        main_layout.addWidget(vis_widget)
    
    def update_algorithm_info(self):
        algorithm = self.algorithms[self.algorithm_selector.currentIndex()]()
        info_text = f"""
        <b>Description:</b> {algorithm.description}
        <br><br>
        <b>Time Complexity:</b> {algorithm.time_complexity}
        <br>
        <b>Space Complexity:</b> {algorithm.space_complexity}
        """
        self.algo_info.setText(info_text)
    
    def setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
    
    def generate_array(self):
        size = self.size_spinner.value()
        
        if self.random_array.isChecked():
            self.current_array = random.sample(range(1, size + 1), size)
        elif self.nearly_sorted.isChecked():
            self.current_array = list(range(1, size + 1))
            # Introduce some randomness
            swaps = size // 10
            for _ in range(swaps):
                i, j = random.sample(range(size), 2)
                self.current_array[i], self.current_array[j] = self.current_array[j], self.current_array[i]
        else:  # reversed
            self.current_array = list(range(size, 0, -1))
        
        self.visualizer.setState(SortingState(self.current_array))
        self.sort_button.setEnabled(True)
        self.update_stats(None)
        self.statusbar.showMessage("New array generated")
    
    def update_stats(self, stats: SortingStats):
        if not stats:
            self.stats_label.setText("No sorting in progress")
            return
        
        stats_text = f"""
        <b>Comparisons:</b> {stats.comparisons:,}
        <br>
        <b>Swaps:</b> {stats.swaps:,}
        <br>
        <b>Time:</b> {stats.duration:.2f} seconds
        """
        self.stats_label.setText(stats_text)
    
    def start_sorting(self):
        if self.worker and self.worker.isRunning():
            return
        
        # Disable controls
        self.sort_button.setEnabled(False)
        self.generate_button.setEnabled(False)
        self.algorithm_selector.setEnabled(False)
        self.size_spinner.setEnabled(False)
        
        # Create and start worker
        algorithm = self.algorithms[self.algorithm_selector.currentIndex()]()
        self.worker = SortingWorker(algorithm, self.current_array, self.speed_slider.value())
        self.worker.update_signal.connect(self.update_visualization)
        self.worker.finished_signal.connect(self.sorting_finished)
        self.worker.error_signal.connect(self.sorting_error)
        self.worker.start()
        
        self.statusbar.showMessage(f"Sorting with {algorithm.name()}...")
    
    def update_visualization(self, state: SortingState):
        self.visualizer.setState(state)
        self.update_stats(state.stats)
    
    def sorting_finished(self):
        # Re-enable controls
        self.sort_button.setEnabled(True)
        self.generate_button.setEnabled(True)
        self.algorithm_selector.setEnabled(True)
        self.size_spinner.setEnabled(True)
        
        self.statusbar.showMessage("Sorting completed!")
        
        # Show completion dialog
        QMessageBox.information(self, "Sorting Complete", 
                              "The sorting algorithm has finished executing!")
    
    def sorting_error(self, error_message: str):
        QMessageBox.critical(self, "Sorting Error", 
                           f"An error occurred during sorting:\n{error_message}")
        self.sorting_finished()

# Enhanced sorting worker thread
class SortingWorker(QThread):
    update_signal = pyqtSignal(SortingState)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, algorithm: SortingAlgorithm, array: List[int], speed: int):
        super().__init__()
        self.algorithm = algorithm
        self.array = array.copy()
        self.delay = (101 - speed) / 1000  # Convert speed (1-100) to delay in seconds
    
    def run(self):
        try:
            def update_callback(state: SortingState):
                self.update_signal.emit(state)
                time.sleep(self.delay)
            
            self.algorithm.sort(self.array, update_callback)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

# Main entry point with error handling
def main():
    try:
        app = QApplication(sys.argv)
        # Set application-wide stylesheet
        app.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #5c5c5c;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4c4f51;
            }
            QPushButton:pressed {
                background-color: #5c5f61;
            }
            QComboBox {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #5c5c5c;
                padding: 5px;
                border-radius: 3px;
            }
            QSpinBox {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #5c5c5c;
                padding: 5px;
                border-radius: 3px;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid #5c5c5c;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error",
                           f"An unexpected error occurred:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()