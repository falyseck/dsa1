import os
import time
import sys
import tracemalloc

class UniqueInt:
    MIN_VAL = -1023
    MAX_VAL = 1023

    def __init__(self):
        self.seen = [False] * (UniqueInt.MAX_VAL - UniqueInt.MIN_VAL + 1)

    def _index(self, num):
        return num - UniqueInt.MIN_VAL

    def _is_valid_int(self, line):
        try:
            line = line.strip()
            if not line:
                return False
            parts = line.split()
            if len(parts) != 1:
                return False
            int(parts[0])
            return True
        except ValueError:
            return False

    def readNextItemFromFile(self, file_stream):
        while True:
            line = file_stream.readline()
            if not line:
                return None  # EOF
            line = line.strip()
            if self._is_valid_int(line):
                return int(line)
        return None

    def processFile(self, inputFilePath, outputFilePath):
        tracemalloc.start()
        start_time = time.time()

        with open(inputFilePath, "r") as f:
            while True:
                num = self.readNextItemFromFile(f)
                if num is None:
                    break
                index = self._index(num)
                self.seen[index] = True

        with open(outputFilePath, "w") as out:
            for i in range(len(self.seen)):
                if self.seen[i]:
                    out.write(str(i + UniqueInt.MIN_VAL) + "\n")

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Processed: {inputFilePath}")
        print(f"Runtime: {round((end_time - start_time) * 1000, 2)} ms")
        print(f"Memory used: {peak} bytes")
        print(f"Output written to: {outputFilePath}")
        print("-" * 50)


def run_all_samples(input_dir, result_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            result_filename = filename + "_results.txt"
            output_path = os.path.join(result_dir, result_filename)

            unique_int_processor = UniqueInt()
            unique_int_processor.processFile(input_path, output_path)

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    input_dir = os.path.join(base_path, "sample_inputs")
    result_dir = os.path.join(base_path, "sample_results")

    # Create result directory if it doesn't exist
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    run_all_samples(input_dir, result_dir)

