You're are a talented and professional tester, python developer, and educator.
Your task is to create meaningful test messages to all python tests provided in section "Tests before".
You'll be provided with context code for better understanding.

**Important:** You can **only** add variables and change/add test comments in test functions. Everything else should be left intact.


### One-test Examples

Please note that here are simple examples with one test case.
You'll be provided with "Tests before" as file, and, after adding messages, you should return "Tests after" as file.

Context:
```python
class Statistics:
    """Class to calculate statistics on the pd.DataFrame / pd.Series"""
    @staticmethod
    def get_lens(text_series: pd.Series) -> pd.Series:
        """Return the series containing the lengths of the text column"""
        return text_series.str.len()
```

Test before:
```python
def test_get_lens(sample_df: pd.DataFrame) -> None:
    lengths = Statistics.get_lens(sample_df['text'])
    assert lengths.tolist() == [22, 20], "get_lens() works incorrectly"
```

Test after:
```python
def test_get_lens(sample_df: pd.DataFrame) -> None:
    lengths = Statistics.get_lens(sample_df['text'])
    test_message = f"""\
get_lens() works incorrectly
Input texts:
{{sample_df['text'].tolist()}}
Expected: [22, 20]
Got: {{lengths.tolist()}}
"""
    assert lengths.tolist() == [22, 20], test_message
```

---

Context:
```python
class Statistics:
    """Class to calculate statistics on the pd.DataFrame / pd.Series"""
    @staticmethod
    def get_quantile(series: pd.Series, p: float) -> tuple:
        """Return the p quantile"""
        return series.quantile(p)
```

Test before:
```python
@pytest.mark.parametrize(
    "series, quantile, expected", [
        (pd.Series([1, 2, 3, 4, 5]), 0.5, 3),
        (pd.Series([10, 20, 30]), 0.25, 15),
    ]
)
def test_get_quantile(series: pd.Series, quantile: float, expected: float) -> None:
    assert Statistics.get_quantile(series, quantile) == expected
```

Test after:
```python
@pytest.mark.parametrize(
    "series, quantile, expected", [
        (pd.Series([1, 2, 3, 4, 5]), 0.5, 3),
        (pd.Series([10, 20, 30]), 0.25, 15),
    ]
)
def test_get_quantile(series: pd.Series, quantile: float, expected: float) -> None:
    returned_quantile = Statistics.get_quantile(series, quantile)
    input_series = series.tolist()
    test_message = f"""\
get_quantile() works incorrectly
Input series: {{input_series}}
Quantile: {{quantile}}
Expected: {{expected}}
Got: {{returned_quantile}}
    """

    assert returned_quantile == expected, test_message
```

---

Context:
```python
class DataProcessor:
    """Class to process the IMDB dataset"""
    @staticmethod
    def remove_outliers(df: pd.DataFrame, series: pd.Series, max_val: int) -> pd.DataFrame:
        """Remove outliers from the pd.DataFrame"""
        return df[series <= max_val]
```

Test before:
```python
@pytest.mark.parametrize(
    "df, series, max_val, expected_len", [
        (pd.DataFrame({{'val': [1, 1000]}}), pd.Series([1, 1000]), 999, 1),
        (pd.DataFrame({{'val': [1, 2, 3]}}), pd.Series([1, 2, 3]), 3, 3),
    ]
)
def test_remove_outliers_param(df: pd.DataFrame, series: pd.Series, max_val: int, expected_len: int) -> None:
    result = DataProcessor.remove_outliers(df, series, max_val)
    assert len(result) == expected_len, "remove_outliers() works incorrectly with non-default parameters"
```

Test after:
```python
@pytest.mark.parametrize(
    "df, series, max_val, expected_len", [
        (pd.DataFrame({{'val': [1, 1000]}}), pd.Series([1, 1000]), 999, 1),
        (pd.DataFrame({{'val': [1, 2, 3]}}), pd.Series([1, 2, 3]), 3, 3),
    ]
)
def test_remove_outliers_param(df: pd.DataFrame, series: pd.Series, max_val: int, expected_len: int) -> None:
    result = DataProcessor.remove_outliers(df, series, max_val)
    test_message = f"""\
remove_outliers() works incorrectly
Input DataFrame:
{{df}}
Input series (based on which outliers are removed):
{{series.tolist()}}
Max value for outliers: {{max_val}}
Expected length out output: {{expected_len}}
Got: {{len(result)}}
    """
    assert len(result) == expected_len, test_message
```

### Your Task

Context:
```python
{context}
```

Tests before:
```python
{tests_before}
```

Tests after:
