class custom_sort:
    original_list = None
    sorted_list = None
    def __init__(self, arr):
        if not isinstance(arr, list):
            raise Exception("Array argument in constructor must be of type list")
        self.original_list = arr
    def substr_get_number(self, a_substr) -> int:
        #print("Before getting iter of substr, it looks like {}".format(a_substr))
        a_substr_iter = iter(a_substr)
        #print("Successfully created iter")
        how_many_digits = 0
        while True:
            try:
                a_char = next(a_substr_iter)
                #print("a_char {}".format(a_char))
                a_int = int(a_char)
                #print("Converted a char to int {}".format(a_int))
                how_many_digits += 1
            except(ValueError):
                break
            except(StopIteration):
                #print("Iter exhausted.")
                break
            #except:
            #    print("Unknown exception encountered")
            #    break
        #print("Substring that is a number {}".format(a_substr[0:how_many_digits]))
        return int(a_substr[:how_many_digits])
    def substr_get_digits(self, a_substr):
        a_substr_iter = iter(a_substr)
        how_many_digits = 0
        while True:
            try:
                a_char = next(a_substr_iter)
                a_int = int(a_char)
                how_many_digits += 1
            except:
                break
        return how_many_digits
    def swap(self, arr, index_a, index_b):
        temp = arr[index_a]
        arr[index_a] = arr[index_b]
        arr[index_b] = temp
    # Returns 1 if entry_a is higher than entry_b, -1 if the converse, 0 if they are equal
    def compare(self, entry_a, entry_b) -> int:
        entry_char_index = 0
        offset = 0
        while entry_char_index < len(entry_a):
            should_continue = False
            while offset != 0:
                entry_char_index += 1
                offset -= 1
                should_continue = True
            if should_continue:
                continue
            try:
                entry_a_char = entry_a[entry_char_index]
                entry_b_char = entry_b[entry_char_index]
                try:
                    entry_a_char_as_int = int(entry_a_char)
                    entry_b_char_as_int = int(entry_b_char)
                    #print("Found similar numerics. Sorting smartly...")
                    substr_a = entry_a[entry_char_index:]
                    substr_b = entry_b[entry_char_index:]
                    #print("Getting int from substrings: <{}, {}>".format(substr_a, substr_b))
                    val_a = self.substr_get_number(substr_a)
                    val_b = self.substr_get_number(substr_b)
                    #print("val_a and val_b is <{},{}>".format(val_a, val_b))
                    if val_a > val_b:
                        return 1
                    elif val_a == val_b:
                        #print("val_a = val_b!")
                        digits_count = self.substr_get_digits(substr_a)
                        offset += digits_count-1
                        entry_char_index += 1
                        #print("Continuing")
                        continue
                    else:
                        return -1
                except(ValueError):
                    #print("Value Error Exception caught")
                    if entry_a_char != entry_b_char:
                        print("Breaking from entry_a_char and entry_b_char comparison at <{},{}> respectively.  Resorting to string comparison".format(entry_a_char, entry_b_char))
                        break
                except(IndexError):
                    print("Index error caught")
            except(IndexError):
                print("An index was out of bounds")
            entry_char_index += 1
        # if it gets to this point, then do a typical string comparison
        if entry_a > entry_b:
            return 1
        elif entry_a == entry_b:
            return 0
        else:
            return -1
    def sort_prioritizing_proper_number_order(self, is_ascending = True):
        final_arr = self.original_list[:]
        # marker is either a min or max placeholder depending on whether it is ascending or descending
        # If it is ascending then it is a placeholder for min, and max if in reverse.
        if len(final_arr) > 0:
            marker = None
            marker_index = -1
            for i in range(0, len(final_arr)):
                iterable_number_list = range(i+1,len(final_arr)) if is_ascending else range(len(final_arr) - 1, i)
                if marker is None:
                    marker = final_arr[i]
                    marker_index = i
                for index_a in iterable_number_list:
                    entry = final_arr[index_a]
                    #print("Index is {}".format(index_a))
                    if is_ascending and self.compare(entry, marker) == -1: # if this is true then entry is in the incorrect spot
                        #print("Found a new minimum: {}, old: {}".format(entry, marker))
                        marker = entry
                        marker_index=index_a
                    elif not is_ascending and self.compare(entry, marker) == 1:
                        #print("Found a new max: {}, old: {}".format(entry, marker))
                        marker = entry
                        marker_index = index_a
                if i != marker_index:
                    #print("Indices <{},{}> will switch: {} with {}".format(i, marker_index, entry, marker))
                    self.swap(final_arr, i, marker_index)
                marker = None
                marker_index = -1
        self.sorted_list = final_arr
        print("Original list: {}\nSorted list:{}".format(self.original_list, self.sorted_list))
        return self.sorted_list