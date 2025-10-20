### Python Usage Preferences

- **Code Structure & Organization**:
  - **Script + Variable Configuration**: By default, CLI is not used unless specifically requested. Configuration items are defined as constants or variables at the top of the script.
  - **Modular Design**: Prefers to break down the code into small, reusable modules.

- **Import Style**:
  - **Unified Import Method**: Uses `from pathlib import Path`, avoiding `import pathlib`.

- **String Handling**:
  - **String Format**: Prefers double quotes (`"`) over single quotes (`'`).

- **Type Hinting**:
  - **Type Annotations**: Prefers type hints. Non-primitive types are always enclosed in double quotes.

- **Object-Oriented Programming**:
  - **Class Syntax**: Prefers using `class` for encapsulation of complex logic.

- **Code Style**:
  - **Clean, Readable Code**: Encapsulates complex logic into functions and classes. Frequently adds detailed comments.

- **Error Handling**:
  - **Exception Handling**: Uses `try-except` blocks for exceptions with appropriate logging.

- **File & Data Operations**:
  - **Path Management**: Prefers `Pathlib` for handling file paths.
  - **Directory Operations**: Uses methods like `Path.mkdir()` and `Path.exists()` to check and create directories.

- **Testing & Debugging**:
  - **Simple Test Cases**: Prefers simple functional tests added after the `__main__` block.

- **Performance Optimization**:
  - **Execution Efficiency**: Focused on optimizing code execution, especially with large datasets.
  - **Libraries**: Frequently uses `Polars` and `Pandas`.

- **Libraries & Frameworks**:
  - **Data Analysis & Processing**: Prefers `Pandas`, `Polars`, and `SQLAlchemy`.
  - **Task Scheduling**: Uses `Apache Airflow` for task automation.
  - **Machine Learning**: Utilizes `scikit-learn` and `XGBoost` when needed.

- **Asynchronous & Concurrent Processing**:
  - **Asyncio & Multi-threading**: Prefers `asyncio` and multi-threading for concurrent processing.
