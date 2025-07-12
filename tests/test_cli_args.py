import argparse

import pytest

from app.cli_args import parse_args


def test_parse_args_with_config(monkeypatch):
    """Test that --config argument is parsed correctly."""
    monkeypatch.setattr("sys.argv", ["main.py", "--config", "config.yml"])
    args = parse_args()
    assert isinstance(args, argparse.Namespace)
    assert args.config == "config.yml"


def test_parse_args_without_config(monkeypatch):
    """Test default behavior when --config is not provided."""
    monkeypatch.setattr("sys.argv", ["main.py"])
    args = parse_args()
    assert isinstance(args, argparse.Namespace)
    assert args.config is None


def test_parse_args_invalid_type(monkeypatch):
    """Test simulated invalid config input that should still be string-parsed."""
    monkeypatch.setattr("sys.argv", ["main.py", "--config", "123"])  # still str
    args = parse_args()
    assert isinstance(args.config, str)
    assert args.config == "123"


def test_parse_args_rejects_non_str(monkeypatch):
    """This test ensures the type check is working (artificial edge case)."""

    # We bypass argparse by mocking its output directly
    class FakeArgs:
        config = 123  # not a str

    monkeypatch.setattr(
        "app.cli_args.argparse.ArgumentParser.parse_args", lambda self: FakeArgs()
    )

    with pytest.raises(TypeError, match="Expected --config to be a string"):
        parse_args()
