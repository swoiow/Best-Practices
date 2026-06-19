# PYTHON-PRO-GUIDE.md

## 1. Scope

This guide applies to Python repositories, scripts, libraries, data-processing jobs, and agent-oriented Python code.

The goal is to keep Python code clear, explicit, maintainable, testable, and easy to change. Prefer simple structures that fit the current repository over speculative abstractions.

Priority order:

1. User request and repository-specific instructions.
2. Existing local conventions in nearby files.
3. Project formatter, linter, type checker, and test conventions.
4. This guide.

Do not apply style rules mechanically when they reduce readability. Consistency inside the current project, module, or function matters more than theoretical purity.

## 2. Agent Change Discipline

Before changing code:

* Read surrounding files first.
* Preserve current behavior unless the requested change requires otherwise.
* Make the smallest clean change that solves the problem.
* Avoid unrelated refactors.
* Do not add dependencies unless clearly necessary.
* Keep public APIs stable unless changing them is part of the task.

After modifying code, summarize only:

* What changed.
* Why it changed.
* Any manual checks the user should run.

## 3. Formatting and Layout

Use the project formatter if one exists.

Defaults:

* Use 4 spaces per indentation level.
* Do not mix tabs and spaces.
* Follow repository line length configuration.
* If no configuration exists, prefer 88 characters for code and 72 characters for long comments or docstrings.
* Use UTF-8 for all new Python source files.
* Use two blank lines between top-level functions/classes.
* Use one blank line between methods inside a class.

```python
# Good
x = 1
y = 2
long_variable = 3

# Bad
x             = 1
y             = 2
long_variable = 3
```

Prefer implicit line continuation:

```python
result = client.create_report(
    account_id=account_id,
    start_date=start_date,
    end_date=end_date,
    include_archived=False,
)
```

## 4. Imports

Order imports in this sequence:

1. Standard library.
2. Third-party packages.
3. Local application imports.

Rules:

* Put imports at the top of the file after module comments and docstring.
* Prefer one import per line.
* Use absolute imports for application packages unless local convention says otherwise.
* Avoid wildcard imports.
* Remove unused imports.
* Prefer `from pathlib import Path`, not `import pathlib`.
* Use `if TYPE_CHECKING:` for imports needed only by type checkers.

```python
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from app.config import Settings
from app.models import Report

if TYPE_CHECKING:
    from app.clients import StorageClient
```

## 5. Whitespace

Avoid visual noise around brackets, calls, commas, colons, and indexing.

```python
# Good
spam(ham[1], {"eggs": 2})
dict_["key"] = items[index]

# Bad
spam( ham[ 1 ], { "eggs": 2 } )
dict_ ["key"] = items [index]
```

Use one space around most binary operators:

```python
count = count + 1
is_valid = status == "ready" and retry_count < max_retries
```

Do not put spaces around `=` for keyword arguments or default values:

```python
def create_user(name: str, is_active: bool = True) -> User:
    return User(name=name, is_active=is_active)
```

Do not put multiple statements on one line.

## 6. Naming

Use precise English names.

* Packages/modules: short lowercase names; underscores are acceptable when they improve readability.
* Classes/exceptions: `CapWords`.
* Functions/methods/variables: `snake_case`.
* Constants: `UPPER_SNAKE_CASE`.
* Internal names: prefix with a single underscore.
* Magic names: use existing double-underscore names only for Python protocols.
* Avoid single-character names except in very small scopes.
* Never use `l`, `O`, or `I` as single-character variable names.

```python
MAX_RETRIES = 3


def fetch_user_profile(user_id: str) -> UserProfile:
    ...


class PaymentError(Exception):
    """Raised when payment processing fails."""
```

## 7. Type Hints

Use type annotations for public functions, public methods, and non-trivial internal functions.

Guidelines:

* Prefer `list[str]`, `dict[str, int]`, `tuple[str, ...]`.
* Use `collections.abc` for `Mapping`, `Sequence`, `Iterable`, `Callable`.
* Use `Path` for filesystem paths.
* Use `str | None` instead of `Optional[str]` unless the repository uses older style.
* Use aliases for repeated complex types.
* Use `from __future__ import annotations` in new modules when helpful.

