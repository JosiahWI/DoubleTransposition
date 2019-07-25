#!/usr/bin/python3


import sys
import os
import random


class Matrix:


    def __init__(self, key, text, block_size):
        self.key = key
        print("gen reverse key")
        self.reverse_key = self.sort_matrix(self.key, range(len(key)))
        text = text.lower()
        t = ""
        for char in text:
            if char.isalpha():
                t += char
        text = t
        self.width = len(key)
        text = add_padding(text, 'e', self.width)
        self.height = int(len(text) / self.width)
        self.block_size = 5
        self.matrix = text_to_matrix(text, self.height)


    def __str__(self):
        text = ""
        for row in self.matrix:
            for char in row:
                text += char
        if self.block_size:
            text = self.add_spaces(text)
        return text


    def sort_matrix(self, key, matrix):
        zipped_columns = [pair for pair in zip(list(key), matrix)]
        print(zipped_columns)
        x =  [pair for pair in sorted(zipped_columns, key = lambda x: x[0])]
        print(x)
        return [pair[1] for pair in x]

    def sort(self):
        print("sort")
        self.matrix = self.sort_matrix(self.key, self.matrix)


    def unsort(self):
        print("unsort")
        self.matrix = self.sort_matrix(self.reverse_key, self.matrix)


    def swap_rows_columns(self):
        text = ""
        width = len(self.matrix[0])
        height = len(self.matrix)
        for x in range(width):
            for y in range(height):
                text += self.matrix[y][x]
        self.matrix = text_to_matrix(text, width)



    def transpose(self):
        text = ""
        height = len(self.matrix[0])
        for x in self.matrix:
            for char in x:
                text += char
        self.matrix = text_to_matrix(text, height)


    def add_spaces(self, text):
        new_text = ""
        i = 0
        for char in text:
            if i == self.block_size:
                new_text += " "
                i = 0
            new_text += char
            i += 1
        return new_text


def encrypt(key, text, block_size=5):
    matrix = Matrix(key, text, block_size)
    # First transposition.
    matrix.swap_rows_columns()
    matrix.sort()
    matrix.transpose()
    # Second transposition.
    matrix.swap_rows_columns()
    matrix.sort()
    matrix.transpose()

    f = open("ciphertext.txt", "w+")
    f.write(str(matrix))
    f.close()
    return str(matrix)


def decrypt(key, text, block_size=0):
    # First de-transposition.
    matrix = Matrix(key, text, block_size)
    matrix.transpose()
    matrix.unsort()
    matrix.swap_rows_columns()
    # Second de-transposition.
    matrix.transpose()
    matrix.unsort()
    matrix.swap_rows_columns()

    f = open("plaintext.txt", "w+")
    f.write(str(matrix))
    f.close()
    return str(matrix)
    
    

def text_to_matrix(text, width):
    matrix = []
    height = int(len(text)/width)
    for column_index in range(width):
        column_start, column_end = column_index*height, (column_index+1)*height
        matrix.append(text[column_start:column_end])
    return matrix


def matrix_to_text(matrix, block_size):
    text = ""
    for row in matrix:
        for char in row:
            text += char
    text = add_spaces(text, block_size)
    return text
    

def add_padding(text, letter, offset_size):
    padding_size = offset_size - (len(text) % offset_size)
    if padding_size != offset_size:
        text += (letter * padding_size)
    return text


if __name__ == '__main__':
    if len(sys.argv) < 4:
        mode = input("Do you want to encrypt or decrypt? e or d: >> ")
        key = input("the key: >> ")
        text = input("the message, optionally a file name: >> ")
    else:
        mode = sys.argv[1]
        key = sys.argv[2]
        text = sys.argv[3]
    
    if text in os.listdir("./"):
        f = open(text)
        text = f.read()
        f.close()

    if mode == 'e':
        print(encrypt(key, text))
    elif mode == 'd':
        print(decrypt(key, text))