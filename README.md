# Sorting Algorithm Visualizer

A feature-rich, interactive visualization tool for various sorting algorithms built with PyQt6. This application helps users understand how different sorting algorithms work through real-time visualization and performance metrics.



## Features

- **Multiple Visualization Styles**
  - Bars: Traditional bar graph representation
  - Dots: Connected dot visualization
  - Scatter: Scatter plot with guide lines
  - Circular: Circular visualization pattern

- **Real-time Statistics**
  - Number of comparisons
  - Number of swaps
  - Execution time
  - Current sorting progress

- **Customization Options**
  - Adjustable array size (10-500 elements)
  - Variable sorting speed
  - Multiple color themes (Classic, Sunset, Forest)
  - Different initial array arrangements (Random, Nearly Sorted, Reversed)

- **Plugin System**
  - Extensible architecture supporting custom sorting algorithm implementations
  - Hot-loading of new algorithms from the plugins directory

## Supported Algorithms

1. **Block Sort**
   
3. **Comb Sort**

4. **Gnome Sort**
   
5. **Heap Sort**

6. **Insertion Sort**

7. **Merge Sort**

8. **Pancake Sort**

9. **Quick Sort**

10. **Selection Sort**
11. **Shell Sort**
## Installation

1. Clone the repository:
```bash
git clone https://github.com/terminatormlp/sorting-algorithms-gui.git
cd sorting-algorithms-gui
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Using the interface:
   - Select a sorting algorithm from the dropdown menu
   - Adjust the array size
   - Choose the initial array arrangement (Random, Nearly Sorted, Reversed)
   - Select visualization style and theme
   - Adjust sorting speed using the slider
   - Click "Generate New Array" to create a new dataset
   - Click "Sort" to begin visualization

## Creating Custom Algorithms

You can add your own sorting algorithms by creating a new file in the `plugins` directory:

1. Create a new Python file in the `plugins` directory
2. Implement your algorithm by extending the `SortingAlgorithm` base class:

```python
import time
from typing import List, Callable
from algorithms import SortingAlgorithm, SortingState, SortingStats

class MySort(SortingAlgorithm):
    def name(self) -> str:
        return "My Sort Algorithm"
    
    @property
    def description(self) -> str:
        return "Description of how my algorithm works"
    
    @property
    def time_complexity(self) -> str:
        return "O(?)"
    
    @property
    def space_complexity(self) -> str:
        return "O(?)"
    
    def sort(self, arr, update_callback):
        # Implement your sorting logic here
        pass
```
