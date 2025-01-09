
import time
from typing import List, Callable
from algorithms import SortingState, SortingAlgorithm, SortingStats


class BlockSort(SortingAlgorithm):
    def name(self) -> str:
        return "Block Sort"
    
    @property
    def description(self) -> str:
        return "A hybrid sorting algorithm that combines merge sort's efficiency with insertion sort's performance on small blocks"
    
    @property
    def time_complexity(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def _insertion_sort_range(self, arr: List[int], start: int, end: int, 
                            stats: SortingStats, update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort a range within the array using insertion sort.
        
        Args:
            arr: Array to sort
            start: Starting index of the range
            end: Ending index of the range (exclusive)
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        for i in range(start + 1, end):
            key = arr[i]
            j = i - 1
            while j >= start:
                stats.comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    stats.swaps += 1
                    update_callback(SortingState(
                        array=arr.copy(),
                        compared_indices=[j, j + 1],
                        highlighted_indices=[i],
                        sorted_indices=list(range(start, j + 1)),
                        stats=stats
                    ))
                    j -= 1
                else:
                    break
            arr[j + 1] = key
    
    def _merge_blocks(self, arr: List[int], start1: int, end1: int, start2: int, end2: int,
                     stats: SortingStats, update_callback: Callable[[SortingState], None]) -> None:
        """
        Merge two sorted blocks within the array.
        
        Args:
            arr: Array containing the blocks to merge
            start1: Start index of first block
            end1: End index of first block (exclusive)
            start2: Start index of second block
            end2: End index of second block (exclusive)
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        merged = []
        i, j = start1, start2
        
        while i < end1 and j < end2:
            stats.comparisons += 1
            if arr[i] <= arr[j]:
                merged.append(arr[i])
                i += 1
            else:
                merged.append(arr[j])
                j += 1
            stats.swaps += 1
        
        while i < end1:
            merged.append(arr[i])
            stats.swaps += 1
            i += 1
        
        while j < end2:
            merged.append(arr[j])
            stats.swaps += 1
            j += 1
        
        for i, val in enumerate(merged):
            arr[start1 + i] = val
            update_callback(SortingState(
                array=arr.copy(),
                highlighted_indices=[start1 + i],
                compared_indices=[],
                sorted_indices=list(range(start1, start1 + i)),
                stats=stats
            ))
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array using Block Sort algorithm.
        
        Args:
            arr: Array to sort
            update_callback: Function to call with updated sorting state for visualization
        """
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        
        # Block size - using sqrt(n) as a reasonable block size
        block_size = max(1, int(n ** 0.5))
        
        # Sort individual blocks using insertion sort
        for i in range(0, n, block_size):
            end = min(i + block_size, n)
            self._insertion_sort_range(arr, i, end, stats, update_callback)
            update_callback(SortingState(
                array=arr.copy(),
                highlighted_indices=list(range(i, end)),
                sorted_indices=list(range(i)),
                stats=stats
            ))
        
        # Merge sorted blocks
        curr_size = block_size
        while curr_size < n:
            for start in range(0, n, curr_size * 2):
                mid = min(start + curr_size, n)
                end = min(start + curr_size * 2, n)
                if mid < end:
                    self._merge_blocks(arr, start, mid, mid, end, stats, update_callback)
            
            curr_size *= 2
            update_callback(SortingState(
                array=arr.copy(),
                sorted_indices=[i for i in range(n) if i < curr_size or 
                              (i % (curr_size * 2) < curr_size and 
                               i + curr_size >= n)],
                stats=stats
            ))
        
        # Final state
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(n)),
            stats=stats
        ))