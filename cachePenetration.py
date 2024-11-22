import sys
import array
import csv
import math
import hashlib

# Probability of false positives
p = 0.0000001


def calculate_n(file_path):
    """
    Calculate the number of emails in the database.

    :param file_path: The path to the file containing the emails.
    :return: The number of emails in the database.
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return sum(1 for _ in reader)


def make_bit_array(bit_size, fill=0):
    """
    Create a bit array of the given size.

    :param bit_size: The size of the bit array.
    :param fill: Initial fill value (0 or 1).
    :return: Bit array.
    """
    int_size = (bit_size + 31) // 32
    fill_value = 0xFFFFFFFF if fill else 0
    bit_array = array.array('I', (fill_value,) * int_size)
    return bit_array


def test_bit(array_name, bit_num):
    """
    Test if the bit at 'bit_num' is set.

    :param array_name: Bit array.
    :param bit_num: Bit index.
    :return: True if set, else False.
    """
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return (array_name[record] & mask) != 0


def set_bit(array_name, bit_num):
    """
    Set the bit at 'bit_num'.

    :param array_name: Bit array.
    :param bit_num: Bit index.
    """
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask


class BloomFilter:
    def __init__(self, n_hashes, size):
        self.n_hashes = n_hashes
        self.size = size
        self.bit_array = make_bit_array(size)

    def hash_function(self, item, seed):
        """
        Hash function using SHA256 with seed.

        :param item: Item to hash.
        :param seed: Seed for the hash.
        :return: Hash value.
        """
        hash_obj = hashlib.sha256(f"{seed}:{item}".encode())
        return int(hash_obj.hexdigest(), 16)

    def add(self, item):
        """
        Add an item to the Bloom Filter.

        :param item: Item to add.
        """
        for seed in range(self.n_hashes):
            result = self.hash_function(item, seed)
            set_bit(self.bit_array, result % self.size)

    def check(self, item):
        """
        Check if an item is in the Bloom Filter.

        :param item: Item to check.
        :return: True if probably in, False if definitely not.
        """
        for seed in range(self.n_hashes):
            result = self.hash_function(item, seed)
            if not test_bit(self.bit_array, result % self.size):
                return False
        return True


def main():
    if len(sys.argv) != 3:
        return

    input_file = sys.argv[1]
    check_file = sys.argv[2]

    # Calculate the number of items in the input database
    n = calculate_n(input_file)

    # Calculate optimal Bloom Filter parameters
    m = math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2))))
    k = round((m / n) * math.log(2))

    # Create a Bloom Filter
    bloom = BloomFilter(k, m)

    # Add emails from the input file to the Bloom Filter
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            email = row[0]
            bloom.add(email)

    # Check emails from the check file against the Bloom Filter
    with open(check_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            email = row[0]
            result = "Probably in the DB" if bloom.check(
                email) else "Not in the DB"
            print(f"{email},{result}")


if __name__ == "__main__":
    main()