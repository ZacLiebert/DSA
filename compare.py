import sys
import time
import numpy as np

# ==========================================
# 1. SETUP
# ==========================================
N = 1000000  

# Increase recursion depth to prevent crashes in QuickSort/MergeSort
sys.setrecursionlimit(2000000)

# ==========================================
# 2. ALGORITHMS
# ==========================================

def quick_sort(arr):
    # Base case
    if len(arr) <= 1: return arr
    
    # Pivot Selection: Middle element
    # This avoids O(N^2) worst-case performance on sorted arrays
    pivot = arr[len(arr) // 2]
    
    # Partitioning (Pythonic way)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Recursive calls
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) > 1:
        # Divide into two halves
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        
        # Recursive sorting
        merge_sort(L); merge_sort(R)
        
        # Merge sorted halves
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]: arr[k] = L[i]; i += 1
            else: arr[k] = R[j]; j += 1
            k += 1
        
        # Copy remaining elements
        while i < len(L): arr[k] = L[i]; i += 1; k += 1
        while j < len(R): arr[k] = R[j]; j += 1; k += 1
    return arr

def heapify(arr, n, i):
    # Maintain Max-Heap property
    largest = i
    l = 2 * i + 1  # Left child
    r = 2 * i + 2  # Right child
    
    if l < n and arr[i] < arr[l]: largest = l
    if r < n and arr[largest] < arr[r]: largest = r
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i] # Swap
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    # Build Max Heap
    for i in range(n // 2 - 1, -1, -1): heapify(arr, n, i)
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] # Swap root to end
        heapify(arr, i, 0)
    return arr

# ==========================================
# 3. MAIN EXECUTION
# ==========================================

print(f"Generating {N:,} elements (Range: -1B to 1B)...")

# Generate data with large range (-1 Billion to +1 Billion)
data = {
    '1.Float_Asc': np.sort(np.random.uniform(-1e9, 1e9, N)),
    '2.Float_Desc': np.sort(np.random.uniform(-1e9, 1e9, N))[::-1],
    '3.Float_Rnd_1': np.random.uniform(-1e9, 1e9, N),
    '4.Float_Rnd_2': np.random.uniform(-1e9, 1e9, N),
    '5.Float_Rnd_3': np.random.uniform(-1e9, 1e9, N),
    '6.Int_Rnd_1': np.random.randint(-1e9, 1e9, N),
    '7.Int_Rnd_2': np.random.randint(-1e9, 1e9, N),
    '8.Int_Rnd_3': np.random.randint(-1e9, 1e9, N),
    '9.Int_Rnd_4': np.random.randint(-1e9, 1e9, N),
    '10.Int_Rnd_5': np.random.randint(-1e9, 1e9, N)
}

# Prepare CSV output
csv_filename = "Final_Results.csv"
csv_file = open(csv_filename, "w")
csv_file.write("Dataset,QuickSort,HeapSort,MergeSort,Sort_Cpp,Sort_Numpy\n")

print("Running benchmarks (in ms)...")
print("-" * 50)

for name, arr in data.items():
    print(f">> Processing: {name}")
    row = name
    
    # 1. QuickSort
    t0 = time.time()
    quick_sort(arr.tolist())
    row += "," + str(int(round((time.time() - t0) * 1000)))

    # 2. HeapSort
    t0 = time.time()
    heap_sort(arr.tolist())
    row += "," + str(int(round((time.time() - t0) * 1000)))

    # 3. MergeSort
    t0 = time.time()
    merge_sort(arr.tolist())
    row += "," + str(int(round((time.time() - t0) * 1000)))

    # 4. Sort C++ (Timsort)
    lst = arr.tolist()
    t0 = time.time(); lst.sort()
    row += "," + str(int(round((time.time() - t0) * 1000)))

    # 5. Sort Numpy
    t0 = time.time(); np.sort(arr.copy())
    row += "," + str(int(round((time.time() - t0) * 1000)))

    csv_file.write(row + "\n")

csv_file.close()
print("-" * 50)
print(f"Done! Results saved to '{csv_filename}'")