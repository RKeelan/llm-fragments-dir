import llm
import os
from pathlib import Path
from typing import List

@llm.hookimpl
def register_fragment_loaders(register):
    register("dir", directory_loader)

def is_probably_utf8(path: Path, *, sample_size: int = 4096) -> bool:
    """
    Check if a file is probably UTF-8 encoded by reading the first sample_size bytes. If they decode cleanly, the file
    is probably UTF-8 encoded.
    """
    with path.open("rb") as fp:
        head = fp.read(sample_size)

    try:
        head.decode("utf-8", errors="strict")
        return True
    except UnicodeDecodeError:
        return False

def directory_loader(argument: str) -> List[llm.Fragment]:
    """
    Load files from a local directory as fragments

    Argument is a path to a directory
    """
    dir_path = Path(argument)
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {argument}")
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {argument}")

    fragments = []
    
    for root, _, files in os.walk(dir_path):
        root_path = Path(root)
        for file in files:
            file_path = root_path / file
            if file_path.is_file() and is_probably_utf8(file_path):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    fragments.append(llm.Fragment(content, str(file_path.absolute())))
                except UnicodeDecodeError:
                    # Skip files that actually can't be decoded as UTF-8
                    continue

    return fragments
