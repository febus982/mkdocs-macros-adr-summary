from pathlib import Path


class InvalidFileError(Exception):
    def __init__(self, file_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path

    file_path: Path
