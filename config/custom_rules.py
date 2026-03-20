import re
from robocop.linter.rules import Rule, RuleSeverity, VisitorChecker

class LocatorSnakeCaseRule(Rule):
    """
    Enforce snake_case lowercase naming for variables holding XPath or CSS locators.
    """
    name = "locator-snake-case"
    rule_id = "LOC01"
    # Show variable name with ${} wrapper in the message
    message = "Locator variable '{variable}' must be snake_case with lower case letters."
    severity = RuleSeverity.ERROR


class LocatorSnakeCaseChecker(VisitorChecker):
    locator_snake_case: LocatorSnakeCaseRule

    def visit_Variable(self, node):  # noqa: N802
        # node.name is like "${THIS_CKE}"
        raw_name = node.name.strip("${}").strip()

        # node.value is a list of tokens, join them into a string
        if node.value:
            value_str = " ".join(str(v) for v in node.value)

            # Detect locator values (XPath or CSS)
            if value_str.startswith("//") or value_str.startswith("css") \
               or "xpath" in value_str.lower() or "css" in value_str.lower():
                # Enforce snake_case lowercase
                if not re.fullmatch(r"[a-z0-9_]+", raw_name):
                    self.report(
                        self.locator_snake_case,
                        variable=node.name,   # keep ${NAME} for message
                        node=node,
                        col=node.col_offset
                    )