# AGENTS.md

## 1. Scope

This guide applies to Python repositories, scripts, libraries, data-processing jobs, and agent-oriented Python code.

Keep the code clear, explicit, maintainable, and easy to change. Prefer simple structures that match the current repository over speculative abstractions.

When working in an existing repository, follow the local style first. Use this guide to fill gaps where the repository has no stronger convention.

## 2. Response Style

When summarizing changes, be brief and precise.

After modifying code, summarize only:

- What changed
- Why it changed
- Any manual checks the user should run

Avoid long explanations unless the user asks for them.

## 3. Change Discipline

Before changing code:

- Read the surrounding files and understand the existing structure.
- Preserve current behavior unless the requested change requires otherwise.
- Make the smallest clean change that solves the problem.
- Avoid unrelated refactors.
- Do not add new dependencies unless clearly necessary.
- Keep public APIs stable unless changing them is part of the task.
- Prefer direct, end-state fixes when the root cause and target design are clear.

During small fixes, use targeted edits instead of broad rewrites.

## 4. Repository Structure

Prefer a predictable Python layout.

Guidelines:

- Keep source code separate from tests, generated files, and temporary files.
- Place tests in a mirrored `tests/` tree when the repository already follows that style.
- Keep scripts in `scripts/` unless the repository already has another convention.
- Keep configuration examples documented and avoid committing secrets.
- Do not create broad utility modules unless there is a clear repeated use case.
- Prefer clearly named package modules over ambiguous catch-all files.
- Keep repository-level documentation close to the behavior it describes.

## 5. Code Organization

Organize code around explicit responsibilities.

- Encapsulate complex logic in functions or classes.
- Keep modules small enough to understand without jumping across many files.
- Prefer composition over deep inheritance.
- Prefer explicit dependency passing over hidden module-level state.
- Avoid circular imports.
- Avoid large catch-all classes or files.
- Avoid premature extension points.
- Move business logic out of entrypoint files.
- Keep entrypoints focused on parsing configuration, initializing dependencies, and starting execution.

For standalone scripts:

- Do not introduce a CLI framework unless requested or already used by the project.
- Define configuration constants near the top of the file.
- Use `if __name__ == "__main__":` for executable examples or script execution.
- Keep reusable logic outside the `__main__` block.

## 6. Python Coding Style

Use Google Style Python unless the repository has a stronger local convention.

Required preferences:

- Use double quotes for strings.
- Use `from pathlib import Path`, not `import pathlib`.
- Prefer f-strings for normal string formatting.
- Use `logging` instead of `print`, except for intentional user-facing CLI output.
- Use clear names instead of clever abbreviations.
- Keep functions focused.
- Keep imports organized and remove unused imports.
- Prefer standard library features before adding external packages.
- Prefer lazy logging formatting over f-strings inside logging calls.

## 7. Type Hints

Use type annotations for public functions, public methods, and non-trivial internal functions.

Guidelines:

- Prefer built-in generic types such as `list[str]`, `dict[str, int]`, and `tuple[str, ...]`.
- Use `collections.abc` for abstract interfaces such as `Mapping`, `Sequence`, `Iterable`, and `Callable`.
- Use `Path` for filesystem paths where practical.
- Use `str | None` instead of `Optional[str]` unless the repository uses older style.
- Use explicit aliases for repeated complex types.
- Quote forward references when needed.
- Use `from __future__ import annotations` in new modules when it simplifies annotations.
- Avoid unnecessary runtime imports used only for typing; prefer `if TYPE_CHECKING:` where appropriate.

## 8. Docstrings and Comments

Use clear Google-style docstrings for public functions, classes, and methods.

Language preference:

- Class names and function names should be English.
- Comments may use Chinese when that improves local readability.
- Function purpose may be described in Chinese if the repository uses Chinese comments.
- Parameter and return descriptions should be English.
- Comment intent, constraints, and non-obvious decisions.
- Do not restate code line by line.
- Keep comments current when behavior changes.

## 9. Naming Semantics

Use precise English names.

Guidelines:

