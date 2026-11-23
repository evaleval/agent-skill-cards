"""Shared setup: import this checkout's src/, and keep every test away from the network."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))

EXAMPLE = Path(__file__).parent / "fixtures" / "hello-skill"


@pytest.fixture(autouse=True)
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """No test may use the network, a model key or a token, whatever the machine has set."""
    for name in (
        "SKILLCARD_API_KEY",
        "OPENROUTER_API_KEY",
        "SKILLCARD_MODEL",
        "SKILLCARD_API_BASE",
        "GITHUB_TOKEN",
    ):
        monkeypatch.delenv(name, raising=False)

    def refuse(*args: object, **kwargs: object) -> None:
        raise AssertionError("a test tried to use the network")

    # Every request of the pipeline and of urllib goes through this method.
    monkeypatch.setattr("urllib.request.OpenerDirector.open", refuse)
    # git reads no settings of this machine, so that hooks or signing cannot change a test.
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)


@pytest.fixture
def skill(tmp_path: Path) -> Path:
    """A clean copy of the example skill, so that stray files next to it cannot change the hash."""
    stray = shutil.ignore_patterns(".DS_Store", "__pycache__")
    return Path(shutil.copytree(EXAMPLE, tmp_path / "hello-skill", ignore=stray))


def git(folder: Path, *arguments: str, given: str | None = None) -> str:
    """Run git in a test repository and return what it printed. ``given`` is its input."""
    command = [
        "git",
        "-C",
        str(folder),
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.invalid",
    ]
    done = subprocess.run(
        [*command, *arguments], input=given, capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


@pytest.fixture
def repository(tmp_path: Path, skill: Path) -> Path:
    """A git repository on this machine that holds the example skill under ``skills/hello-skill``."""
    root = tmp_path / "repository"
    shutil.copytree(skill, root / "skills" / "hello-skill")
    (root / "README.md").write_text("A repository with one skill.\n", encoding="utf-8")
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "add the skill")
    return root
