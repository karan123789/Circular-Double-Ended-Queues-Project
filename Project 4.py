from typing import TypeVar, List, Optional


T = TypeVar('T')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: Optional[List[T]] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # ============ Modify Functions Below ============#

    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque - this is the number
        of items currently in the circular deque, and will not necessarily
        be equal to the capacity

        :return:  int representing length of the circular deque
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty

        :return: True if empty, False otherwise
        """
        if self.size == 0:
            return True
        else:
            return False

    def front_element(self) -> Optional[T]:
        """
        Returns the first element in the circular deque

        :return: the first element if it exists, otherwise None
        """
        if self.is_empty():
            return None
        else:
            return self.queue[self.front]

    def back_element(self) -> Optional[T]:
        """
        Returns the last element in the circular deque

        :return: the last element if it exists, otherwise None
        """
        if self.is_empty():
            return None
        else:
            return self.queue[self.back]

    def grow(self) -> None:
        """
        Doubles the capacity of the deque by creating a new underlying Python
        list with double the capacity of the old one and copies the values
        over from the current list.

        :return: None
        """
        doubled_capacity = self.capacity * 2  # Calculate the new capacity by doubling the current capacity.
        expanded_queue = [None] * doubled_capacity  # Create a new list with the new capacity to hold the expanded deque.

        # Copy elements from the current deque to the new deque.
        for i in range(self.size):
            expanded_queue[i] = self.queue[(self.front + i) % self.capacity]

        # Update deque attributes with the new deque.
        self.queue = expanded_queue  # Replace the old deque with the new expanded deque.
        self.capacity = doubled_capacity  # Update the capacity attribute to reflect the new capacity.
        self.front = 0  # Reset the front index to the start of the deque.
        self.back = self.size - 1  # Update the back index accordingly.




    def shrink(self) -> None:
        """
        Halves the capacity of the deque (the reverse of grow). Copies over the contents
        of the old list to a new one with half the original capacity.

        :return: None
        """
        if self.capacity // 2 < 4:  # If halving the capacity would make it less than 4, return early.
            return

        halved_capacity = self.capacity // 2  # Calculate the new capacity by halving the current capacity.
        reduced_queue = [None] * halved_capacity  # Create a new list with the halved capacity to hold the reduced deque.

        # Copy elements from the current deque to the new deque.
        for i in range(self.size):
            reduced_queue[i] = self.queue[(self.front + i) % self.capacity]

        # Update deque attributes with the new deque.
        self.queue = reduced_queue  # Replace the old deque with the new reduced deque.
        self.front = 0  # Reset the front index to the start of the deque.
        self.back = self.size - 1  # Update the back index accordingly.
        self.capacity = halved_capacity  # Update the capacity attribute to reflect the new capacity.



    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Add a value to either the front or back of the circular deque
        based off the parameter front

        :param value: value to add into the circular deque
        :param front: which end of the deque to add the value
        :return: None
        """
        if self.size == 0:  # Check if the deque is empty.
            self.front = 0  # If empty, set both front and back to the same index.
            self.back = 0
        else:
            if front:  # If the value is to be added to the front of the deque.
                self.front = (self.front - 1) % self.capacity  # Calculate the new front index.
            else:
                self.back = (self.back + 1) % self.capacity  # Calculate the new back index.

        self.queue[self.front if front else self.back] = value
          # Assign the value to the appropriate index.

        self.size += 1  # Increment the size of the deque.

        if self.size == self.capacity:  # Check if the deque is full after adding the value.
            self.grow()  # Call the grow method to expand the deque if needed.




    def dequeue(self, front: bool = True) -> Optional[T]:
        """
        Remove an item from the queue

        :param front: Whether to remove the front or back item from the dequeue
        :return: removed item, None if empty
        """
        if self.is_empty():  # Check if the deque is empty.
            return None

        if front:  # If removing from the front.
            removed_element = self.queue[self.front]  # Get the item to be removed from the front.
            self.front = (self.front + 1) % self.capacity  # Adjust the front index accordingly.
        else:  # If removing from the back.
            removed_element = self.queue[self.back]  # Get the item to be removed from the back.
            self.back = (self.back - 1 + self.capacity) % self.capacity  # Adjust the back index accordingly.

        self.size -= 1  # Decrement the size of the deque.

        if self.is_empty():  # If the deque is now empty after removing the item.
            self.front = None  # Reset front and back indices.
            self.back = None

        if self.size <= self.capacity // 4 and self.capacity // 2 >= 4:  # Check if the deque is less than or equal to one-fourth full.
            self.shrink()  # Call the shrink method to reduce the deque's capacity.

        return removed_element  # Return the removed item.




def maximize_profits(profits: List[int], k: int) -> int:
    """
    Takes in a pay period (as a list of profits), a work interval k,
    and returns the maximum profit that can be made within the pay period

    :param profits: A list of profits representing the amount of money made (or lost) for a given day
    :param k: A work interval. You must work at least once every k days.
    :return: The maximum possible profit obtainable within the pay period
    """
    num_days = len(profits)  # Number of days in the pay period
    max_profit = [0] * (num_days + 1)  # Initialize the max_profit list with zeros
    deque = []  # Initialize an empty deque
    deque_front = 0  # Initialize the front of the deque
    deque_rear = -1  # Initialize the rear of the deque
    
    day = 1  # Initialize the current day

    while day <= num_days:  # Iterate over each day in the pay period
        # Remove elements of deque which are out of this window
        while deque_front <= deque_rear and deque[deque_front] < day - k:
            deque_front += 1

        # Update the max_profit for the current day
        if deque_front <= deque_rear:
            max_profit[day] = profits[day - 1] + max_profit[deque[deque_front]]
        else:
            max_profit[day] = profits[day - 1]

        # Remove all elements smaller than the current from deque
        for idx in range(deque_rear, deque_front - 1, -1):
            if max_profit[day] >= max_profit[deque[idx]]:
                deque_rear -= 1
            else:
                break

        deque.append(None)  # Add a new element to the deque
        deque_rear += 1  # Increment the rear of the deque
        deque[deque_rear] = day  # Update the rear of the deque to the current day
        
        day += 1  # Move to the next day

    return max_profit[-1]  # Return the maximum profit






