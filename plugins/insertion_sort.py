
import time
from typing import List, Callable
from algorithms import SortingState, SortingAlgorithm, SortingStats


class InsertionSort(SortingAlgorithm):
    def name(self) -> str:
        return "Insertion Sort"
    
    @property
    def description(self) -> str:
        return ("Builds the final sorted array one item at a time by repeatedly "
                "inserting elements into their correct position")
    
    @property
    def time_complexity(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def _find_insertion_position(self, arr: List[int], start: int, key: int, 
                               stats: SortingStats) -> int:
        """
        Find the correct position for inserting the key element.
        
        Args:
            arr: Array being sorted
            start: Starting position for backward search
            key: Element to insert
            stats: Statistics tracking object
        
        Returns:
            int: Position where key should be inserted
        """
        j = start
        while j >= 0:
            stats.comparisons += 1
            if arr[j] > key:
                j -= 1
            else:
                break
        return j + 1
    
    def _shift_elements(self, arr: List[int], start: int, end: int, 
                       stats: SortingStats, update_callback: Callable[[SortingState], None]) -> None:
        """
        Shift elements right to make space for insertion.
        
        Args:
            arr: Array being sorted
            start: Starting position for shift
            end: Ending position for shift
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        for j in range(end - 1, start - 1, -1):
            arr[j + 1] = arr[j]
            stats.swaps += 1
            update_callback(SortingState(
                array=arr.copy(),
                compared_indices=[j, j + 1],
                highlighted_indices=[j + 1],
                sorted_indices=list(range(0, end)),
                stats=stats
            ))
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array using Insertion Sort algorithm.
        
        Args:
            arr: Array to sort
            update_callback: Function to call with updated sorting state for visualization
        """
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        
        for i in range(1, n):
            key = arr[i]
            # Find where to insert the current element
            insert_pos = self._find_insertion_position(arr, i - 1, key, stats)
            
            # Shift elements to make space
            if insert_pos < i:
                self._shift_elements(arr, insert_pos, i, stats, update_callback)
                
                # Insert the element
                arr[insert_pos] = key
                stats.swaps += 1
                update_callback(SortingState(
                    array=arr.copy(),
                    highlighted_indices=[insert_pos],
                    sorted_indices=list(range(0, i + 1)),
                    stats=stats
                ))
        
        # Final update with fully sorted array
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(n)),
            stats=stats
        ))