import hash, tree, database, file_scanner, config_reader, os

class file_manager:
    def __init__(self):
        self.scanner = file_scanner.file_scanner()
        self.config = config_reader.config("config.env")
        self.database = database.Database()

    def _get_last_commit(self):
        commit_file = self.config.get_commit_file()

        last_line = self._get_last_line_of_file(commit_file)
        return self.database.retrieve_object(last_line)

    def _get_last_line_of_file(self, file):
        with open(file, 'rb') as f:
            try:  # catch OSError in case of a one line file 
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            return f.readline().decode()
            

    def update_files(self):
        files = self.scanner.scan()

if __name__ == "__main__":
    f = file_manager()
    print(f._get_last_commit().data)