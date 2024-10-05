import config_reader, os

class file_scanner:
    def __init__(self):
        self.config = config_reader.config("config.env")
        self.directory = self.config.get_main_directory()
        self.exclude = set(["my_git"])

    def scan(self):
        results = set()
        for root, dirs, files in os.walk(self.directory):
            dirs[:] = [d for d in dirs if d not in self.exclude]
            for file in files:
                full_path = os.path.join(root, file)
                results.add(full_path)
        return results


if __name__ == "__main__":
    c = file_scanner()
    print(c.scan())
