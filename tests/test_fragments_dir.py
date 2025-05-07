import os
import pathlib
import pytest
import tempfile
from llm_fragments_dir import directory_loader, is_probably_utf8


def test_directory_loader_with_nonexistent_directory():
    with pytest.raises(ValueError, match="Directory does not exist"):
        directory_loader("/nonexistent/path")


def test_directory_loader_with_file():
    with tempfile.NamedTemporaryFile() as tmp:
        with pytest.raises(ValueError, match="Path is not a directory"):
            directory_loader(tmp.name)


def test_directory_loader_with_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        fragments = directory_loader(tmpdir)
        assert len(fragments) == 0


def test_directory_loader_with_text_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        # Create some text files
        file1 = tmpdir_path / "file1.txt"
        file2 = tmpdir_path / "file2.txt"
        file1.write_text("Hello, World!", encoding="utf-8")
        file2.write_text("Another text file", encoding="utf-8")

        fragments = directory_loader(tmpdir)
        assert len(fragments) == 2

        # Check fragment contents and identifiers
        fragment_contents = {str(fragment) for fragment in fragments}
        assert "Hello, World!" in fragment_contents
        assert "Another text file" in fragment_contents

        fragment_sources = {fragment.source for fragment in fragments}
        assert str(file1) in fragment_sources
        assert str(file2) in fragment_sources


def test_directory_loader_with_nested_directories():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        # Create nested directory structure
        nested_dir = tmpdir_path / "nested"
        nested_dir.mkdir()
        file1 = tmpdir_path / "file1.txt"
        file2 = nested_dir / "file2.txt"
        file1.write_text("Root file", encoding="utf-8")
        file2.write_text("Nested file", encoding="utf-8")

        fragments = directory_loader(tmpdir)
        assert len(fragments) == 2

        # Check fragment contents and identifiers
        fragment_contents = {str(fragment) for fragment in fragments}
        assert "Root file" in fragment_contents
        assert "Nested file" in fragment_contents

        fragment_sources = {fragment.source for fragment in fragments}
        assert str(file1) in fragment_sources
        assert str(file2) in fragment_sources


def test_directory_loader_skips_binary_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        # Create a text file and a binary file
        text_file = tmpdir_path / "text.txt"
        binary_file = tmpdir_path / "binary.bin"
        text_file.write_text("Text content", encoding="utf-8")
        # Create a binary file with invalid UTF-8 sequence
        binary_file.write_bytes(b"\xff\xfe\x00\x01\x02\x03")

        fragments = directory_loader(tmpdir)
        assert len(fragments) == 1
        assert str(fragments[0]) == "Text content"
        assert fragments[0].source == str(text_file)


def test_is_probably_utf8():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        # Test with UTF-8 text file
        text_file = tmpdir_path / "text.txt"
        text_file.write_text("Hello, World!", encoding="utf-8")
        assert is_probably_utf8(text_file)

        # Test with binary file containing invalid UTF-8 sequence
        binary_file = tmpdir_path / "binary.bin"
        binary_file.write_bytes(b"\xff\xfe\x00\x01\x02\x03")
        assert not is_probably_utf8(binary_file)

        # Test with empty file
        empty_file = tmpdir_path / "empty.txt"
        empty_file.touch()
        assert is_probably_utf8(empty_file)
