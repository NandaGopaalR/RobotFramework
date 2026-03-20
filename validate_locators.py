import re
import sys
import os
import json

# ANSI color codes
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Approval modes:
# "step"  = ask for each issue
# "bulk"  = ask once for all issues
# "ci"    = no prompts (for CI/CD pipelines)
APPROVE_MODE = "step"   # change to "bulk" or "ci" as needed

IGNORE_FILE = "ignored.json"

def load_ignored():
    if os.path.exists(IGNORE_FILE):
        try:
            with open(IGNORE_FILE, "r", encoding="utf-8") as f:
                return {item["id"]: item["line"] for item in json.load(f)}
        except Exception:
            return {}
    return {}

def save_ignored(ignored_dict):
    data = [{"id": k, "line": v} for k, v in ignored_dict.items()]
    with open(IGNORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Configuration: choose "snake", "pascal", or "camel"
NAMING_RULES = {
    "robot": {
        "variables": "pascal",
        "keywords": "pascal",
        "testcases": "pascal"
    },
    "resource": {
        "variables": "snake",
        "keywords": "camel",
        "testcases": "camel"
    }
}

# Registry of declared variables (from resource files)
DECLARED_VARS = {}

def is_snake_case(name: str) -> bool:
    return bool(re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', name))

def is_pascal_case(name: str) -> bool:
    return bool(re.match(r'^[A-Z][a-z0-9A-Z]*$', name))

def is_camel_case(name: str) -> bool:
    return bool(re.match(r'^[a-z]+[A-Za-z0-9]*$', name))

def suggest_snake_case(name: str) -> str:
    suggestion = re.sub(r'(?<!_)([A-Z])', r'_\1', name)
    return suggestion.lower().lstrip("_")

def suggest_pascal_case(name: str) -> str:
    return name.title().replace("_", "")

def suggest_camel_case(name: str) -> str:
    return name[0].lower() + re.sub(r'[_-]', '', name.title())[1:]

def check_rule(name: str, rule: str):
    if rule == "snake":
        return is_snake_case(name), suggest_snake_case(name), "snake_case"
    elif rule == "pascal":
        return is_pascal_case(name), suggest_pascal_case(name), "PascalCase"
    elif rule == "camel":
        return is_camel_case(name), suggest_camel_case(name), "camelCase"
    return True, name, "unknown"

def is_locator_value(value: str) -> bool:
    return (
        "xpath" in value.lower()
        or "css" in value.lower()
        or value.strip().startswith("//")
        or value.strip().startswith("id=")
        or value.strip().startswith("css=")
    )

def check_alignment(line: str, line_no: int, file_path: str, depth: int, is_name_line: bool):
    issues = []
    if line.strip():
        stripped = line.strip()
        actual_indent = len(line) - len(line.lstrip(" "))

        if re.match(r"^ELSE IF\b", stripped) or re.match(r"^ELSE\b", stripped):
            expected_indent = (depth - 1) * 4
        elif re.match(r"^END\b", stripped):
            expected_indent = (depth - 1) * 4
        else:
            expected_indent = depth * 4

        if is_name_line:
            if actual_indent != 0:
                corrected = line.lstrip()
                issues.append({
                    "file": file_path,
                    "line_no": line_no,
                    "line": line.rstrip(),
                    "suggestion": corrected,
                    "rule": "Name must start at column 0",
                    "approve_line": corrected
                })
        else:
            if actual_indent != expected_indent:
                corrected = " " * expected_indent + line.lstrip()
                issues.append({
                    "file": file_path,
                    "line_no": line_no,
                    "line": line.rstrip(),
                    "suggestion": corrected,
                    "rule": f"Indentation must be {expected_indent} spaces",
                    "approve_line": corrected
                })
    return issues

def validate_file(file_path: str):
    issues = []
    in_test_case = False
    in_variables_section = False
    in_keywords_section = False
    depth = 0

    file_type = "robot" if file_path.endswith(".robot") else "resource"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("#"):
            continue

        if stripped.startswith("***"):
            section = stripped.lower().strip("* ").strip()
            in_test_case = section == "test cases"
            in_variables_section = section == "variables"
            in_keywords_section = section == "keywords"
            depth = 0
            continue

        section_type = None
        if in_variables_section:
            section_type = "variables"
        elif in_test_case:
            section_type = "testcases"
        elif in_keywords_section:
            section_type = "keywords"

        if (in_test_case or in_keywords_section) and stripped and not line.startswith(" "):
            issues.extend(check_alignment(line, line_no, file_path, depth, True))
            depth = 1
            continue
        else:
            issues.extend(check_alignment(line, line_no, file_path, depth, False))

        if re.match(r"^\s*FOR\b", stripped) or re.match(r"^\s*IF\b", stripped):
            depth += 1
        elif re.match(r"^\s*END\b", stripped):
            depth = max(1, depth - 1)

        # Variable checks
        for pattern, prefix in [(r"\${([^}]+)}", "${"), (r"@{([^}]+)}", "@{"), (r"&{([^}]+)}", "&{")]:
            match = re.search(pattern, stripped)
            if match and section_type:
                var_name = match.group(1)

                # Skip dictionary key access like ${List['Status']}
                if "[" in var_name and "]" in var_name:
                    continue

                # Detect locator variables
                locator = False
                if "=" in stripped:
                    parts = stripped.split("=", 1)
                    if len(parts) > 1 and is_locator_value(parts[1]):
                        locator = True

                # If declared in resource, enforce resource rule
                if var_name in DECLARED_VARS:
                    rule = DECLARED_VARS[var_name]["rule"]
                    ok, suggestion, rule_name = check_rule(var_name, rule)
                else:
                    rule = NAMING_RULES[file_type][section_type]
                    ok, suggestion, rule_name = check_rule(var_name, rule)

                    # Store declaration if in resource file
                    if file_type == "resource":
                        DECLARED_VARS[var_name] = {"rule": rule, "file_type": file_type, "locator": locator}

                if not ok:
                    approve_line = line.replace(f"{prefix}{var_name}}}", f"{prefix}{suggestion}}}")
                    issues.append({
                        "file": file_path,
                        "line_no": line_no,
                        "line": line.rstrip(),
                        "error_var": var_name,
                        "suggestion": f"{prefix}{suggestion}}}",
                        "rule": rule_name,
                        "approve_line": approve_line.rstrip()
                    })
    return issues

def validate_folder(folder_path: str):
    all_issues = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".robot") or file.endswith(".resource"):
                file_path = os.path.join(root, file)
                all_issues.extend(validate_file(file_path))
    return all_issues

def apply_fixes(file_path, issues):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Group issues by line number
    grouped = {}
    for issue in issues:
        grouped.setdefault(issue["line_no"], []).append(issue)

    for line_no, line_issues in grouped.items():
        idx = line_no - 1
        current_line = lines[idx].rstrip("\n")

        # Start from the original line
        modified_line = current_line
        for issue in line_issues:
            modified_line = issue["approve_line"]

        lines[idx] = modified_line + "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_file.py <file_or_folder_path>")
        sys.exit(1)

    path_to_check = sys.argv[1]
    problems = []
    if os.path.isfile(path_to_check):
        problems = validate_file(path_to_check)
    elif os.path.isdir(path_to_check):
        problems = validate_folder(path_to_check)
    else:
        print(f"❌ Path not found: {path_to_check}")
        sys.exit(1)

    if problems:
        approved = []
        ignored = load_ignored()

        if APPROVE_MODE == "step":
            cancelled = False
            # Group problems by line number
            grouped = {}
            for p in problems:
                grouped.setdefault(p["line_no"], []).append(p)

            for line_no, line_issues in grouped.items():
                issue_id = f"{line_issues[0]['file']}:{line_no}"
                current_line = line_issues[0]['line']

                # Build combined suggestion
                combined_line = current_line
                for issue in line_issues:
                    combined_line = issue["approve_line"]

                print(f"{line_issues[0]['file']}:{line_no}")
                print(f"| {current_line}")
                for issue in line_issues:
                    print(f"    ^-- {issue['rule']}. Suggested: {BLUE}{issue['suggestion']}{RESET}")
                print(f"    Combined approve line: {combined_line}")

                choice = input("Approve this fix? (y/n/i for ignore/c to cancel): ")

                if choice.lower() == "y":
                    approved.append({
                        "file": line_issues[0]['file'],
                        "line_no": line_no,
                        "approve_line": combined_line
                    })
                elif choice.lower() == "i":
                    print("⏭️ Ignored this issue permanently.")
                    ignored[issue_id] = current_line
                elif choice.lower() == "c":
                    print("🚫 Cancelled approval process.")
                    cancelled = True
                    break
                else:
                    print("❌ Rejected this fix.")

            save_ignored(ignored)

            if cancelled and approved:
                final_choice = input("Apply approved fixes so far? (y/n): ")
                if final_choice.lower() != "y":
                    approved = []

        elif APPROVE_MODE == "bulk":
            grouped = {}
            for p in problems:
                grouped.setdefault(p["line_no"], []).append(p)

            for line_no, line_issues in grouped.items():
                current_line = line_issues[0]['line']
                combined_line = current_line
                for issue in line_issues:
                    combined_line = issue["approve_line"]

                print(f"{line_issues[0]['file']}:{line_no}")
                print(f"| {current_line}")
                for issue in line_issues:
                    print(f"    ^-- {issue['rule']}. Suggested: {BLUE}{issue['suggestion']}{RESET}")
                print(f"    Combined approve line: {combined_line}")

            choice = input("Approve all fixes? (y/n): ")
            if choice.lower() == "y":
                approved = [{"file": i[0]['file'], "line_no": ln, "approve_line": i[-1]['approve_line']}
                            for ln, i in grouped.items()]

        elif APPROVE_MODE == "ci":
            print("CI mode: listing issues only (no fixes applied).")
            grouped = {}
            for p in problems:
                grouped.setdefault(p["line_no"], []).append(p)

            for line_no, line_issues in grouped.items():
                current_line = line_issues[0]['line']
                combined_line = current_line
                for issue in line_issues:
                    combined_line = issue["approve_line"]

                print(f"{line_issues[0]['file']}:{line_no}")
                print(f"| {current_line}")
                for issue in line_issues:
                    print(f"    ^-- {issue['rule']}. Suggested: {BLUE}{issue['suggestion']}{RESET}")
                print(f"    Combined approve line: {combined_line}")

            approved = []
            if problems:
                sys.exit(2)

        # Apply fixes if any were approved
        if approved:
            if os.path.isfile(path_to_check):
                apply_fixes(path_to_check, approved)
            else:
                files_grouped = {}
                for p in approved:
                    files_grouped.setdefault(p["file"], []).append(p)
                for fpath, issues in files_grouped.items():
                    apply_fixes(fpath, issues)
            print(f"✅ Fixes applied successfully. Ignored issues: {len(ignored)}")
        else:
            if len(ignored) > 0:
                print(f"✅ All issues resolved or ignored. Ignored issues: {len(ignored)}")
            else:
                print("🟦 No fixes applied.")
    else:
        print(f"✅ All variables and alignment follow conventions. Ignored issues: {len(load_ignored())}")