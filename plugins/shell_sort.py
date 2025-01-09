from abc import ABC, abstractmethod
import time
from typing import List, Callable
from dataclasses import dataclass
from algorithms import SortingState, SortingAlgorithm, SortingStats

class ShellSort(SortingAlgorithm):
    def name(self) -> str:
        return "Shell Sort"
    
    def description(self) -> str:
        return "An optimization of insertion sort that allows the exchange of items that are far apart, gradually reducing the gap between elements to be compared"
    
    @property
    def time_complexity(self) -> str:
        return "O(n log n) to O(n²) depending on gap sequence"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        
        # Start with a big gap, then reduce the gap
        # Using the gap sequence: n/2, n/4, n/8, ..., 1
        gap = n // 2
        
        # Keep track of sorted elements for visualization
        sorted_elements = set()
        
        while gap > 0:
            # Do a gapped insertion sort for this gap size
            for i in range(gap, n):
                # Store current element to be inserted
                temp = arr[i]
                j = i
                
                # Shift elements that are gap positions ahead 
                # until we find the right position for temp
                while j >= gap:
                    stats.comparisons += 1
                    if arr[j - gap] > temp:
                        arr[j] = arr[j - gap]
                        stats.swaps += 1
                        
                        # Update visualization showing the gap comparison
                        update_callback(SortingState(
                            array=arr.copy(),
                            compared_indices=[j, j - gap],
                            highlighted_indices=[i],  # Current element being inserted
                            sorted_indices=list(sorted_elements),
                            stats=stats
                        ))
                        
                        j -= gap
                    else:
                        break
                
                # Put temp in its correct location
                if arr[j] != temp:
                    arr[j] = temp
                    stats.swaps += 1
                    
                    # Update visualization for the insertion
                    update_callback(SortingState(
                        array=arr.copy(),
                        highlighted_indices=[j],
                        compared_indices=[],
                        sorted_indices=list(sorted_elements),
                        stats=stats
                    ))
            
            # After each gap iteration, mark elements as partially sorted
            for i in range(gap):
                is_section_sorted = True
                for j in range(i, n, gap):
                    if j + gap < n:
                        stats.comparisons += 1
                        if arr[j] > arr[j + gap]:
                            is_section_sorted = False
                            break
                
                if is_section_sorted:
                    for j in range(i, n, gap):
                        sorted_elements.add(j)
            
            # Show the state after processing current gap
            update_callback(SortingState(
                array=arr.copy(),
                highlighted_indices=[],
                compared_indices=[],
                sorted_indices=list(sorted_elements),
                stats=stats
            ))
            
            # Calculate next gap
            gap //= 2
        
        # Final state with all elements sorted
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            highlighted_indices=[],
            compared_indices=[],
            sorted_indices=list(range(n)),
            stats=stats
        ))