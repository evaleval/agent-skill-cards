"""Phase 1, skill identification.

Takes one skill, as a local folder or as a repository with a path and a commit, and creates
the run folder that every later phase reads. The run folder holds a frozen copy of the
skill's files under ``files/`` and ``snapshot.json`` with the identity of the skill: the place
it comes from, the hash of its files and the file list. The place says which skill it is, the
hash says which version, and the name is a label.

The hash rule is called ``skill-tree-v2``. Regular files retain the sha256sum-style records
of v1. A symbolic link contributes the sha256 of its target text as a typed record; its
target is never followed or stored in the run. For a repository the files are read as the
commit stores them and not from a checked-out copy. File modes and version control data are
not part of the hash.

The skill's files are read as bytes. They are never executed or imported.
"""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from skillcard import HASH_SCHEME, quoted, read_frontmatter, read_json, write_json
from skillcard.index import (
    IdentityIndex,
    card_content_record,
    compatible_content,
    normalize_repository,
    source_identity,
    source_identity_from_card,
)

VERSION_CONTROL = {".git"}


def _contains_control_character(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


SCRIPT_ENDINGS = {
    ".bash", ".bat", ".c", ".cc", ".cjs", ".cmd", ".cpp", ".cs", ".dockerfile", ".go", ".java",
    ".js", ".jsx", ".kt", ".lua", ".mjs", ".php", ".pl", ".ps1", ".py", ".rb", ".rs", ".sh",
    ".swift", ".ts", ".tsx", ".zsh",
}  # fmt: skip
SCRIPT_NAMES = {"dockerfile", "makefile"}
DOCUMENT_ENDINGS = {".adoc", ".htm", ".html", ".markdown", ".md", ".mdx", ".rst", ".txt"}
DOCUMENT_NAMES = {"authors", "changelog", "copying", "licence", "license", "notice", "readme"}

# The case in which this version of a skill already has a card, see compare_with_cards.
ALREADY = "same place, same files"

GIT_SECONDS = 600
GIT_ENVIRONMENT = {
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_LFS_SKIP_SMUDGE": "1",
    "GIT_ALLOW_PROTOCOL": "https:http:ssh:git:file",
}


class AlreadyKnown(Exception):
    """This version of the skill already has a card. ``cards`` names the card files."""

    def __init__(self, cards: list[str]) -> None:
        super().__init__(f"this version of the skill already has a card, {', '.join(cards)}")
        self.cards = cards


def sha256_of(path: Path) -> str:
    """Return the lowercase hexadecimal sha256 of a file's content."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_hash(files: list[dict], scheme: str = HASH_SCHEME) -> str:
    """Return the content hash of a file list using the named hash scheme.

    V1 hashes regular files in sha256sum format. V2 preserves those records and gives a link
    a typed, NUL-prefixed record so it cannot be confused with a regular file of the same
    name. Files marked as left out are not on the list.
    """
    if scheme not in {"skill-tree-v1", "skill-tree-v2"}:
        raise ValueError(f"unsupported hash scheme {scheme!r}")
    lines = sorted(
        (
            item["path"].encode("utf-8"),
            item["sha256"].encode("ascii"),
            item.get("file_type", "regular"),
        )
        for item in files
        if item["in_hash"]
    )
    if any(file_type not in {"regular", "symbolic link"} for _, _, file_type in lines):
        raise ValueError("a file has an unknown file type")
    if scheme == "skill-tree-v1" and any(file_type != "regular" for _, _, file_type in lines):
        raise ValueError("skill-tree-v1 cannot hash symbolic links")
    listing = b"".join(
        digest + (b"  " if file_type == "regular" else b"  \0link\0") + path + b"\n"
        for path, digest, file_type in lines
    )
    return "sha256:" + hashlib.sha256(listing).hexdigest()


def kind_of(path: str, data: bytes) -> str:
    """Say whether a file is a script, a document, data or binary.

    This is a simple rule by content and file ending. A file that does not decode as text is
    binary. A file that starts with a shebang line or has the ending of a program is a script.
    Prose and markup are documents, and everything else is data.
    """
    if b"\0" in data:
        return "binary"
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return "binary"
    name = path.rsplit("/", 1)[-1].lower()
    ending = "." + name.rsplit(".", 1)[1] if "." in name else ""
    if text.startswith("#!") or ending in SCRIPT_ENDINGS or name in SCRIPT_NAMES:
        return "script"
    if ending in DOCUMENT_ENDINGS or (not ending and name in DOCUMENT_NAMES):
        return "document"
    return "data"


def file_entry(path: str, data: bytes, executable: bool, file_type: str = "regular") -> dict:
    """Return the entry of one file in the file list."""
    return {
        "path": path,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "kind": kind_of(path, data) if file_type == "regular" else "data",
        "file_type": file_type,
        "in_hash": True,
        "executable": executable,
        "exclusion_reason": "none",
    }


def list_files(folder: Path) -> tuple[list[dict], list[dict]]:
    """List files and symbolic links without following them, plus skipped entries.

    A symbolic link's target text is hashed as data but never stored or followed. Version
    control data is excluded. A file name with a line break is refused because it would make
    the list that the hash is computed over ambiguous.
    """
    files, skipped = [], []
    for root, folders, names in os.walk(folder):
        for name in sorted(folders + names):
            path = Path(root) / name
            relative = path.relative_to(folder).as_posix()
            mode = path.lstat().st_mode
            if _contains_control_character(relative):
                raise ValueError(f"a file name in {folder.name} contains a control character")
            if name.lower() in VERSION_CONTROL:
                skipped.append({"path": relative, "reason": "version control data"})
            elif stat.S_ISLNK(mode):
                target = os.fsencode(os.readlink(path))
                files.append(file_entry(relative, target, False, "symbolic link"))
            elif stat.S_ISDIR(mode):
                continue
            elif not stat.S_ISREG(mode):
                skipped.append({"path": relative, "reason": "not a regular file"})
            else:
                files.append(file_entry(relative, path.read_bytes(), bool(mode & 0o111)))
        folders[:] = [name for name in folders if name.lower() not in VERSION_CONTROL]
    files.sort(key=lambda item: item["path"].encode("utf-8"))
    skipped.sort(key=lambda item: item["path"].encode("utf-8"))
    return files, skipped


# ---------------------------------------------------------------------------------------
# The place of a skill
# ---------------------------------------------------------------------------------------


def repository_address(repository: str) -> str:
    """Return the address git reads from.

    A folder on this machine is given by its full path, because git runs in another folder.
    ``owner/repo`` stands for a repository on GitHub, unless a folder of that name exists.
    """
    if repository.startswith("-"):
        raise ValueError(f"{repository} is not a repository")
    if "://" not in repository and Path(repository).exists():
        return str(Path(repository).resolve())
    if re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
        return f"https://github.com/{repository}"
    return repository


def repository_name(address: str) -> str | None:
    """Return ``host/owner/repo`` for the address of a remote repository, without credentials.

    A repository on this machine has no such name, and ``None`` is returned for it.
    """
    match = re.fullmatch(r"(?:https?|ssh|git)://(?:[^@/]*@)?([^/]+)/(.+)", address)
    match = match or re.fullmatch(r"[\w.-]+@([^:/]+):(.+)", address)
    if not match:
        return None
    host, rest = match.group(1).lower(), match.group(2).strip("/")
    return f"{host}/{rest.removesuffix('.git')}"


def skill_id(address: str, path: str) -> str:
    """Return the place of a skill, the repository and the path of the skill inside it."""
    name = repository_name(address)
    return f"{name}#{path or '.'}" if name else "none"


def _identity_url(address: str) -> str | None:
    """Return a public-form repository URL when the address names a remote repository."""
    name = repository_name(address)
    if name:
        return f"https://{name}"
    return normalize_repository(address)


def _checkout_source(skill_dir: Path) -> dict | None:
    """Find the origin and commit of a local skill folder inside a Git checkout."""
    try:
        root = Path(_git(skill_dir, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        relative = skill_dir.resolve().relative_to(root).as_posix()
        remote = _git(root, "remote", "get-url", "origin").decode("utf-8", "replace").strip()
        commit = _git(root, "rev-parse", "HEAD").decode("ascii").strip()
        changed = bool(
            _git(root, "status", "--porcelain", "--untracked-files=all", "--", relative).strip()
        )
    except (ValueError, OSError):
        return None
    repository = _identity_url(remote)
    if not repository:
        return None
    return {
        "repository": repository,
        "path": relative,
        "commit": commit,
        "worktree_changed": changed,
    }


def location_text(source: dict) -> str:
    """Say where the files come from in the words a card uses."""
    if source["kind"] != "repository":
        return source["location"]
    name = repository_name(source["repository"])
    if name and name.startswith("github.com/"):
        return f"GitHub {name.removeprefix('github.com/')}, path {source['path'] or '.'}"
    return f"{name or source['repository']}, path {source['path'] or '.'}"


def place_of_location(location: object) -> str | None:
    """Read the place of a skill back from the location text of a card."""
    if not isinstance(location, str):
        return None
    if match := re.fullmatch(r"GitHub ([^/\s]+/[^/\s,]+), path (.+)", location):
        return f"github.com/{match.group(1)}#{match.group(2)}"
    if match := re.fullmatch(r"([^\s,]+/[^\s,]+), path (.+)", location):
        return f"{match.group(1)}#{match.group(2)}"
    return None


def _same_place(one: str | None, other: str | None) -> bool:
    """Compare two places. The repository part is compared without regard to case."""
    if not one or not other or "none" in (one, other):
        return False
    one_repository, _, one_path = one.partition("#")
    other_repository, _, other_path = other.partition("#")
    return one_repository.lower() == other_repository.lower() and one_path == other_path


def _card_source_identity(which: dict) -> dict | None:
    return source_identity_from_card({"which_files": which})


def _file_comparison(current: list[dict], previous: list[dict], card: str) -> dict:
    """Compare each path in two manifests without treating a shared file as a full match."""
    left = {one["path"]: one for one in current if isinstance(one, dict)}
    right = {one["path"]: one for one in previous if isinstance(one, dict)}
    common = sorted(left.keys() & right.keys())
    same, changed = [], []
    for path in common:
        one, other = left[path], right[path]
        same_content = one.get("sha256") == other.get("sha256") and one.get(
            "file_type", "regular"
        ) == other.get("file_type", "regular")
        if same_content:
            same.append(path)
        else:
            changed.append(
                {
                    "path": path,
                    "current_sha256": one.get("sha256"),
                    "card_sha256": other.get("sha256"),
                    "current_type": one.get("file_type", "regular"),
                    "card_type": other.get("file_type", "regular"),
                }
            )
    return {
        "card": card,
        "same": same,
        "changed": changed,
        "only_current": sorted(left.keys() - right.keys()),
        "only_card": sorted(right.keys() - left.keys()),
    }


def compare_with_cards(snapshot: dict, cards_dir: Path | None) -> dict:
    """Compare a skill with card files by source, compatible content, and individual files.

    The result names the cards for each case. Persistent decisions and observations are kept
    separately by :class:`skillcard.index.IdentityIndex`.
    """
    found: dict = {
        "compared_with": 0,
        "same place, same files": [],
        "same place, other files": [],
        "other place, same files": [],
        "other files, same SKILL.md": [],
        "file_comparisons": [],
    }
    if cards_dir is None or not Path(cards_dir).is_dir():
        return found
    skill_md = next((f["sha256"] for f in snapshot["files"] if f["path"] == "SKILL.md"), None)
    for path in sorted(Path(cards_dir).glob("*.json")):
        try:
            card = read_json(path)
            which = card["which_files"]
            card_place = place_of_location(which["source"].get("location"))
            card_skill_md = next(
                (f["sha256"] for f in which["files"] if f["path"] == "SKILL.md"), None
            )
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            continue
        found["compared_with"] += 1
        card_source = _card_source_identity(which)
        same_place = (
            source_identity({"source_identity": snapshot.get("source_identity")}) == card_source
            if snapshot.get("source_identity") and card_source
            else _same_place(snapshot["skill_id"], card_place)
        )
        same_content = compatible_content(snapshot, card_content_record(card))
        if same_content:
            found["same place, same files" if same_place else "other place, same files"].append(
                path.name
            )
        else:
            if same_place:
                found["same place, other files"].append(path.name)
            elif skill_md and card_skill_md == skill_md:
                found["other files, same SKILL.md"].append(path.name)
            comparison = _file_comparison(snapshot["files"], which.get("files", []), path.name)
            if comparison["same"] or comparison["changed"]:
                found["file_comparisons"].append(comparison)
    return found


# ---------------------------------------------------------------------------------------
# Reading the files of a skill from a commit
# ---------------------------------------------------------------------------------------


def _git(folder: Path, *arguments: str, stdin: bytes | None = None) -> bytes:
    """Run one git command in ``folder`` and return what it printed."""
    command = ["git", "-c", f"core.hooksPath={os.devnull}", "-C", str(folder), *arguments]
    try:
        done = subprocess.run(
            command,
            input=stdin,
            capture_output=True,
            env={**os.environ, **GIT_ENVIRONMENT},
            timeout=GIT_SECONDS,
            check=False,
        )
    except FileNotFoundError:
        raise ValueError("git was not found, reading a repository needs git") from None
    except subprocess.TimeoutExpired:
        raise ValueError(f"git {arguments[0]} took longer than {GIT_SECONDS} seconds") from None
    if done.returncode != 0:
        said = [
            line for line in done.stderr.decode("utf-8", "replace").splitlines() if line.strip()
        ]
        # git names the cause on a line that starts with fatal or error.
        cause = next((line for line in said if line.startswith(("fatal:", "error:"))), None)
        command = next(word for word in arguments if not word.startswith("-"))
        raise ValueError(f"git {command} failed, {cause or (said[-1] if said else 'no message')}")
    return done.stdout


def read_commit(
    repository: str, path: str, commit: str | None, work: Path
) -> tuple[str, list[dict], list[dict], dict[str, bytes]]:
    """Read the files of the skill at ``path`` as one commit of ``repository`` stores them.

    Returns the commit, the file list, what was skipped, and the content of every file. The
    files are read from the objects of the commit. Nothing is checked out, so settings of
    this machine such as line ending conversion cannot change a byte. ``commit`` is a full
    commit hash, a branch or a tag, and the newest commit of the default branch when absent.
    """
    if commit and commit.startswith("-"):
        raise ValueError(f"{commit} is not a commit")
    _git(work, "init", "-q")
    _git(work, "remote", "add", "origin", repository_address(repository))
    # The repository is asked for the commit without its files, then for the files of the
    # skill only. A repository that cannot leave files out sends all of them, which is fine.
    _git(work, "config", "remote.origin.promisor", "true")
    _git(work, "config", "remote.origin.partialclonefilter", "blob:none")
    try:
        _git(
            work, "fetch", "-q", "--depth", "1", "--filter=blob:none", "--no-tags",
            "origin", commit or "HEAD",
        )  # fmt: skip
    except ValueError as error:
        if commit and re.fullmatch(r"[0-9a-fA-F]{4,39}", commit):
            raise ValueError(f"{error}. A commit is given by its full hash") from None
        raise
    # A tag can be an object of its own. The commit it points to is what is read.
    sha = _git(work, "rev-parse", "FETCH_HEAD^{commit}").decode("ascii").strip()
    inside = ["--", f"{path}/"] if path else []
    listing = _git(work, "--literal-pathspecs", "ls-tree", "-r", "-z", sha, *inside)

    entries, skipped, control = [], [], set()
    for record in listing.split(b"\0"):
        if not record:
            continue
        head, _, name = record.partition(b"\t")
        mode, kind, oid = head.decode("ascii").split()
        try:
            relative = name.decode("utf-8")[len(path) + 1 if path else 0 :]
        except UnicodeDecodeError:
            raise ValueError(f"a file name in {path or repository} is not valid UTF-8") from None
        if _contains_control_character(relative):
            raise ValueError(f"a file name in {path or repository} contains a control character")
        parts = relative.split("/")
        hidden = next((i for i, part in enumerate(parts) if part.lower() in VERSION_CONTROL), None)
        if hidden is not None:
            # git never checks out a folder of this name, but a crafted commit can hold one.
            # It is version control data, as in a folder on this machine, and is not read.
            control.add("/".join(parts[: hidden + 1]))
            continue
        if kind == "commit":
            raise ValueError(
                f"{relative} is a submodule, and its files are not part of the commit. "
                "A skill with a submodule cannot be read yet"
            )
        if kind == "blob":
            file_type = "symbolic link" if mode == "120000" else "regular"
            entries.append((relative, oid, mode == "100755", file_type))
    skipped += [{"path": folder, "reason": "version control data"} for folder in control]

    oids = "".join(f"{oid}\n" for _, oid, _, _ in entries).encode("ascii")
    if oids:
        try:
            # One request for all files of the skill.
            _git(
                work, "-c", "fetch.negotiationAlgorithm=noop", "fetch", "-q", "origin",
                "--no-tags", "--no-write-fetch-head", "--recurse-submodules=no",
                "--filter=blob:none", "--stdin", stdin=oids,
            )  # fmt: skip
        except ValueError:
            pass  # git then asks for each missing file on its own when it is read below
    stream = _git(work, "cat-file", "--batch", stdin=oids) if oids else b""

    files, contents, position = [], {}, 0
    for relative, oid, executable, file_type in entries:
        end = stream.index(b"\n", position)
        header = stream[position:end].decode("ascii").split()
        if len(header) != 3 or header[0] != oid or header[1] != "blob":
            raise ValueError(f"{relative} could not be read from the commit")
        size = int(header[2])
        data = stream[end + 1 : end + 1 + size]
        position = end + 1 + size + 1
        files.append(file_entry(relative, data, executable, file_type))
        if file_type == "regular":
            contents[relative] = data
    files.sort(key=lambda item: item["path"].encode("utf-8"))
    skipped.sort(key=lambda item: item["path"].encode("utf-8"))
    return sha, files, skipped, contents


# ---------------------------------------------------------------------------------------
# Writing the run folder
# ---------------------------------------------------------------------------------------


def _write_run(out_dir: Path, name: str, snapshot: dict, contents: dict[str, bytes]) -> Path:
    """Write ``snapshot.json`` and ``files/`` into the run folder of this skill version.

    The run folder is named after the skill folder and the first eight characters of the
    hash, so the same files always land in the same place.
    """
    run_dir = Path(out_dir) / f"{name}-{snapshot['hash'].removeprefix('sha256:')[:8]}"
    if run_dir.exists():
        try:
            existing = read_json(run_dir / "snapshot.json")
        except (OSError, ValueError):
            existing = {}
        if existing.get("source_identity") != snapshot.get("source_identity"):
            identity = json.dumps(snapshot.get("source_identity"), sort_keys=True).encode("utf-8")
            suffix = hashlib.sha256(identity).hexdigest()[:8]
            run_dir = run_dir.with_name(f"{run_dir.name}-{suffix}")
    # A commit can hold file names that a checkout would refuse, such as ``..``. Nothing is
    # written unless every file lands inside the run folder.
    frozen = (run_dir / "files").resolve()
    paths = set(contents) | {item["path"] for item in snapshot.get("files", [])}
    for path in paths:
        target = (frozen / path).resolve()
        if target == frozen or not target.is_relative_to(frozen):
            raise ValueError(f"the file name {path!r} would be written outside the run folder")
        if any(part.lower() in VERSION_CONTROL for part in target.relative_to(frozen).parts):
            raise ValueError(f"the file name {path!r} would be written as version control data")
    if run_dir.exists():
        if not (run_dir / "snapshot.json").is_file():
            raise ValueError(f"{run_dir} exists and is not a run folder")
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    write_json(run_dir / "snapshot.json", snapshot)
    for path, data in contents.items():
        target = run_dir / "files" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return run_dir


def _snapshot(
    name: str, place: str, source: dict, files: list[dict], skipped: list[dict], skill_md: bytes
) -> dict:
    """Return the identity of one skill version as it is written to ``snapshot.json``."""
    frontmatter = read_frontmatter(skill_md.decode("utf-8", "replace"))
    exclusions = [
        {
            "path": item["path"],
            "reason": item.get("exclusion_reason", "not included in hash"),
            "sha256": item.get("sha256", "none"),
        }
        for item in files
        if not item["in_hash"]
    ] + [{"path": item["path"], "reason": item["reason"], "sha256": "none"} for item in skipped]
    exclusions.sort(key=lambda item: (item["path"].encode("utf-8"), item["reason"]))
    source_repo = normalize_repository(source.get("repository"))
    identity = (
        {"repository": source_repo, "path": source.get("path", "")}
        if source_repo and source.get("kind") == "repository"
        else None
    )
    return {
        "skill": name,
        "skill_id": place,
        "source_identity": identity,
        "original_skill_name": quoted(frontmatter.get("name")),
        "hash": content_hash(files),
        "hash_scheme": HASH_SCHEME,
        "source": source,
        "files": files,
        "skipped": skipped,
        "exclusions": exclusions,
    }


def _known(snapshot: dict, cards_dir: Path | None, stop_if_known: bool, out_dir: Path) -> dict:
    """Compare cards, record the observation, and stop when the planned action is SKIP."""
    known = compare_with_cards(snapshot, cards_dir)
    index = IdentityIndex(Path(out_dir) / "identity-index.json")
    decision = index.decide(snapshot, cards_dir, allow_skip=stop_if_known)
    # The comparison remains useful for anonymous local folders and for callers that supply
    # their own card comparison. A card-level exact match is enough to record a skip.
    if stop_if_known and known[ALREADY]:
        decision = {
            "action": "SKIP",
            "reason": "a card records this same source and compatible content",
            "reuse_card": None,
            "existing_card": known[ALREADY][0],
        }
    if (
        known["file_comparisons"]
        and decision["action"] == "FULL_ANALYSIS"
        and any(
            comparison["changed"] or comparison["only_current"] or comparison["only_card"]
            for comparison in known["file_comparisons"]
        )
    ):
        decision["reason"] = "partial file matches are diagnostic only; full analysis is required"
    snapshot["identity_action"] = decision["action"]
    snapshot["identity_reason"] = decision["reason"]
    snapshot["identity_handoff"] = {
        "action": decision["action"],
        "content_identity": {
            "hash_scheme": snapshot["hash_scheme"],
            "hash": snapshot["hash"],
        },
        "reuse_card": decision.get("reuse_card"),
        "source_identity": snapshot.get("source_identity"),
        "source": snapshot["source"],
        "index": "identity-index.json",
    }
    indexed_comparisons = index.file_comparisons(snapshot)
    known["file_comparisons"] = _merge_file_comparisons(
        known["file_comparisons"], indexed_comparisons
    )
    if indexed_comparisons and decision["action"] == "FULL_ANALYSIS":
        decision["reason"] = "partial file matches are diagnostic only; full analysis is required"
        snapshot["identity_reason"] = decision["reason"]
        snapshot["identity_handoff"]["action_reason"] = decision["reason"]
    known["action_reason"] = decision["reason"]
    snapshot["identity_handoff"]["action_reason"] = decision["reason"]
    known["action"] = decision["action"]
    known["action_reason"] = decision["reason"]
    known["reuse_card"] = decision.get("reuse_card")
    snapshot["known"] = known
    index.observe(snapshot, decision)
    if stop_if_known and decision["action"] == "SKIP":
        card = decision.get("existing_card")
        raise AlreadyKnown([Path(card).name if card else "identity-index.json"])
    return known


def _merge_file_comparisons(*groups: list[dict]) -> list[dict]:
    """Keep one copy of each per-file comparison when cards and the index overlap."""
    merged, seen = [], set()
    for group in groups:
        for comparison in group:
            signature = (
                comparison.get("card"),
                tuple(comparison.get("same", [])),
                tuple(tuple(sorted(item.items())) for item in comparison.get("changed", [])),
                tuple(comparison.get("only_current", [])),
                tuple(comparison.get("only_card", [])),
            )
            if signature not in seen:
                seen.add(signature)
                merged.append(comparison)
    return merged


def identify(
    skill_dir: Path,
    out_dir: Path,
    leave_out: tuple[str, ...] = (),
    cards_dir: Path | None = None,
    stop_if_known: bool = False,
) -> Path:
    """Freeze one skill folder on this machine and return the run folder created for it.

    ``leave_out`` names documents about the skill that are stored next to it, for example a
    card that a registry generated. They are copied and listed but are not part of the hash.
    The snapshot records the folder name as the location and not the full path on the
    machine. A local folder has no place that others can reach, so its ``skill_id`` is none.

    With ``stop_if_known``, ``AlreadyKnown`` is raised when this version of the skill already
    has a card in ``cards_dir``. Nothing is written then, and an earlier run folder stays.
    """
    skill_dir = Path(skill_dir).resolve()
    if Path(out_dir).resolve().is_relative_to(skill_dir):
        raise ValueError("the output folder is inside the skill folder, choose another with --out")
    files, skipped = list_files(skill_dir)
    paths = {item["path"] for item in files if item["file_type"] == "regular"}
    if "SKILL.md" not in paths:
        raise ValueError(f"{skill_dir.name} is not a skill folder, it has no SKILL.md")
    if missing := sorted(set(leave_out) - paths):
        raise ValueError(f"cannot leave out files that are not in the folder, {missing}")
    for item in files:
        item["in_hash"] = item["path"] not in leave_out
        item["exclusion_reason"] = "explicit --leave-out" if item["path"] in leave_out else "none"
    contents = {
        item["path"]: (skill_dir / item["path"]).read_bytes()
        for item in files
        if item["file_type"] == "regular"
    }
    checkout = _checkout_source(skill_dir)
    source = (
        {
            "kind": "repository",
            "repository": checkout["repository"],
            "path": checkout["path"],
            "commit": checkout["commit"],
            "worktree_changed": checkout["worktree_changed"],
            "retrieved": date.today().isoformat(),
        }
        if checkout
        else {
            "kind": "local path",
            "location": skill_dir.name,
            "retrieved": date.today().isoformat(),
        }
    )
    place = skill_id(source["repository"], source["path"]) if checkout else "none"
    snapshot = _snapshot(skill_dir.name, place, source, files, skipped, contents["SKILL.md"])
    snapshot["known"] = _known(snapshot, cards_dir, stop_if_known, out_dir)
    return _write_run(out_dir, skill_dir.name, snapshot, contents)


def identify_repository(
    repository: str,
    path: str,
    out_dir: Path,
    commit: str | None = None,
    cards_dir: Path | None = None,
    stop_if_known: bool = False,
) -> Path:
    """Freeze the skill at ``path`` in ``repository`` and return the run folder created for it.

    ``repository`` is the address of a git repository, a folder on this machine that holds
    one, or ``owner/repo`` for a repository on GitHub. ``path`` is the folder inside it that
    holds the skill's SKILL.md. Every file the commit holds under that folder is part of the
    skill and of the hash. ``stop_if_known`` works as in ``identify``.
    """
    path = posixpath.normpath(path).strip("/")
    path = "" if path == "." else path
    if path == ".." or path.startswith("../"):
        raise ValueError("the path of the skill lies outside the repository")
    address = repository_address(repository)
    with tempfile.TemporaryDirectory(prefix="skillcard-") as work:
        sha, files, skipped, contents = read_commit(repository, path, commit, Path(work))
    name = repository_name(address)
    folder = path.rsplit("/", 1)[-1] if path else Path(name or address).name
    if "SKILL.md" not in contents:
        raise ValueError(f"{path or folder} is not a skill folder, it has no SKILL.md")
    identity_address = address
    if Path(address).is_dir():
        try:
            origin = (
                _git(Path(address), "remote", "get-url", "origin")
                .decode("utf-8", "replace")
                .strip()
            )
            if origin:
                identity_address = repository_address(origin)
        except ValueError:
            pass
    identity_url = _identity_url(identity_address)
    source = {
        "kind": "repository",
        "repository": identity_url or (f"https://{name}" if name else Path(address).name),
        "path": path,
        "commit": sha,
        "retrieved": date.today().isoformat(),
    }
    place = skill_id(identity_address, path)
    snapshot = _snapshot(folder, place, source, files, skipped, contents["SKILL.md"])
    snapshot["known"] = _known(snapshot, cards_dir, stop_if_known, out_dir)
    return _write_run(out_dir, folder, snapshot, contents)
