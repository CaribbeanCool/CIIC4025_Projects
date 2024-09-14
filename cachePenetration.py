import sys
import array
import csv
import math

# Probability of false positives
p = 0.0000001


def calculate_n(fileDir):
    """
    Calculate the number of emails in the database.

    :param fileDir: The path to the file containing the emails.
    :return: The number of emails in the database.
    """
    with open(fileDir, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        return sum(1 for _ in reader)


def main():
    """
    Main function to run the bloom filter algorithm to check if an email is in the database or not, using the `Bloom Filter` algorithm.

    :return: None
    """
    if len(sys.argv) != 3:
        return

    # Calculate n
    n = calculate_n(sys.argv[1])

    # Calculate m
    m = math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2))))

    # Calculate k
    k = round((m / n) * math.log(2))

    # Number of Hashing functions
    NUM_OF_HASHES = k

    # Number of bits in bloom filter
    NUM_OF_BITS = m

    class BloomFilter:
        def __init__(self, nHash, size):
            self.nHash = nHash

            # size of the bloom filter
            self.size = size

            # determined size of array
            int_size = (size + 31) // 32
            self.bit_array = array.array('I', [0] * int_size)

        def hashFunction(self, item, seed):
            return hash((seed, item))

        def add(self, item):
            for i in range(0, self.nHash, 1):
                hashingIndex = self.hashFunction(item, i) % self.size
                self.bit_array[hashingIndex // 32] |= 1 << (hashingIndex % 32)

        def CheckDataBase(self, item):
            for i in range(self.nHash):
                index = self.hashFunction(item, i) % self.size
                if not (self.bit_array[index // 32] & (1 << (index % 32))):
                    return "Not in the DB"
            return "Probably in the DB"

    def createCheck(file_path):
        dataBaseCheck = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                email = row[0].strip()
                dataBaseCheck.append(email)
        return dataBaseCheck

    def CheckEmails(dataBase, dataBaseCheck, bloomFilter):
        for email in dataBase:
            bloomFilter.add(email)

        for email in dataBaseCheck:
            print(email + "," + bloomFilter.CheckDataBase(email))

    file_path = sys.argv[1]
    check_path = sys.argv[2]

    dataBase = createCheck(file_path)
    dataCheck = createCheck(check_path)
    bloomFilter = BloomFilter(NUM_OF_HASHES, NUM_OF_BITS)
    CheckEmails(dataBase, dataCheck, bloomFilter)


if __name__ == "__main__":
    main()
