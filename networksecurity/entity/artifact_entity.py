from dataclasses import dataclass
@dataclass
class Artifact:
    train_file_path: str
    test_file_path: str