- Use nouns for role-like objects.
- Use verbs for actions and workflow stages.
- Use output-key names only for actual output data.
- Do not reuse the same name for different semantic layers.
- Centralize repeated string constants in a clearly scoped module.
- Prefer context-scoped names over falsely generic names.
- When renaming a contract, update the central definition first, then update callers.
- Avoid scattering string literals across unrelated files.

## 10. Error Handling

Handle errors explicitly.

Guidelines:

- Raise specific exceptions.
- Do not silently swallow errors.
- Use `try/except` only when adding useful handling, context, retry behavior, cleanup, or translation.
- Re-raise exceptions when the caller should decide what to do.
- Log useful context, not just the exception message.
- Avoid broad `except Exception` unless it is at a boundary and re-raises or converts the error intentionally.
- Do not hide failed validations.
- Preserve the original exception where it is useful for debugging.

## 11. Filesystem and Data Operations

Use `pathlib.Path` for paths.

Guidelines:

- Use `Path.exists()`, `Path.is_file()`, and `Path.is_dir()` for checks.
- Use `Path.mkdir(parents=True, exist_ok=True)` for directory creation.
- Use explicit encoding for text files.
- Avoid hardcoded absolute paths.
- Keep input paths, output paths, and runtime configuration explicit.
- Prefer atomic writes when overwriting important files.
- Keep temporary files and generated outputs outside source directories unless the repository already has a convention.

For data processing:

- Prefer existing repository data libraries.
- For tabular data, use suitable dataframe or query engines when they reduce complexity.
- For database access, prefer explicit connection handling and transaction boundaries.
- Process large datasets in chunks or lazy pipelines when memory pressure matters.
- Avoid loading large files fully into memory unless the size is known and acceptable.
- Validate schemas, required columns, and key assumptions near data boundaries.

## 12. Dependencies

Do not add dependencies casually. Reuse existing dependencies when they are appropriate. Add a new dependency only when it meaningfully improves clarity, correctness, performance, or maintainability.

Choose libraries by scenario.

For general scripting and automation:

- Prefer the Python standard library first.
- Use `argparse` for simple command-line parsing when a CLI is actually needed.
- Use `typer` only when the project benefits from a richer CLI interface.

For filesystem and serialization:

- Use `pathlib` for paths.
- Use `json`, `csv`, `tomllib`, and `configparser` from the standard library when sufficient.
- Use `PyYAML` when YAML support is needed.
- Use `orjson` only when JSON performance is important and the dependency is justified.

For configuration and validation:

- Use `dataclasses` for lightweight typed configuration.
- Use `pydantic` when runtime validation, parsing, and structured error reporting are valuable.
- Use environment variables for deployment-time values, but validate them at clear boundaries.

For data processing:

- Use `pandas` for broad compatibility and common dataframe workflows.
- Use `polars` for fast dataframe processing, lazy execution, or larger datasets.
- Use `pyarrow` for columnar data, Parquet, Arrow interoperability, and efficient data exchange.
- Use `duckdb` for local analytical SQL over files or in-memory data.
- Use `SQLAlchemy` when structured database access and connection management are needed.

For HTTP and network clients:

- Use `requests` for simple synchronous HTTP calls if already present.
- Use `httpx` when both sync and async clients, timeouts, and modern client behavior are useful.
- Use `aiohttp` only when the project already uses it or requires its specific async capabilities.
- Always set explicit timeouts for external network calls.

For async and concurrency:

- Use `asyncio` for native async flows.
- Use `concurrent.futures` for simple thread or process pools.
- Avoid mixing concurrency models without a clear boundary.

For testing:

- Use `pytest` for most test suites.
- Use `unittest` when the repository already uses it or standard-library-only constraints matter.
- Use `pytest-mock` or built-in mocking tools when mocking is necessary.

For logging and observability:

- Use the standard `logging` module by default.

For scheduling and workflows:

- Use cron or simple scheduler mechanisms for small local jobs.

For machine learning:

