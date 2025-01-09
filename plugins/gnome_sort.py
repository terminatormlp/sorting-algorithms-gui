import time
from typing import List, Callable
from algorithms import SortingState, SortingAlgorithm, SortingStats


class GnomeSort(SortingAlgorithm):
    def name(self) -> str:
        return "Gnome Sort"
    
    @property
    def description(self) -> str:
        return ("A simple sorting algorithm that works by repeatedly swapping "
                "adjacent elements that are in the wrong order")
    
    @property
    def time_complexity(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def _should_swap(self, arr: List[int], index: int, stats: SortingStats) -> bool:
        """
        Check if elements at current and previous position should be swapped.
        
        Args:
            arr: Array being sorted
            index: Current position
            stats: Statistics tracking object
            
        Returns:
            bool: True if elements should be swapped, False otherwise
        """
        stats.comparisons += 1
        return index > 0 and arr[index] < arr[index - 1]
    
    def _get_sorted_indices(self, arr: List[int], current_index: int) -> List[int]:
        """
        Get indices of elements that are in their final sorted positions.
        
        Args:
            arr: Current array state
            current_index: Current position in array
            
        Returns:
            List[int]: Indices of sorted elements
        """
        return [i for i in range(current_index) 
                if all(arr[j] <= arr[j+1] for j in range(i, current_index-1))]
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array using Gnome Sort algorithm.
        
        Args:
            arr: Array to sort
            update_callback: Function to call with updated sorting state for visualization
        """
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        index = 0
        
        while index < n:
            # If at start or elements are in order, move forward
            if index == 0 or arr[index] >= arr[index - 1]:
                index += 1
            else:
                # Swap elements and move backward
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                stats.swaps += 1
                
                # Update visualization
                update_callback(SortingState(
                    array=arr.copy(),
                    compared_indices=[index, index - 1],
                    highlighted_indices=[index - 1],
                    sorted_indices=self._get_sorted_indices(arr, index),
                    stats=stats
                ))
                
                index -= 1
        
        # Final update with fully sorted array
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(n)),
            stats=stats
        ))