```python
from collections.abc import Mapping, Sequence
from pathlib import Path

Row = Mapping[str, str | int | float | None]


def write_rows(rows: Sequence[Row], output_path: Path) -> None:
    ...
```

## 8. Docstrings and Comments

Use Google-style docstrings for public modules, classes, functions, and methods.

Rules:

* Comments explain intent, constraints, tradeoffs, and non-obvious behavior.
* Do not restate code line by line.
* Keep comments current when behavior changes.
* Inline comments should be used sparingly.

```python
def normalize_email(email: str) -> str:
    """Normalize an email address for identity matching.

    Args:
        email: Raw email address from user input.

    Returns:
        Lowercase, stripped email address.

    Raises:
        ValueError: If the email address is empty.
    """
    normalized = email.strip().lower()
    if not normalized:
        raise ValueError("email must not be empty")
    return normalized
```

## 9. Error Handling

Handle errors explicitly.

* Raise specific exceptions.
* Do not silently swallow errors.
* Use `try/except` only when adding context, retry behavior, cleanup, or translation.
* Re-raise exceptions when the caller should decide what to do.
* Log useful context.
* Avoid broad `except Exception` unless it is at a boundary and intentional.

```python
class ConfigError(Exception):
    """Raised when runtime configuration is invalid."""


def load_required_env(name: str, env: Mapping[str, str]) -> str:
    try:
        value = env[name]
    except KeyError as exc:
        raise ConfigError(f"Missing required environment variable: {name}") from exc

    if not value:
        raise ConfigError(f"Environment variable must not be empty: {name}")
    return value
```

## 10. Logging

Use `logging` instead of `print`, except for intentional user-facing CLI output.

```python
LOGGER.info("Imported %s rows from %s", row_count, input_path)
LOGGER.warning("Retrying request url=%s attempt=%s", url, attempt)
```

Do not log secrets, tokens, passwords, private keys, or raw credentials.

## 11. Filesystem and Data Operations

Use `pathlib.Path`.

* Use explicit encoding for text files.
* Avoid hardcoded absolute paths.
* Keep input paths, output paths, and runtime configuration explicit.
* Prefer atomic writes when overwriting important files.
* Validate schemas and required columns near data boundaries.
* Avoid loading large files fully into memory unless the size is known and acceptable.

```python
content = path.read_text(encoding="utf-8")
path.write_text(content, encoding="utf-8")
```

## 12. Dependencies

Do not add dependencies casually.

Recommended defaults:

* Standard library first.
* `argparse` for simple CLIs.
* `dataclasses` for lightweight typed configuration.
* `pydantic` when runtime validation is valuable.
* `pytest` for most test suites.
* Standard `logging` for observability.

Always set explicit timeouts for external network calls.

```python
with httpx.Client(timeout=10.0) as client:
    response = client.get(url)
    response.raise_for_status()
```

## 13. Async and Concurrency

Use async or threaded execution only when it improves correctness, throughput, responsiveness, or integration with existing APIs.

Async rules:

* Do not block the event loop.
* Do not call `time.sleep()` in async code.
* Use `asyncio.sleep()` in async code.
* Keep async boundaries explicit.
* Do not create or manage event loops inside sync wrappers.
* Avoid shared mutable state unless protected.

## 14. Pythonic Recommendations

Compare to `None` with identity:

```python
if value is None:
    ...

if value is not None:
    ...
```

Use truthiness for sequences:

```python
if not items:
    return []
```

Do not compare booleans to `True` or `False`:

```python
if is_enabled:
    start()
```

Use `isinstance` for type checks:

```python
if isinstance(value, int):
    ...
```

Use string methods for prefix and suffix checks:

```python
if filename.endswith(".json"):
    ...

if key.startswith("user:"):
    ...
```

## 15. Testing and Review Checklist

Before finalizing a change, verify:

* The change directly addresses the requested task.
* No unrelated refactor was introduced.
* Imports are clean.
* Formatting follows the local formatter.
* Type hints are present where useful.
* Public functions have clear docstrings.
* Comments explain intent rather than restating code.
* Exceptions are specific and not silently swallowed.
* Logging uses lazy formatting.
* Paths use `Path`.
* Text file operations specify encoding.
* Async code does not block the event loop.
* Network calls have explicit timeouts.
* New dependencies were avoided unless justified.
* Manual checks are listed when they cannot be run directly.
