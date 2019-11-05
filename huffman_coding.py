#!/usr/bin/env python

"""Implementation of the Huffman Coding algorithm to efficiently encode and decode text files"""

from queue import PriorityQueue
from collections import Counter
import json
import sys


def reverse_table(coding):
    """Return a copy of the coding table (Dictionary) with tuples in reverse order"""

    return {b: c for c, b in coding.items()}


def sorted_table(coding):
    """Return a copy of the coding table (Dictionary) sorted with the most common characters first"""

    def coding_sort_key(t):
        """Custom key for sorting a string of 0's and 1's"""
        f, _ = t
        s = ""
        for i in f:
            if i == "0":
                s += "1"
            else:
                s += "2"
        return int(s)

    pairs = []
    for t in coding:
        pairs.append((coding[t], t))
    pairs.sort(key=coding_sort_key)
    return reverse_table(dict(pairs))


class Priority_Node:
    """Priority_Node class used to form the tree used in Huffman_Coding"""

    def __init__(self, data, priority):
        self.data = data
        self.priority = priority
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.priority < other.priority


def Huffman_Coding(freq):
    """Takes a Counter object of frequencies of each character as 'freq'
    Outputs an encoding table (Dictionary of characters and their encoded representation as a string of 0's and 1's)
    """

    def get_codings(coding, path, parent):
        """Recursively adds the binary code for each character to coding (dict)"""
        left = parent.left
        right = parent.right
        if left.data:
            coding[left.data] = path + "0"
        else:
            get_codings(coding, path + "0", left)
        if right.data:
            coding[right.data] = path + "1"
        else:
            get_codings(coding, path + "1", right)

    heap = PriorityQueue()
    for c in freq:
        heap.put(Priority_Node(c, freq[c]))
    root = None
    while True:
        left = heap.get()
        if heap.empty():
            root = left
            break
        right = heap.get()
        new_node = Priority_Node(0, left.priority + right.priority)
        new_node.left = left
        new_node.right = right
        heap.put(new_node)
    coding = dict()
    get_codings(coding, "", root)
    return coding


def create_table(
    filename, table_file_name="", extra_chars=[chr(i) for i in range(128)]
):
    """Given a filename, returns an encoding table (Dictionary) based upon the frequencies of each character in the file specified by the filename
    If 'table_file_name' is provided, also writes the new encoding table to a file in JSON format
    By default, also adds ASCII characters to the table to avoid problems if another file has characters that do not appear in the file used to generate the table.
    """

    characters = Counter()
    with open(filename, "r") as f:
        for line in f.readlines():
            characters.update(line)
    # if there are any common characters (128 ASCII characters by default) not already included in the Counter, add them
    for char in extra_chars:
        if char not in characters:
            characters.update(char)

    table = Huffman_Coding(characters)

    if table_file_name:
        with open(table_file_name, "w") as table_file:
            json.dump(table, table_file)
    return table


def get_table(filename):
    """Given a filename, return the stored encoding table (JSON) as a Dictionary."""

    with open(filename, "r") as table_file:
        table = json.load(table_file)
    return table


class Node:
    """Node class used for the tree when decoding"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def get_tree(table):
    """Given an encoding table as a dictionary, create the associated Huffman tree (for decoding). Return root Node of the tree.
    """

    root = Node(None)
    for char in table:
        current = root
        for b in table[char]:
            if b == "0":
                if current.left:
                    current = current.left
                else:
                    current.left = Node(None)
                    current = current.left
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = Node(None)
                    current = current.right
        current.data = char
    return root


def encode(in_file_name, table_file_name, out_file_name=""):
    """Encode the text in 'in_file_name' using the encoding table in 'table_file_name' (JSON) and write the encoded characters to 'out_file_name'
    If 'table_file_name' file does not exist, instead create a new encoding table using the characters in 'in_file_name' and store in a new file 'table_file_name'
    If no output filename is given, output file with .bin file extension
    """

    if not out_file_name:
        try:
            i = len(in_file_name) - in_file_name[::-1].index(".") - 1
            out_file_name = in_file_name[:i] + ".bin"
        except ValueError:
            out_file_name = in_file_name + ".bin"

    try:
        table = get_table(table_file_name)
    except FileNotFoundError:
        table = create_table(in_file_name, table_file_name)

    binary_string = ""
    with open(in_file_name, "r") as f:
        for line in f.readlines():
            for c in line:
                binary_string += table[c]

    padding = 8 - (len(binary_string) % 8)
    integers = [
        int(binary_string[i : i + 8], 2)
        for i in range(0, len(binary_string) - 8, 8)
    ]
    integers.append(
        int(
            binary_string[
                len(binary_string)
                - (len(binary_string) % 8) : len(binary_string)
            ]
            + "0" * padding,
            2,
        )
    )
    encoded_bytes = bytes(integers)
    with open(out_file_name, "wb") as f:
        # write the padding to the file first
        f.write(bytes([padding]))
        f.write(encoded_bytes)


def decode(in_file_name, table_file_name, out_file_name=""):
    """Decode the text in 'in_file_name' using the table in 'table_file_name', and return the resulting string.
    If an output filename is provided, instead write the resulting string to a file.
    """

    table = get_table(table_file_name)
    root = get_tree(table)

    with open(in_file_name, "rb") as f:
        # get the padding first
        padding = ord(f.read(1))
        encoded_bytes = f.read()

    from_bytes_string = ""
    for b in encoded_bytes:
        binary = str(bin(b))[2:]
        s = "0" * ((8 - len(binary)) % 8) + binary
        from_bytes_string += s
    from_bytes_string = from_bytes_string[:-padding]

    decoded_string = ""
    current = root
    for b in from_bytes_string:
        if b == "0":
            current = current.left
        else:
            current = current.right
        if current.data:
            decoded_string += current.data
            current = root

    if out_file_name:
        with open(out_file_name, "w") as f:
            f.write(decoded_string)
    else:
        return decoded_string


if __name__ == "__main__":

    try:
        if sys.argv[1] == "create_table":
            filename = sys.argv[2]
            if len(sys.argv) == 4:
                table_file_name = sys.argv[3]
                print(create_table(filename, table_file_name))
            elif len(sys.argv) == 5:
                table_file_name = sys.argv[3]
                extra_chars = sys.argv[4]
                print(create_table(filename, table_file_name, extra_chars))
            else:
                print(create_table(filename))
        elif sys.argv[1] == "get_table":
            filename = sys.argv[2]
            print(get_table(filename))
        elif sys.argv[1] == "encode":
            in_file_name = sys.argv[2]
            table_file_name = sys.argv[3]
            if len(sys.argv) == 5:
                out_file_name = sys.argv[4]
                encode(in_file_name, table_file_name, out_file_name)
            else:
                encode(in_file_name, table_file_name)
        elif sys.argv[1] == "decode":
            in_file_name = sys.argv[2]
            table_file_name = sys.argv[3]
            if len(sys.argv) == 5:
                out_file_name = sys.argv[4]
                decode(in_file_name, table_file_name, out_file_name)
            else:
                print(decode(in_file_name, table_file_name))
        else:
            print("Command not recognized.")
    except IndexError:
        print("Insufficient number of arguments.")
    except FileNotFoundError:
        print("Incorrect filename.")
