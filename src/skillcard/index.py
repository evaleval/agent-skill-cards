"""Persistent source and content identity history for skill-card runs."""

from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from skillcard import read_json, write_json

INDEX_FORMAT = "skillcard-identity-index-v1"
ACTIONS = {"SKIP", "FULL_ANALYSIS", "SOURCE_ONLY"}


def _normal_path(path: object) -> str:
    if not isinstance(path, str) or path in ("", "."):
        return "."
    return "/".join(part for part in path.replace("\\", "/").split("/") if part and part != ".")


def normalize_repository(repository: object) -> str | None:
    """Return a credential-free canonical repository URL, or None for a local-only source."""
    if not isinstance(repository, str) or not repository or repository == "none":
        return None
    candidate = repository.strip()
    if re.match(r"^[A-Za-z]:[\\/]", candidate) or candidate.startswith(("/", "\\")):
        return None
    explicit_url = "://" in candidate
    if Path(candidate).exists():
        return None
    if not explicit_url:
        candidate = "https://" + candidate
    parsed = urlsplit(candidate)
    if not parsed.hostname:
        return None
    if not explicit_url and "." not in parsed.hostname and parsed.hostname != "localhost":
        return None
    host = parsed.hostname.lower()
    try:
        port_number = parsed.port
    except ValueError:
        return None
    port = f":{port_number}" if port_number else ""
    path = parsed.path.rstrip("/").removesuffix(".git")
    return urlunsplit((parsed.scheme.lower() or "https", host + port, path, "", ""))


def source_identity(snapshot: dict) -> str | None:
    """Return the stable repository URL plus skill path key, if the source is identifiable."""
    identity = snapshot.get("source_identity")
    if isinstance(identity, dict):
        repository, path = identity.get("repository"), identity.get("path")
    else:
        source = snapshot.get("source", {})
        repository, path = source.get("repository"), source.get("path")
    repository = normalize_repository(repository)
    if repository is None:
        return None
    return f"{repository.lower()}#{_normal_path(path)}"


def source_identity_from_card(card: dict) -> str | None:
    """Read a source key from explicit fields or the card's established location text."""
    which = card.get("which_files", {})
    source = which.get("source", {})
    repository, path = source.get("repository"), source.get("path")
    if not repository or repository == "none":
        location = source.get("location", "")
        match = re.fullmatch(r"GitHub ([^/\s]+/[^/\s,]+), path (.+)", location)
        if match:
            repository, path = f"https://github.com/{match.group(1)}", match.group(2)
        else:
            match = re.fullmatch(r"([^/\s]+/.+), path (.+)", location)
            if match:
                repository, path = f"https://{match.group(1)}", match.group(2)
    return source_identity({"source_identity": {"repository": repository, "path": path}})


def content_identity(record: dict) -> str:
    scheme = record.get("hash_scheme") or "skill-tree-v1"
    return f"{scheme}:{record.get('hash', '')}"


def _exclusions(record: dict) -> tuple[tuple[str, str, str], ...]:
    explicit = record.get("exclusions")
    if isinstance(explicit, list):
        values = explicit
    else:
        values = [
            {
                "path": one.get("path"),
                "reason": one.get("exclusion_reason", "not recorded"),
                "sha256": one.get("sha256", "none"),
            }
            for one in record.get("files", [])
            if isinstance(one, dict) and not one.get("in_hash", True)
        ]
    return tuple(
        sorted(
            (
                str(one.get("path", "")),
                str(one.get("reason", "not recorded")),
                str(one.get("sha256", "none")),
            )
            for one in values
            if isinstance(one, dict)
        )
    )


def compatible_content(one: dict, other: dict) -> bool:
    """Say whether two records can safely share content analysis."""
    one_scheme = one.get("hash_scheme") or "skill-tree-v1"
    other_scheme = other.get("hash_scheme") or "skill-tree-v1"
    if one_scheme not in {"skill-tree-v1", "skill-tree-v2"} or one_scheme != other_scheme:
        return False
    if _exclusions(one) != _exclusions(other):
        return False
    return one.get("hash") == other.get("hash")


