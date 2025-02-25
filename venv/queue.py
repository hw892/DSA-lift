"""
queue.py

A minimal FIFO Queue implementation. Use only if you still need a 
custom queue for your multi-lift logic. Otherwise, you can remove 
this file entirely if you're storing requests in a list in each Lift.
"""

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """
        Add an item to the end of the queue.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Remove and return the item at the front of the queue.
        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.items.pop(0)

    def peek(self):
        """
        Return the front item without removing it.
        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)