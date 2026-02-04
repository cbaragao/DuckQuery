import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
from m_ast.nodes import SelectColumns
from main import List


def test_run_query_with_selectcolumns_node():
    df = pd.DataFrame({'id':[1,2], 'name':['A','B'], 'age':[30,40]})
    with List(df) as lst:
        lst.register_table('other', pd.DataFrame({'x':[1]}))
        result = lst.run_query(select=SelectColumns(table='current_df', columns=['id', 'name'])).data()
        assert list(result.columns) == ['id', 'name']