- Use `scikit-learn` for classical machine learning workflows.
- Use `XGBoost` when gradient-boosted tree models are appropriate.
- Use specialized deep learning libraries only when the task clearly requires them and the repository already supports their operational footprint.

For packaging and project tooling:

- Follow the repository’s existing `pyproject.toml`, lockfile, and package manager conventions.
- Do not introduce a new package manager or build backend without a clear reason.
- Keep optional feature dependencies isolated when practical.

## 13. Async and Concurrency

Use async or threaded execution only when it improves correctness, throughput, responsiveness, or integration with existing async APIs.

Async rules:

- Do not block the event loop.
- Do not call `time.sleep()` in async code.
- Use `asyncio.sleep()` in async code.
- Keep async boundaries explicit.
- Prefer explicit async APIs over hidden sync-to-async conversion.
- Do not create or manage event loops inside sync wrappers.
- Avoid shared mutable state across concurrent tasks unless protected.
- Make cancellation and cleanup behavior clear.

Threading rules:

- Use threads for blocking I/O when async APIs are unavailable.
- Avoid threads for CPU-heavy work unless the workload releases the GIL or uses appropriate executors.
- Keep shared state minimal.
- Use locks or queues when shared state is unavoidable.

## 14. Decorators

Use decorators when they improve clarity, reuse, or correctness.

Good decorator use cases:

- Retry
- Timeout
- Logging
- Validation
- Metrics
- Permission checks
- Sync/async adaptation

Decorator requirements:

- Use `functools.wraps`.
- Use `ParamSpec` and `TypeVar` when preserving function signatures.
- Support both `@decorator` and `@decorator(...)` only when it genuinely improves usability.
- Separate sync and async wrappers.
- Validate decorator configuration early.
- Do not share mutable retry or backoff state across calls.
- Re-raise the final original exception.
- Use `asyncio.sleep()` for async wrappers.
- Use `time.sleep()` only for sync wrappers.
- Do not create or manage event loops inside sync wrappers.

Retry expectations:

- `max_tries` means total attempts.
- `retry_interval=0` means no delay.
- Backoff state must be created per call.
- Final failure must raise the original exception.

## 15. Testing and Debugging

Follow the repository’s testing convention.

General rules:

- Add or update tests when changing behavior.
- Keep tests focused and readable.
- Prefer simple functional tests for scripts.
- Use fixtures for repeated setup.
- Avoid excessive mocking when real lightweight objects are clearer.
- Do not run large test suites unless requested or clearly necessary.
- For quick script validation, a lightweight example may be placed under `if __name__ == "__main__":`.

Useful manual checks may include:

- Python syntax compilation for changed files.
- Focused unit tests for changed behavior.
- Relevant integration checks when the change touches external systems.
- Static checks or formatting checks when the repository already uses them.

Run only the checks that are relevant to the change and practical in the current environment.

## 16. Configuration and Runtime Values

Keep runtime configuration explicit.

Guidelines:

- Put script-level constants near the top of the file.
- Do not hide configuration inside deeply nested functions.
- Read environment variables at clear boundaries.
- Validate required configuration early.
- Avoid global mutable configuration.
- Keep secrets out of source code and logs.
- Prefer typed configuration objects when the configuration becomes non-trivial.
- Keep development, test, and runtime configuration separable.

## 17. Public APIs

For public functions, classes, and modules:

- Keep signatures stable unless change is required.
- Use explicit parameter names.
- Avoid positional-only cleverness.
- Return predictable types.
- Raise documented exceptions where appropriate.
- Avoid leaking internal implementation details.
- Keep compatibility with existing import usage when practical.
- Treat public names as contracts once other modules depend on them.

## 18. Review Checklist

Before finalizing a change, verify:

- The change directly addresses the requested task.
- No unrelated refactor was introduced.
- Imports are clean.
- Type hints are present where useful.
- Public functions have clear docstrings.
- Exceptions are specific and not silently swallowed.
- Logging uses lazy formatting.
- Paths use `Path`.
- Strings use double quotes.
- Async code does not block the event loop.
- New dependencies were avoided unless justified.
- Manual checks are listed for the user when they cannot be run directly.