def _compare_manifests(current: dict, previous: dict, reference: str) -> dict:
    """Compare file records individually and retain additions, removals and changed files."""
    left = {
        one["path"]: one
        for one in current.get("files", [])
        if isinstance(one, dict) and isinstance(one.get("path"), str)
    }
    right = {
        one["path"]: one
        for one in previous.get("files", [])
        if isinstance(one, dict) and isinstance(one.get("path"), str)
    }
    common = sorted(left.keys() & right.keys())
    same, changed = [], []
    for path in common:
        one, other = left[path], right[path]
        one_type = one.get("file_type", "regular")
        other_type = other.get("file_type", "regular")
        if one.get("sha256") == other.get("sha256") and one_type == other_type:
            same.append(path)
        else:
            changed.append(
                {
                    "path": path,
                    "current_sha256": one.get("sha256"),
                    "card_sha256": other.get("sha256"),
                    "current_type": one_type,
                    "card_type": other_type,
                }
            )
    return {
        "card": reference,
        "same": same,
        "changed": changed,
        "only_current": sorted(left.keys() - right.keys()),
        "only_card": sorted(right.keys() - left.keys()),
    }


def _card_record(card: dict) -> dict:
    which = card.get("which_files") or {}
    version = which.get("version") or {}
    return {
        "hash": version.get("hash"),
        "hash_scheme": version.get("hash_scheme", "skill-tree-v1"),
        "exclusions": version.get("exclusions"),
        "files": which.get("files", []),
    }


def _empty() -> dict:
    return {"format": INDEX_FORMAT, "sources": {}, "contents": {}, "observations": []}


