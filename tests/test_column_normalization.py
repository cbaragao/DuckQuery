import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import List, Jointype


def test_column_normalization_no_suffixes():
    """Ensure run_query normalizes DuckDB/pandas renamed duplicate columns (no '_1' suffixes)."""
    main_df = pd.DataFrame(
        {"id": [1, 2, 3], "name": ["A", "B", "C"], "department_id": [10, 20, 10]}
    )

    dept_df = pd.DataFrame({"id": [10, 20], "department_name": ["X", "Y"]})

    with List(main_df) as lst:
        lst.register_table("departments", dept_df)

        # Join that would normally produce duplicate 'id' columns
        result = lst.run_query(
            select=["id", "name", "department_id", "departments.id", "department_name"],
            joins=[
                {
                    "type": Jointype.INNER,
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id",
                }
            ],
        ).data()

        # Ensure no automatic '_1' suffixes remain in column names
        assert not any(
            str(c).endswith("_1") or str(c).endswith("_2") for c in result.columns
        )
