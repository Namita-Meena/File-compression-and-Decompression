import os
from heapq import heappush, heappop, heapify
from collections import defaultdict, Counter

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

    def __lt__(self, nxt):
        return self.freq < nxt.freq

def build_huffman_tree(data):
    frequency = Counter(data)
    heap = [Node(freq, symbol) for symbol, freq in frequency.items()]
    heapify(heap)
    
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        left.huff = '0'
        right.huff = '1'
        
        newNode = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heappush(heap, newNode)
        
    return heap[0]

def build_codes(node, val=''):
    codes = {}
    if node is None:
        return codes

    if not node.left and not node.right:
        codes[node.symbol] = val or '0'
        
    codes.update(build_codes(node.left, val + '0'))
    codes.update(build_codes(node.right, val + '1'))
    return codes

def compress(data, codes):
    encoded_data = ''.join(codes[char] for char in data)
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data = encoded_data + '0' * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    encoded_data = padded_info + encoded_data
    byte_array = bytearray()
    
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        byte_array.append(int(byte, 2))
    
    return byte_array

def decompress(data, root):
    bit_string = ''.join(f"{byte:08b}" for byte in data)
    extra_padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-extra_padding]
    
    decoded_data = []
    current_node = root
    
    for bit in bit_string:
        current_node = current_node.left if bit == '0' else current_node.right
        if not current_node.left and not current_node.right:
            decoded_data.append(current_node.symbol)
            current_node = root
            
    return ''.join(decoded_data)

def compress_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.read()
    
    root = build_huffman_tree(data)
    codes = build_codes(root)
    compressed_data = compress(data, codes)
    
    with open(output_file, 'wb') as f:
        f.write(bytes(compressed_data))
    print(f"File {input_file} compressed to {output_file}")

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
        
    root = build_huffman_tree(''.join(chr(byte) for byte in data))
    decompressed_data = decompress(data, root)
    
    with open(output_file, 'w') as f:
        f.write(decompressed_data)
    print(f"File {input_file} decompressed to {output_file}")

# Example usage
compress_file('example.txt', 'example_compressed.huf')
decompress_file('example_compressed.huf', 'example_decompressed.txt')