class IdentityIndex:
    """A JSON index that tracks observations, source versions and reusable content analysis."""

    def __init__(self, path: Path):
        self.path = Path(path)
        if self.path.exists():
            self.data = read_json(self.path)
            if self.data.get("format") != INDEX_FORMAT:
                raise ValueError(f"{self.path} is not a supported skill-card identity index")
        else:
            self.data = _empty()

    def _relative(self, target: Path) -> str:
        return Path(os.path.relpath(target.resolve(), self.path.parent.resolve())).as_posix()

    def _resolve(self, reference: str) -> Path:
        target = (self.path.parent / reference).resolve()
        if not target.is_file():
            return target
        return target

    def _content_entry(self, snapshot: dict) -> dict | None:
        entries = self.data["contents"].get(content_identity(snapshot), [])
        for entry in entries:
            if compatible_content(snapshot, entry["record"]):
                references = entry.get("analysis_cards") or [entry.get("analysis_card")]
                for reference in reversed([one for one in references if one]):
                    card = self._resolve(reference)
                    if not card.is_file():
                        continue
                    try:
                        if compatible_content(snapshot, _card_record(read_json(card))):
                            return entry
                    except (OSError, ValueError, KeyError, TypeError, AttributeError):
                        continue
        return None

    def _remember_analysis_card(
        self, snapshot: dict, reference: str, bind_to_source: bool = True
    ) -> bool:
        """Index a readable, compatible card reference for this content and source version."""
        card_path = self._resolve(reference)
        if not card_path.is_file():
            return False
        try:
            if not compatible_content(snapshot, _card_record(read_json(card_path))):
                return False
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            return False

        content_key = content_identity(snapshot)
        record = {
            "hash": snapshot["hash"],
            "hash_scheme": snapshot.get("hash_scheme", "skill-tree-v1"),
            "exclusions": snapshot.get("exclusions", []),
            "files": snapshot.get("files", []),
        }
        analyses = self.data["contents"].setdefault(content_key, [])
        entry = next((one for one in analyses if compatible_content(record, one["record"])), None)
        if entry is None:
            entry = {
                "record": record,
                "first_seen": date.today().isoformat(),
                "analysis_cards": [],
            }
            analyses.append(entry)
        entry["last_seen"] = date.today().isoformat()
        references = entry.setdefault("analysis_cards", [])
        if entry.get("analysis_card") and entry["analysis_card"] not in references:
            references.append(entry["analysis_card"])
        if reference not in references:
            references.append(reference)

        key = source_identity(snapshot)
        if key and bind_to_source:
            for version in self.data["sources"].get(key, {}).get("versions", []):
                if version["content_identity"] == content_key and compatible_content(
                    record, version["record"]
                ):
                    version["analysis_card"] = reference
        return True

    def _card_candidates(self, snapshot: dict, cards_dir: Path | None) -> list[tuple[Path, dict]]:
        if cards_dir is None or not Path(cards_dir).is_dir():
            return []
        matches = []
        for path in sorted(Path(cards_dir).glob("*.json")):
            try:
                card = read_json(path)
                if compatible_content(snapshot, _card_record(card)):
                    matches.append((path, card))
            except (OSError, ValueError, KeyError, TypeError, AttributeError):
                continue
        return matches

    def _source_has_versions(self, key: str | None) -> bool:
        return bool(key and self.data["sources"].get(key, {}).get("versions"))

    def decide(self, snapshot: dict, cards_dir: Path | None, allow_skip: bool) -> dict:
        """Choose one of the three pipeline actions and identify a reusable card when possible."""
        key = source_identity(snapshot)
        content_key = content_identity(snapshot)
        source = self.data["sources"].get(key, {}) if key else {}
        prior = source.get("versions", [])
        exact_prior = next(
            (
                version
                for version in prior
                if compatible_content(snapshot, version["record"])
                and version.get("content_identity") == content_key
                and version.get("analysis_card")
                and self._resolve(version["analysis_card"]).is_file()
            ),
            None,
        )
        same_source_card = None
        candidates = self._card_candidates(snapshot, cards_dir)
        if key:
            for path, card in candidates:
                if source_identity_from_card(card) == key:
                    same_source_card = path
                    break
        if exact_prior or same_source_card:
            return {
                "action": "SKIP" if allow_skip else "FULL_ANALYSIS",
                "reason": "same source and compatible content version already has a card",
                "reuse_card": None,
                "existing_card": (
                    exact_prior["analysis_card"]
                    if exact_prior
                    else self._relative(same_source_card)
                ),
            }

        # A new content version at an already observed source is a full analysis. Its previous
        # versions remain in the index even when another source happens to have similar files.
        if self._source_has_versions(key):
            return {
                "action": "FULL_ANALYSIS",
                "reason": "new content version at a previously observed source",
                "reuse_card": None,
            }

        if not key:
            return {
                "action": "FULL_ANALYSIS",
                "reason": "source identity is unavailable, so shared content cannot be attributed",
                "reuse_card": None,
            }

        content = self._content_entry(snapshot)
        if content:
            references = content.get("analysis_cards") or [content.get("analysis_card")]
            return {
                "action": "SOURCE_ONLY",
                "reason": "compatible content analysis exists at another source",
                "reuse_card": next(one for one in reversed(references) if one),
            }
        if candidates:
            return {
                "action": "SOURCE_ONLY",
                "reason": "compatible content analysis exists in the cards directory",
                "reuse_card": self._relative(candidates[0][0]),
            }
        return {
            "action": "FULL_ANALYSIS",
            "reason": "no compatible content analysis exists",
            "reuse_card": None,
        }

    def file_comparisons(self, snapshot: dict) -> list[dict]:
        """Compare the current manifest with every earlier source version and analysis."""
        comparisons = []
        seen = set()
        previous_records = []
        for content_key, entries in sorted(self.data["contents"].items()):
            for entry in entries:
                record = entry.get("record", {})
                references = entry.get("analysis_cards") or [entry.get("analysis_card")]
                references = [reference for reference in references if reference]
                reference = references[-1] if references else content_key
                previous_records.append((reference, record))
        for source_key, source in sorted(self.data["sources"].items()):
            for version in source.get("versions", []):
                record = version.get("record", {})
                reference = version.get("analysis_card") or version.get("content_identity")
                reference = reference or f"{source_key}#unknown-version"
                previous_records.append((reference, record))

        for reference, record in previous_records:
            if compatible_content(snapshot, record):
                continue
            comparison = _compare_manifests(snapshot, record, reference)
            # Disjoint manifests are not a partial match. A shared path with either the same
            # or changed content is the evidence that makes this comparison useful.
            if not comparison["same"] and not comparison["changed"]:
                continue
            signature = (
                reference,
                tuple(comparison["same"]),
                tuple(tuple(sorted(item.items())) for item in comparison["changed"]),
                tuple(comparison["only_current"]),
                tuple(comparison["only_card"]),
            )
            if signature not in seen:
                seen.add(signature)
                comparisons.append(comparison)
        return comparisons

    def observe(self, snapshot: dict, decision: dict) -> None:
        """Record one input observation and append it to the source's version history."""
        action = decision["action"]
        if action not in ACTIONS:
            raise ValueError(f"unknown identity action {action!r}")
        observed = date.today().isoformat()
        key = source_identity(snapshot)
        content_key = content_identity(snapshot)
        version_record = {
            "content_identity": content_key,
            "hash_scheme": snapshot.get("hash_scheme", "skill-tree-v1"),
            "hash": snapshot["hash"],
            "record": {
                "hash": snapshot["hash"],
                "hash_scheme": snapshot.get("hash_scheme", "skill-tree-v1"),
                "exclusions": snapshot.get("exclusions", []),
                "files": snapshot.get("files", []),
            },
            "first_observed": observed,
            "last_observed": observed,
            "commits": [],
            "observations": 0,
            "analysis_card": None,
        }
        if commit := snapshot.get("source", {}).get("commit"):
            version_record["commits"].append(commit)
        if key:
            source = self.data["sources"].setdefault(
                key,
                {
                    "repository": snapshot["source_identity"]["repository"],
                    "path": snapshot["source_identity"]["path"],
                    "versions": [],
                },
            )
            existing = next(
                (
                    one
                    for one in source["versions"]
                    if one["content_identity"] == content_key
                    and compatible_content(snapshot, one["record"])
                ),
                None,
            )
            if existing is None:
                source["versions"].append(version_record)
                existing = source["versions"][-1]
            existing["last_observed"] = observed
            existing["observations"] = existing.get("observations", 0) + 1
            if commit and commit not in existing["commits"]:
                existing["commits"].append(commit)
        event = {
            "observed": observed,
            "source_identity": key,
            "content_identity": content_key,
            "action": action,
            "reason": decision["reason"],
            "commit": snapshot.get("source", {}).get("commit", "none"),
            "reuse_card": decision.get("reuse_card"),
            "existing_card": decision.get("existing_card"),
            "source": snapshot.get("source", {}),
            "file_comparisons": snapshot.get("known", {}).get("file_comparisons", []),
        }
        if decision.get("existing_card"):
            self._remember_analysis_card(snapshot, decision["existing_card"])
        elif decision.get("reuse_card"):
            self._remember_analysis_card(snapshot, decision["reuse_card"], bind_to_source=False)
        self.data["observations"].append(event)
        self.save()

    def analysis_card_for(self, snapshot: dict) -> Path | None:
        """Resolve the source card selected by the most recent matching source-only plan."""
        key, content_key = source_identity(snapshot), content_identity(snapshot)
        for event in reversed(self.data["observations"]):
            if (
                event.get("source_identity") == key
                and event.get("content_identity") == content_key
                and event.get("action") == "SOURCE_ONLY"
                and event.get("reuse_card")
            ):
                target = self._resolve(event["reuse_card"])
                return target if target.is_file() else None
        return None

    def card_references_for(self, snapshot: dict) -> list[Path]:
        """Return all readable cards recorded for a compatible content identity."""
        references: list[str] = []
        entry = self._content_entry(snapshot)
        if entry:
            references.extend(entry.get("analysis_cards", []))
            if entry.get("analysis_card"):
                references.append(entry["analysis_card"])
        key, content_key = source_identity(snapshot), content_identity(snapshot)
        for event in reversed(self.data["observations"]):
            if (
                event.get("source_identity") == key
                and event.get("content_identity") == content_key
                and event.get("reuse_card")
            ):
                references.append(event["reuse_card"])
                break
        cards = []
        for reference in references:
            path = self._resolve(reference)
            if path.is_file() and path not in cards:
                try:
                    if compatible_content(snapshot, _card_record(read_json(path))):
                        cards.append(path)
                except (OSError, ValueError, KeyError, TypeError, AttributeError):
                    continue
        return cards

    def complete(self, snapshot: dict, run_dir: Path) -> None:
        """Record a successfully validated card as a reusable analysis for this content."""
        card = run_dir / "card.json"
        reference = self._relative(card)
        if not self._remember_analysis_card(snapshot, reference):
            raise ValueError(f"{card} does not match the identified content")
        self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        write_json(self.path, self.data)


def card_content_record(card: dict) -> dict:
    """Public adapter used by identification and composition for a card's content identity."""
    return _card_record(card)
