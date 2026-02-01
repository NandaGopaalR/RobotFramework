# Copilot Instructions for RobotFramework_Project/Base

## Project Overview
- This is a Robot Framework test automation project using SeleniumLibrary for browser automation.
- Main test cases are in the `Test/` directory, with configuration in `config/` and results in `results/`.
- The project uses a Python virtual environment (`venv/`) and dependencies are listed in `requirments.txt`.

## Key Directories & Files
- `Test/`: Contains Robot Framework test suites (e.g., `Selenium_test.robot`).
- `config/defaults.yaml`: Stores configuration variables (e.g., URL, browser type) loaded in tests.
- `Resorces/`: Intended for shared resources, functions, and libraries (currently empty).
- `results/`: Stores Robot Framework output files (`log.html`, `output.xml`, `report.html`).
- `requirments.txt`: Lists all required Python and Robot Framework packages.

## Patterns & Conventions
- Test cases use variables from YAML config via the `Variables` setting in `.robot` files.
  - Example: `${url}=    ${CONFIGS.url}`
- SeleniumLibrary is the primary library for browser automation.
- Use `${CURDIR}` for relative paths in test files.
- All browser and URL settings should be managed in `config/defaults.yaml`.
- Test case names and keywords should be descriptive and follow Robot Framework conventions.

## Developer Workflows
- **Setup:**
  - Create and activate the Python virtual environment in `venv/`.
  - Install dependencies: `pip install -r requirments.txt`.
- **Running Tests:**
  - Run tests with: `robot Test/Selenium_test.robot`
  - Results are output to the `results/` directory.
- **Debugging:**
  - Review `results/log.html` and `results/output.xml` for detailed execution logs and errors.
  - Common Selenium errors may relate to missing or misconfigured browser drivers.
- **Configuration:**
  - Update `config/defaults.yaml` to change test parameters (e.g., browser, URL).

## Integration Points
- Integrates with Selenium via `robotframework-seleniumlibrary`.
- Uses YAML for configuration (via `PyYAML`).
- No custom Python libraries or keywords are present by default, but `Resorces/` is structured for future expansion.

## Project-Specific Notes
- The `Resorces/` directory is reserved for reusable keywords, functions, and libraries, but is currently empty.
- All test output is centralized in `results/` for easy review.
- The project is designed for extensibility: add new test suites to `Test/`, new configs to `config/`, and new resources to `Resorces/`.

---

For any unclear or missing conventions, review the example in `Test/Selenium_test.robot` and `config/defaults.yaml`.
