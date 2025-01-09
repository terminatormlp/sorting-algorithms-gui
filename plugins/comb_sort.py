import time
from typing import List, Callable
from algorithms import SortingState, SortingAlgorithm, SortingStats


class CombSort(SortingAlgorithm):
    def __init__(self, shrink_factor: float = 1.3):
        """
        Initialize CombSort with a custom shrink factor.
        
        Args:
            shrink_factor (float): Factor by which the gap is reduced in each iteration.
                                  Default is 1.3, which has been found to be optimal.
        """
        self.shrink_factor = shrink_factor
    
    def name(self) -> str:
        return "Comb Sort"
    
    @property
    def description(self) -> str:
        return ("An improvement over Bubble Sort that eliminates turtles "
                "(small values near the end) by using a gap larger than 1")
    
    @property
    def time_complexity(self) -> str:
        return "O(n²/2^p) where p is the number of increments"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def _is_sorted(self, arr: List[int]) -> bool:
        """
        Check if the array is sorted.
        
        Args:
            arr: Array to check
            
        Returns:
            bool: True if array is sorted, False otherwise
        """
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    
    def _get_sorted_indices(self, arr: List[int], n: int) -> List[int]:
        """
        Get indices of elements that are in their final sorted positions.
        
        Args:
            arr: Current array state
            n: Length of array
            
        Returns:
            List[int]: Indices of sorted elements
        """
        return [j for j in range(n) if all(arr[k] <= arr[k+1] 
                for k in range(j, n-1))]
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array using Comb Sort algorithm.
        
        Args:
            arr: Array to sort
            update_callback: Function to call with updated sorting state for visualization
        """
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        gap = n
        is_sorted = False
        
        while not is_sorted:
            # Update gap
            gap = max(1, int(gap / self.shrink_factor))
            is_sorted = (gap == 1)  # Will be set to False if any swaps occur
            
            # Perform comparisons with current gap
            for i in range(n - gap):
                stats.comparisons += 1
                if arr[i] > arr[i + gap]:
                    # Swap elements
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    stats.swaps += 1
                    is_sorted = False
                    
                    # Update visualization
                    update_callback(SortingState(
                        array=arr.copy(),
                        compared_indices=[i, i + gap],
                        highlighted_indices=[i, i + gap],
                        sorted_indices=self._get_sorted_indices(arr, n),
                        stats=stats
                    ))
        
        # Final update with fully sorted array
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(n)),
            stats=stats
        ))