import os
import inspect
import importlib.util
from typing import List, Type
from algorithms import SortingAlgorithm


class PluginLoader:
    def __init__(self, plugin_dir: str = "plugins"):
        """
        Initialize the plugin loader with the directory where plugins are stored.
        
        Args:
            plugin_dir (str): Path to the plugins directory (relative to the main script)
        """
        self.plugin_dir = plugin_dir
        self._create_plugin_dir()

    def _create_plugin_dir(self):
        """Create the plugins directory if it doesn't exist."""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            # Create an empty __init__.py to make the directory a Python package
            with open(os.path.join(self.plugin_dir, "__init__.py"), "w") as f:
                pass

    def _load_module(self, filepath: str):
        """
        Load a Python module from a file path.
        
        Args:
            filepath (str): Path to the Python file
            
        Returns:
            module: Loaded Python module or None if loading fails
        """
        module_name = os.path.splitext(os.path.basename(filepath))[0]
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None:
            return None
        
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")
            return None

    def discover_algorithms(self) -> List[Type[SortingAlgorithm]]:
        """
        Discover all sorting algorithms in the plugins directory.
        
        Returns:
            List[Type[SortingAlgorithm]]: List of discovered sorting algorithm classes,
                                         sorted by algorithm name
        """
        algorithms = []
        
        # Scan the plugins directory
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                filepath = os.path.join(self.plugin_dir, filename)
                module = self._load_module(filepath)
                
                if module is None:
                    continue
                
                # Find all classes in the module that inherit from SortingAlgorithm
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and
                        obj != SortingAlgorithm and
                        issubclass(obj, SortingAlgorithm)):
                        algorithms.append(obj)
        
        return sorted(algorithms, key=lambda x: x().name())