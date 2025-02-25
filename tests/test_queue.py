"""
test_queue.py

Unit tests for the custom FIFO Queue implementation in queue.py.
We no longer reference single-lift PriorityQueue logic (if removed).

If you're no longer using queue.py, you can remove this test file entirely.
Otherwise, here's a minimal test that confirms enqueue/dequeue behavior.
"""

import unittest
from queue import Queue  # the minimal queue you may have

class TestQueue(unittest.TestCase):

    def test_fifo_behavior(self):
        q = Queue()
        self.assertTrue(q.is_empty(), "Queue should be empty initially.")

        q.enqueue("first")
        q.enqueue("second")
        q.enqueue("third")

        self.assertEqual(q.size(), 3, "Queue should have size 3 after enqueues.")
        self.assertFalse(q.is_empty(), "Queue should not be empty.")

        # Dequeue and verify FIFO order
        item1 = q.dequeue()
        self.assertEqual(item1, "first", "First dequeued item should be 'first'.")
        item2 = q.dequeue()
        self.assertEqual(item2, "second", "Second dequeued item should be 'second'.")
        item3 = q.dequeue()
        self.assertEqual(item3, "third", "Third dequeued item should be 'third'.")

        self.assertTrue(q.is_empty(), "Queue should be empty after dequeuing all items.")

        # Dequeue from empty -> should raise IndexError
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.peek()  # empty -> error

        q.enqueue("alpha")
        q.enqueue("beta")
        front = q.peek()
        self.assertEqual(front, "alpha", "Peek should return 'alpha' without removing it.")
        self.assertEqual(q.size(), 2, "Queue size should remain 2 after peek.")

if __name__ == '__main__':
    unittest.main()