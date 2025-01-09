import time
from typing import List, Callable
from algorithms import SortingState, SortingAlgorithm, SortingStats


class HeapSort(SortingAlgorithm):
    def name(self) -> str:
        return "Heap Sort"
    
    @property
    def description(self) -> str:
        return ("A comparison-based sorting algorithm that builds a heap "
                "and repeatedly extracts the maximum element")
    
    @property
    def time_complexity(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def _get_children(self, i: int) -> tuple[int, int]:
        """
        Get indices of left and right children in the heap.
        
        Args:
            i: Parent node index
            
        Returns:
            tuple[int, int]: Indices of left and right children
        """
        return 2 * i + 1, 2 * i + 2
    
    def _heapify(self, arr: List[int], n: int, i: int, stats: SortingStats, 
                 update_callback: Callable[[SortingState], None]) -> None:
        """
        Maintain max heap property at given node.
        
        Args:
            arr: Array being heapified
            n: Size of heap
            i: Index of root node to heapify
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        largest = i
        left, right = self._get_children(i)
        
        # Check if left child is larger than root
        if left < n:
            stats.comparisons += 1
            if arr[left] > arr[largest]:
                largest = left
        
        # Check if right child is larger than current largest
        if right < n:
            stats.comparisons += 1
            if arr[right] > arr[largest]:
                largest = right
        
        # If largest is not root
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            stats.swaps += 1
            
            update_callback(SortingState(
                array=arr.copy(),
                compared_indices=[i, largest],
                highlighted_indices=[i, largest],
                sorted_indices=list(range(n, len(arr))),
                stats=stats
            ))
            
            # Recursively heapify the affected sub-tree
            self._heapify(arr, n, largest, stats, update_callback)
    
    def _build_max_heap(self, arr: List[int], stats: SortingStats,
                       update_callback: Callable[[SortingState], None]) -> None:
        """
        Convert input array into a max heap.
        
        Args:
            arr: Array to convert to heap
            stats: Statistics tracking object
            update_callback: Function to call for visualization updates
        """
        n = len(arr)
        # Build heap (rearrange array)
        # Start from last non-leaf node and move up
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, stats, update_callback)
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        """
        Sort the input array using Heap Sort algorithm.
        
        Args:
            arr: Array to sort
            update_callback: Function to call with updated sorting state for visualization
        """
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        
        # Phase 1: Build max heap
        self._build_max_heap(arr, stats, update_callback)
        
        # Phase 2: Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            # Move current root (maximum element) to end
            arr[0], arr[i] = arr[i], arr[0]
            stats.swaps += 1
            
            update_callback(SortingState(
                array=arr.copy(),
                highlighted_indices=[0, i],
                sorted_indices=list(range(i, n)),
                stats=stats
            ))
            
            # Heapify root element to maintain max heap property
            self._heapify(arr, i, 0, stats, update_callback)
        
        # Final update with fully sorted array
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(len(arr))),
            stats=stats
        ))