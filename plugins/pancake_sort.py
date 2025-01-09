from abc import ABC, abstractmethod
import time
from typing import List, Callable
from dataclasses import dataclass
from algorithms import SortingState, SortingAlgorithm, SortingStats

class PancakeSort(SortingAlgorithm):
    def name(self) -> str:
        return "Pancake Sort"
    
    def description(self) -> str:
        return "A sorting algorithm that only uses flip operations (reversing a prefix of the array)"
    
    @property
    def time_complexity(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    def sort(self, arr: List[int], update_callback: Callable[[SortingState], None]) -> None:
        stats = SortingStats(start_time=time.time())
        n = len(arr)
        
        def flip(size):
            for i in range(size // 2):
                arr[i], arr[size-1-i] = arr[size-1-i], arr[i]
                stats.swaps += 1
                update_callback(SortingState(
                    array=arr.copy(),
                    highlighted_indices=[i, size-1-i],
                    compared_indices=[],
                    sorted_indices=list(range(size, n)),
                    stats=stats
                ))
        
        for size in range(n, 1, -1):
            # Find index of maximum element in arr[0:size]
            max_idx = 0
            for i in range(size):
                stats.comparisons += 1
                if arr[i] > arr[max_idx]:
                    max_idx = i
                update_callback(SortingState(
                    array=arr.copy(),
                    compared_indices=[i, max_idx],
                    highlighted_indices=[max_idx],
                    sorted_indices=list(range(size, n)),
                    stats=stats
                ))
            
            if max_idx != size - 1:
                # Flip from 0 to max_idx
                if max_idx != 0:
                    flip(max_idx + 1)
                # Flip from 0 to size-1
                flip(size)
        
        stats.end_time = time.time()
        update_callback(SortingState(
            array=arr.copy(),
            sorted_indices=list(range(n)),
            stats=stats
        ))