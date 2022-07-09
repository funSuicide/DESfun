from bitarray import bitarray
import split

replace_table = (58, 50, 42, 34, 26, 18, 10, 2,
                 60, 52, 44, 36, 28, 20, 12, 4,
                 62, 54, 46, 38, 30, 22, 14, 6,
                 64, 56, 48, 40, 32, 24, 16, 8,
                 57, 49, 41, 33, 25, 17, 9, 1,
                 59, 51, 43, 35, 27, 19, 11, 3,
                 61, 53, 45, 37, 29, 21, 13, 5,
                 63, 55, 47, 39, 31, 23, 15, 7)

invertation_replace_table = (40, 8, 48, 16, 56, 24, 64, 32,
                             39, 7, 47, 15, 55, 23, 63, 31,
                             38, 6, 46, 14, 54, 22, 62, 30,
                             37, 5, 45, 13, 53, 21, 61, 29,
                             36, 4, 44, 12, 52, 20, 60, 28,
                             35, 3, 43, 11, 51, 19, 59, 27,
                             34, 2, 42, 10, 50, 18, 58, 26,
                             33, 1, 41, 9, 49, 17, 57, 25)

key_replace_table = (57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
                     10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
                     63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
                     14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4)

extend_block_table = (32, 1, 2, 3, 4, 5,
                      4, 5, 6, 7, 8, 9,
                      8, 9, 10, 11, 12, 13,
                      12, 13, 14, 15, 16, 17,
                      16, 17, 18, 19, 20, 21,
                      20, 21, 22, 23, 24, 25,
                      24, 25, 26, 27, 28, 29,
                      28, 29, 30, 31, 32, 1)

key_select_table = (14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
                    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
                    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32)

s_table = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

           [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

           [[0, 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

           [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

           [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

           [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

           [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

           [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

p_table = (16, 7, 20, 21, 29, 12, 28, 17,
           1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9,
           19, 13, 30, 6, 22, 11, 4, 25)


def binary_encode(s: str) -> str:  # готово
    result = ''
    for element in s:
        tmp = bin(ord(element))[2:]
        tmp = '%08d' % int(tmp)
        result += tmp
    return result


def get_binary_block(text: str) -> list:  # готово
    result = []
    tmp = binary_encode(text)
    while len(tmp) % 64 != 0:
        tmp += '0'
    for i in range(0, len(tmp), 64):
        result.append(tmp[i:i + 64])
    return result


def p_expend(str: str) -> str:
    result = ''
    for i in extend_block_table:
        result += str[i - 1]
    return result


def replace_block(block: str) -> str:  # готово
    result = ''
    for i in replace_table:
        print(i-1)
        result += block[i - 1]
    return result


def end_replace_block(block: str) -> str:
    result = ''
    for i in invertation_replace_table:
        result += block[invertation_replace_table[i]]
    return result


def not_or(str1: str, str2: str) -> str:  # готово
    result = ''
    size = len(str1) if len(str1) < len(str2) else len(str2)
    for i in range(size):
        result += '0' if str1[i] == str2[i] else '1'
    return result


def extend_block(block: str) -> str:
    result = ''
    for i in extend_block_table:
        result += block[i - 1]
    return result


def s_extend(str: str, index: int) -> str:
    result = ''
    tmp_1 = int((str[0] + str[5]), 2)
    tmp_2 = int((str[1:4]), 2)
    tmp = s_table[index][tmp_1][tmp_2]
    return bin(tmp)


def process_key(key: str) -> str:
    result = ''
    for i in key_replace_table:
        result += key[i - 1]
    return result


def spin_key(key: str):
    tmp_key = process_key(key)
    first, second = tmp_key[0: 28], tmp_key[28: 56]
    spin_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)
    for i in range(1, 17):
        first_after_spin = first[spin_table[i - 1]:] + first[:spin_table[i - 1]]
        second_after_spin = second[spin_table[i - 1]:] + second[:spin_table[i - 1]]
        yield first_after_spin + second_after_spin


def key_selection_replacement(key: str) -> list:
    child_keys = []
    for child_key56 in spin_key(key):
        child_keys.append(replace_block(child_key56, key_select_table))
    return child_keys


def s_box_compression(right: str) -> str:
    result = []
    result_2 = ''
    for i in range(0, len(right), 6):
        result.append(right[i:i + 6])
    for j in range(8):
        result_2 += s_extend(result[j], j)
    return p_expend(result_2)


def function(right: str, key_i: str) -> str:
    right = extend_block(right)
    tmp = not_or(right, key_i)
    res_sbox = s_box_compression(tmp)
    return res_sbox


def encryption_cycle(block: str, key: str) -> str:
    new_key = process_key(key)
    child_keys = key_selection_replacement(new_key)
    for i in range(16):
        new_key = child_keys[i]
        left = block[0:32]
        right = block[32:64]
        new_left = right
        res_func = function(right, new_key)
        right = not_or(left, res_func)
        block = new_left + right
    return block[32:] + block[:32]


def encrypt(data: str, key: str) -> str:
    result = ''
    blocks = get_binary_block(data)
    bin_key = binary_encode(key)
    print(bin_key)
    print(len(bin_key))
    for i in blocks:
        rep_block = replace_block(i)
        c_block = encryption_cycle(rep_block, bin_key)
        end_rep_block = end_replace_block(c_block)
        result += end_rep_block
    return result




print(encrypt('Hello', 'Zanderrr'))