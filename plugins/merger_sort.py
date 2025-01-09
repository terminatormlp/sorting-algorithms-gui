import time
from typing import List, Callable, Tuple
from algorithms import SortingState, SortingAlgorithm, SortingStats


class MergeSort(SortingAlgorithm):
    
    def name(self) -> str:
        return "Merge Sort"
    
    @property
    def description(self) -> str:
        return ("A divide-and-conquer algorithm that recursively divides the array "
                "into two halves, sorts them, and merges them")
    
    @property
    def time_complexity(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(n)"
    
    def _get_subarrays(self, arr: List[int], left: int, mid: int, 
                       right: int) -> Tuple[List[int], List[int]]:
        """
        Extract left and right subarrays for merging.
        
        Args:
            arr: Original array
            left: Start index
            mid: Middle index
            right: End index
        
        Returns:
            Tuple[List[int], List[int]]: Left and right subarrays
        """
        return arr[left:mid + 1], arr[mid + 1:right + 1]
    
    def _merge(self, arr: List[int], left: int, mid: int, right: int,
               stats: SortingStats, update_callback: Callable[[SortingState], None]) -> None:
        """
        Merge two sorted subarrays into a single sorted array.
        
        Args:
            arr: Array containing subarrays to merge
            left: Start index of first subarray
            mid: End index of first subarray
            right: End index of second subarray
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        left_part, right_part = self._get_subarrays(arr, left, mid, right)
        i = j = 0
        k = left
        
        # Merge elements by comparing both parts
        while i < len(left_part) and j < len(right_part):
            stats.comparisons += 1
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            stats.swaps += 1
            
            update_callback(SortingState(
                array=arr.copy(),
                compared_indices=[left + i, mid + 1 + j],
                highlighted_indices=[k],
                sorted_indices=list(range(left, k)),
                stats=stats
            ))
            k += 1
        
        # Copy remaining elements from left part
        while i < len(left_part):
            arr[k] = left_part[i]
            stats.swaps += 1
            update_callback(SortingState(
                array=arr.copy(),
                highlighted_indices=[k],
                sorted_indices=list(range(left, k)),
                stats=stats
            ))
            i += 1
            k += 1
        
        # Copy remaining elements from right part
        while j < len(right_part):
            arr[k] = right_part[j]
            stats.swaps += 1
            update_callback(SortingState(
                array=arr.copy(),
                highlighted_indices=[k],
                sorted_indices=list(range(left, k)),
                stats=stats
            ))
            j += 1
            k += 1
    
    def _mergesort(self, arr: List[int], left: int, right: int,
                   stats: SortingStats, update_callback: Callable[[SortingState], None]) -> None:
        """
        Recursively sort array using merge sort algorithm.
        
        Args:
            arr: Array to sort
            left: Start index
            right: End index
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        if left < right:
            mid = (left + right) // 2
            
            # Recursively sort both halves
            self._mergesort(arr, left, mid, stats, update_callback)
            self._mergesort(arr, mid + 1, right, stats, update_callback)
            
            # Merge the sorted halves
            self._merge(arr, left, mid, right, stats, update_callback)
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array using Merge Sort algorithm.
        
        Args:
            arr: Array to sort
            update_callback: Function to call with updated sorting state for visualization
        """
        stats = SortingStats(start_time=time.time())
        
        # Start the recursive sorting process
        self._mergesort(arr, 0, len(arr) - 1, stats, update_callback)
        
        # Final update with fully sorted array
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(len(arr))),
            stats=stats
        ))