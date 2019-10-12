# Implementation of the Huffman Coding algorithm to create an encoding table to efficiently encode a text file

from queue import PriorityQueue
from collections import Counter

class Node:
    """Node class used to form the tree used in Huffman_Coding"""

    def __init__(self, data, priority):
        self.data = data
        self.priority = priority
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.priority < other.priority

def Huffman_Coding(freq):
    """Takes a Counter object of frequencies of each character as 'freq'
    Outputs an encoding table (dictionary of characters and their encoded representation as a string of 0's and 1's)
    """

    def get_codings(coding, path, parent):
        left = parent.left
        right = parent.right
        if left.data:
            coding[left.data] = path + '0'
        else:
            get_codings(coding, path + '0', left)
        if right.data:
            coding[right.data] = path + '1'
        else:
            get_codings(coding, path + '1', right)

    heap = PriorityQueue()
    for c in freq:
        heap.put(Node(c, freq[c]))
    root = None
    while True:
        left = heap.get()
        if heap.empty():
            root = left
            break
        right = heap.get()
        new_node = Node(0, left.priority+right.priority)
        new_node.left = left
        new_node.right = right
        heap.put(new_node)
    coding = dict()
    get_codings(coding, '', root)
    return coding

def sorted_table(coding):
    """Return a copy of the coding table (Dictionary) sorted with the most common characters first"""

    def coding_sort_key(t):
        """Custom key for sorting a string of 0's and 1's"""
        f, _ = t
        s = ''
        for i in f:
            if i == '0':
                s += '1'
            else:
                s += '2'
        return int(s)

    pairs = []
    for t in coding:
        pairs.append((coding[t], t))
    pairs.sort(key=coding_sort_key)
    return pairs

def get_table(filename):
    """Given a filename (string), return an encoding table (Dictionary) based upon the frequencies of each character in the file specified by the filename"""

    characters = Counter()
    with open(filename, 'r') as f:
        for line in f.readlines():
            characters.update(line)
    return Huffman_Coding(characters)

def encode(in_file_name, out_file_name=''):
    """Encode the text in 'in_file_name' (string) by creating a new encoding table and writing the encoded characters to 'out_file_name' (string)
    If no output filename is given, output file will have a .bin file extension.
    Returns a tuple of the encoding table (dictionary) and the number of padding bits at the end of the file.
    """

    if not out_file_name:
        try:
            i = len(in_file_name) - in_file_name[::-1].index('.') - 1
            out_file_name = in_file_name[:i] + ".bin"
        except ValueError:
            out_file_name = in_file_name + ".bin"

    table = get_table(in_file_name)
    binary_string = ''
    with open(in_file_name, 'r') as f:
        for line in f.readlines():
            for c in line:
                binary_string += table[c]

    padding = 8 - (len(binary_string)%8)
    integers = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string)-8, 8)]
    integers.append(int(binary_string[len(binary_string)-(len(binary_string)%8):len(binary_string)]+'0'*padding, 2))
    encoded_bytes = bytes(integers)
    
    with open(out_file_name, 'wb') as f:
        f.write(encoded_bytes)

    return (table, padding)

def decode(table, padding, in_file_name, out_file_name=''):
    """Decode the text in 'in_file_name' (string) by reading the table in the file, and return the resulting string.
    If an output filename is provided, it instead will write the resulting string to a file.
    """

    reverse_table = {b: c for c, b in table.items()}

    with open(in_file_name, 'rb') as f:
        encoded_bytes = f.read()

    from_bytes_string = ''
    for b in encoded_bytes:
        binary = str(bin(b))[2:]
        s = '0'*((8-len(binary))%8)+binary
        from_bytes_string += s
    from_bytes_string = from_bytes_string[:-padding]

    decoded_string = ''
    path = ''
    for b in from_bytes_string:
        path += b
        if path in reverse_table:
            decoded_string += reverse_table[path]
            path = ''

    if out_file_name:
        with open(out_file_name, 'w') as f:
            f.write(decoded_string)
    else:
        return decoded_string
