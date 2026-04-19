"""Column name normalization utilities for DuckQuery."""

import re

_SUFFIX_RE = re.compile(r"^(.+)_(\d+)$")


def normalize_suffixes(columns: list[str]) -> list[str]:
    """Strip numeric suffixes (_1, _2, …) from column names when safe.

    A strip is safe when the candidate base name does not already appear in
    *columns* and no two columns would strip to the same base name.

    Args:
        columns: Ordered list of column name strings.

    Returns:
        New list with suffixes removed where safe; original names otherwise.

    Examples:
        >>> normalize_suffixes(["name_1", "value_2"])
        ['name', 'value']
        >>> normalize_suffixes(["id", "id_1"])
        ['id', 'id_1']
        >>> normalize_suffixes(["x_1", "x_2"])
        ['x_1', 'x_2']
    """
    originals: set[str] = set(columns)
    candidates: dict[int, str] = {}

    for i, col in enumerate(columns):
        m = _SUFFIX_RE.match(col)
        if m:
            candidates[i] = m.group(1)

    # Count how many columns strip to each base name
    from collections import Counter

    base_counts: Counter[str] = Counter(candidates.values())

    result = list(columns)
    for i, base in candidates.items():
        if base_counts[base] > 1:
            continue  # two columns would collide
        if base in originals:
            continue  # conflicts with an existing column
        result[i] = base

    return result
