"""Fixture with high cyclomatic complexity and deep nesting."""


def classify(items):
    result = []
    for item in items:
        if item.get("kind") == "a":
            if item.get("priority") == "high":
                if item.get("owner"):
                    if item.get("due"):
                        result.append(("a-high-owned-due", item))
                    else:
                        result.append(("a-high-owned", item))
                else:
                    result.append(("a-high", item))
            elif item.get("priority") == "low":
                result.append(("a-low", item))
            else:
                result.append(("a-unknown", item))
        elif item.get("kind") == "b":
            if item.get("size") == "big":
                result.append(("b-big", item))
            elif item.get("size") == "small":
                result.append(("b-small", item))
            else:
                result.append(("b-unknown", item))
        elif item.get("kind") == "c":
            result.append(("c", item))
        elif item.get("kind") == "d":
            result.append(("d", item))
        else:
            result.append(("other", item))
    return result
