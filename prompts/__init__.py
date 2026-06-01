import csv


class BenchmarkCSV():
    def __init__(self, file: str):
        self.f = open(file, "r", encoding="utf-8")
        self.reader = csv.reader(self.f)
        next(self.reader, None)
        self.file = file

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = next(self.reader)
            return row[0], row[1] 
        except StopIteration:
            raise StopIteration
        except Exception as e:
            print(f"Error reading CSV: {e}")
            raise e

    def __len__(self):
        with open(self.file, "r", encoding="utf-8") as f:
            return sum(1 for _ in f) - 1

    def close(self):
        if not self.f.closed:
            self.f.close()
