from abc import ABC, abstractmethod
import time
from typing import List, Callable
from dataclasses import dataclass
from algorithms import SortingState, SortingAlgorithm, SortingStats

class QuickSort(SortingAlgorithm):
    def name(self) -> str:
        return "Quick Sort"
    
    def description(self) -> str:
        return "A divide-and-conquer sorting algorithm that picks a 'pivot' element and partitions the array around it"
    
    @property
    def time_complexity(self) -> str:
        return "O(n log n) average, O(n²) worst"
    
    @property
    def space_complexity(self) -> str:
        return "O(log n)"
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        # Initialize statistics with start time
        stats = SortingStats(start_time=time.time())
        
        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                stats.comparisons += 1  # Count comparison with pivot
                if arr[j] <= pivot:
                    i += 1
                    # Count swap
                    stats.swaps += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    # Update visualization with current state and stats
                    update_callback(SortingState(
                        array=arr.copy(),
                        compared_indices=[j, high],  # Compare with pivot
                        highlighted_indices=[i],  # Highlight swap position
                        sorted_indices=[],  # Will be set after partition is complete
                        pivot_index=high,
                        stats=stats
                    ))
            
            # Final swap with pivot
            stats.swaps += 1
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            
            # Update visualization
            update_callback(SortingState(
                array=arr.copy(),
                compared_indices=[],
                highlighted_indices=[i + 1, high],
                sorted_indices=[i + 1],  # Pivot is now in its final position
                pivot_index=i + 1,
                stats=stats
            ))
            
            return i + 1
        
        def quicksort(low: int, high: int, sorted_indices: List[int]):
            if low < high:
                # Find pivot position
                pi = partition(low, high)
                # Add pivot to sorted indices as it's now in final position
                sorted_indices.append(pi)
                
                # Recursively sort left and right partitions
                quicksort(low, pi - 1, sorted_indices)
                quicksort(pi + 1, high, sorted_indices)
        
        # Start the sorting process
        sorted_indices = []
        quicksort(0, len(arr) - 1, sorted_indices)
        
        # Set end time and show final state
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            compared_indices=[],
            highlighted_indices=[],
            sorted_indices=list(range(len(arr))),  # All indices are sorted
            stats=stats
        ))
