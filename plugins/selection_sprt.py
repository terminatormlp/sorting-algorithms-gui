import time
from typing import List, Callable
from algorithms import SortingState, SortingAlgorithm, SortingStats

class SelectionSort(SortingAlgorithm):
    def name(self) -> str:
        return "Selection Sort"
    
    def description(self) -> str:
        return "Divides the array into sorted and unsorted regions, repeatedly selecting the minimum element from the unsorted region"
    
    @property
    def time_complexity(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                stats.comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
                update_callback(SortingState(
                    array=arr.copy(),
                    compared_indices=[min_idx, j],
                    highlighted_indices=[min_idx],
                    sorted_indices=list(range(i)),
                    stats=stats
                ))
            
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                stats.swaps += 1
                update_callback(SortingState(
                    array=arr.copy(),
                    highlighted_indices=[i, min_idx],
                    sorted_indices=list(range(i + 1)),
                    stats=stats
                ))
        
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(len(arr))),
            stats=stats
        ))