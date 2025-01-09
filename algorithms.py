from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
from typing import Callable, List


@dataclass
class SortingStats:
    """
    Track statistics for sorting algorithm performance.
    
    Attributes:
        comparisons (int): Number of comparisons performed
        swaps (int): Number of element swaps performed
        start_time (float): Timestamp when sorting started
        end_time (float): Timestamp when sorting completed
    """
    comparisons: int = 0
    swaps: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    
    @property
    def duration(self) -> float:
        """
        Calculate the duration of the sorting operation.
        
        Returns:
            float: Time elapsed in seconds. If sorting is still in progress,
                  returns time elapsed since start.
        """
        if self.end_time == 0.0:
            return time.time() - self.start_time
        return self.end_time - self.start_time


@dataclass
class SortingState:
    """
    Represent the current state of the sorting process for visualization.
    
    Attributes:
        array (List[int]): Current state of the array being sorted
        highlighted_indices (List[int]): Indices of elements to highlight
        compared_indices (List[int]): Indices of elements being compared
        sorted_indices (List[int]): Indices of elements in their final sorted position
        pivot_index (int): Index of the current pivot element (for algorithms like QuickSort)
        stats (SortingStats): Current statistics of the sorting process
    """
    array: List[int]
    highlighted_indices: List[int] = None
    compared_indices: List[int] = None
    sorted_indices: List[int] = None
    pivot_index: int = None
    stats: SortingStats = None
    
    def __post_init__(self):
        """Initialize default values for optional attributes."""
        self.highlighted_indices = self.highlighted_indices or []
        self.compared_indices = self.compared_indices or []
        self.sorted_indices = self.sorted_indices or []
        self.stats = self.stats or SortingStats()


class SortingAlgorithm(ABC):
    """
    Abstract base class for sorting algorithms.
    
    This class defines the interface that all sorting algorithms must implement,
    including methods for sorting and properties for algorithm metadata.
    """
    
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the sorting algorithm.
        
        Returns:
            str: Name of the sorting algorithm
        """
        pass
    
    @abstractmethod
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array and provide visualization updates.
        
        Args:
            arr (List[int]): Array to be sorted
            update_callback (Callable[[SortingState], None]): Function to call with
                updated sorting state for visualization
        """
        pass
    
    @property
    def description(self) -> str:
        """
        Get a description of how the algorithm works.
        
        Returns:
            str: Algorithm description
        """
        return "No description available."
    
    @property
    def time_complexity(self) -> str:
        """
        Get the time complexity of the algorithm.
        
        Returns:
            str: Time complexity in Big O notation
        """
        return "Unknown"
    
    @property
    def space_complexity(self) -> str:
        """
        Get the space complexity of the algorithm.
        
        Returns:
            str: Space complexity in Big O notation
        """
        return "Unknown"