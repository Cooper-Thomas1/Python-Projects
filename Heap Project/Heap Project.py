class Heap:
    """
    A basic heap.
    """

    def __init__(self, items=[], key=None, reverse=False):
        """Constructs a Heap.

        Target Complexity: O(N)

        Args:
            items: Optional. The initial contents of the heap.
            key: Optional. A function to extract a comparison key from an item.
            reverse: Optional. True for a max-heap, False otherwise.
        """
        self.items = heapsort(items)
        self.key = key
        self.reverse = reverse


    def __len__(self):
        """Returns the number of elements in the Heap."""
        return len(self.items)


    def push(self, item):
        """Insert the given item into the Heap.

        Target Complexity: O(lg N).

        Args:
            item: The item to insert.
        """
        self.items.append(item)
        self.upheap(len(self.items) - 1)


    def peek(self):
        """Returns the top element of the Heap.

        Target Complexity: O(1).

        Returns:
            The topmost element in the Heap.

        Raises:
            IndexError: If the Heap is empty.
        """
        if not self.items:
            raise IndexError
        print(self.items)
        return self.items[-1]


    def pop(self):
        """Removes and returns the top element of the Heap.

        Target Complexity: O(lg N).

        Returns:
            The topmost element in the Heap.

        Raises:
            IndexError: If the Heap is empty.
        """
        if not self.items:
            raise IndexError
        
        top_element = self.items[0]
        self.items.pop()
        
        print(self.items)
        self.downheap(0)
        print(self.items)
        return top_element
    

    def swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]


    def upheap(self, j):
        parent = (j - 1) // 2
        while j > 0 and self.items[j] < self.items[parent]:
            self.items[j], self.items[parent] = self.items[parent], self.items[j]
            j = parent
            parent = (j - 1) // 2
    

    def downheap(self, j):
        while 2*j + 1 < len(self.items):
            left = 2*j + 1
            right = 2*j + 2 if (2*j + 2) < len(self.items) else None
            smaller_child = left

            if right is not None and self.items[right] < self.items[left]:
                smaller_child = right

            if self.items[smaller_child] < self.items[j]:
                self.swap(j, smaller_child)
                j = smaller_child
            else:
                break


def heapsort(xs, key=None, reverse=False):
    """Sorts the given list using heapsort.

    Sorts in ascending order by default.

    Args:
        xs: The list to be sorted.
        key: Optional. A function to extract a comparison key from an item.
        reverse: Optional. True for descending order, False for ascending.

    Returns:
        The sorted list.
    """
    length = len(xs)
    for i in range(length // 2, -1, -1):
        heapify(xs, length, i, key=key)

    for i in range(length - 1, 0, -1):
        (xs[i], xs[0]) = (xs[0], xs[i])
        heapify(xs, i, 0, key=key)

    if reverse:
        xs.reverse()
    return xs


def heapify(xs, length, i, key=None):
    largest = i  
    left = 2 * i + 1  
    right = 2 * i + 2  

    if key is not None:
        if left < length and key(xs[i]) < key(xs[left]):
            largest = left

        if right < length and key(xs[largest]) < key(xs[right]):
            largest = right
    else:
        if left < length and xs[i] < xs[left]:
            largest = left

        if right < length and xs[largest] < xs[right]:
            largest = right
    
    if largest != i:
        (xs[i], xs[largest]) = (xs[largest], xs[i])
        heapify(xs, length, largest, key=key)
