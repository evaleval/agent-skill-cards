"""Phase 1, skill identification.

Takes one skill folder and creates the run folder that every later phase reads. The run
folder holds a frozen copy of the skill's files under ``files/`` and ``snapshot.json`` with the
content hash, the source and the file list. The hash is the identity of a skill version, and
the name is a label.

The skill's files are read as bytes. They are never executed or imported.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
from datetime import date
from pathlib import Path

from skillcard import write_json

VERSION_CONTROL = {".git"}


def sha256_of(path: Path) -> str:
    """Return the lowercase hexadecimal sha256 of a file's content."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_hash(files: list[dict]) -> str:
    """Return the content hash of a file list by the rule of schema v1.2.

    The hash is sha256 over a list in the format of the sha256sum utility. The list has one
    line per file with the sha256 of the file's content, two spaces and the path relative to
    the skill folder, and the lines are sorted by path as bytes. File modes are not part of
    the hash, and files marked as left out are not on the list.
    """
    lines = sorted(
        (item["path"].encode("utf-8"), item["sha256"].encode("ascii"))
        for item in files
        if item["in_hash"]
    )
    listing = b"".join(digest + b"  " + path + b"\n" for path, digest in lines)
    return "sha256:" + hashlib.sha256(listing).hexdigest()


def list_files(folder: Path) -> tuple[list[dict], list[dict]]:
    """List every regular file under a folder, and what was skipped with the reason.

    Symbolic links are not followed and version control data is not read, because neither is
    content of the skill. A file name with a line break is refused, because it would make the
    list that the hash is computed over ambiguous.
    """
    files, skipped = [], []
    for root, folders, names in os.walk(folder):
        for name in sorted(folders + names):
            path = Path(root) / name
            relative = path.relative_to(folder).as_posix()
            info = path.lstat()
            mode = info.st_mode
            if name in VERSION_CONTROL:
                skipped.append({"path": relative, "reason": "version control data"})
            elif stat.S_ISLNK(mode):
                skipped.append({"path": relative, "reason": "symbolic link, not followed"})
            elif stat.S_ISDIR(mode):
                continue
            elif not stat.S_ISREG(mode):
                skipped.append({"path": relative, "reason": "not a regular file"})
            elif "\n" in relative:
                raise ValueError(f"a file name in {folder.name} contains a line break")
            else:
                files.append(
                    {
                        "path": relative,
                        "bytes": info.st_size,
                        "sha256": sha256_of(path),
                        "kind": "not examined",
                        "in_hash": True,
                        "executable": bool(mode & 0o111),
                    }
                )
        folders[:] = [name for name in folders if name not in VERSION_CONTROL]
    files.sort(key=lambda item: item["path"].encode("utf-8"))
    skipped.sort(key=lambda item: item["path"].encode("utf-8"))
    return files, skipped


def identify(skill_dir: Path, out_dir: Path, leave_out: tuple[str, ...] = ()) -> Path:
    """Freeze one skill folder and return the run folder created for it.

    ``leave_out`` names documents about the skill that are stored next to it, for example a
    card that a registry generated. They are copied and listed but are not part of the hash.
    The run folder is named after the skill folder and the first eight characters of the
    hash, so the same files always land in the same place. The snapshot records the folder
    name as the location and not the full path on the machine.
    """
    skill_dir = Path(skill_dir).resolve()
    if Path(out_dir).resolve().is_relative_to(skill_dir):
        raise ValueError("the output folder is inside the skill folder, choose another with --out")
    files, skipped = list_files(skill_dir)
    paths = {item["path"] for item in files}
    if "SKILL.md" not in paths:
        raise ValueError(f"{skill_dir.name} is not a skill folder, it has no SKILL.md")
    if missing := sorted(set(leave_out) - paths):
        raise ValueError(f"cannot leave out files that are not in the folder, {missing}")
    for item in files:
        item["in_hash"] = item["path"] not in leave_out
    digest = content_hash(files)

    run_dir = Path(out_dir) / f"{skill_dir.name}-{digest.removeprefix('sha256:')[:8]}"
    if run_dir.exists():
        if not (run_dir / "snapshot.json").is_file():
            raise ValueError(f"{run_dir} exists and is not a run folder")
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    snapshot = {
        "skill": skill_dir.name,
        "hash": digest,
        "source": {
            "kind": "local path",
            "location": skill_dir.name,
            "retrieved": date.today().isoformat(),
        },
        "files": files,
        "skipped": skipped,
    }
    write_json(run_dir / "snapshot.json", snapshot)
    for item in files:
        target = run_dir / "files" / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(skill_dir / item["path"], target)
    return run_dir
