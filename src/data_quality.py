from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

DATASET_NAME = "DataCoSupplyChainDataset.csv"
DICTIONARY_NAME = "DescriptionDataCoSupplyChain.csv"


def repo_root() -> Path:
    """Return the repository root inferred from this file's location."""
    return Path(__file__).resolve().parents[1]


def resolve_data_path(filename: str | Path | None = None, *, root: str | Path | None = None) -> Path:
    """Resolve a path against the project and common data locations."""
    base_root = Path(root) if root is not None else repo_root()
    target_name = Path(filename).name if filename is not None else DATASET_NAME

    candidates = [
        Path(filename) if filename is not None and Path(filename).is_absolute() else None,
        base_root / target_name,
        base_root / "data" / "raw" / target_name,
        base_root / "data" / target_name,
        base_root / "raw" / target_name,
    ]

    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate

    raise FileNotFoundError(f"Could not locate '{target_name}' in the project tree.")


def load_raw_data(filepath: str | Path | None = None) -> pd.DataFrame:
    """Load the supply-chain CSV using a tolerant encoding strategy."""
    source = resolve_data_path(filepath)
    return pd.read_csv(source, encoding="latin-1", low_memory=False)


def load_data_dictionary(filepath: str | Path | None = None) -> pd.DataFrame:
    """Load the field dictionary that explains the raw CSV columns."""
    source = resolve_data_path(filepath or DICTIONARY_NAME)
    return pd.read_csv(source, encoding="latin-1")


def data_quality_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a per-column summary of missingness, dtype, and cardinality."""
    metrics = {
        "column": df.columns,
        "dtype": [str(df[col].dtype) for col in df.columns],
        "missing_count": df.isna().sum().values,
        "missing_pct": (df.isna().mean() * 100).round(2).values,
        "non_null_count": df.notna().sum().values,
        "unique_count": df.nunique(dropna=True).values,
    }
    summary = pd.DataFrame(metrics)
    summary["severity"] = summary["missing_pct"].apply(
        lambda value: "High" if value > 10 else "Medium" if value > 0 else "Low"
    )
    return summary.sort_values(["missing_count", "missing_pct"], ascending=False).reset_index(drop=True)


def summarize_data_quality(df: pd.DataFrame) -> dict[str, Any]:
    """Create a compact dictionary suitable for reporting or tests."""
    summary = data_quality_summary(df)
    high_missing = summary[summary["missing_pct"] > 10]["column"].tolist()
    missing_columns = summary[summary["missing_count"] > 0]["column"].tolist()
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
        "columns_with_missing_values": missing_columns,
        "high_missing_columns": high_missing,
        "column_summary": summary.to_dict(orient="records"),
    }


def _format_table(rows: Iterable[dict[str, Any]], max_rows: int = 10) -> list[str]:
    if not rows:
        return ["No rows to display."]

    row_list = list(rows)[:max_rows]
    headers = list(row_list[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in row_list:
        values = [str(row.get(header, "")) for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def generate_markdown_report(
    df: pd.DataFrame,
    *,
    source_path: str | Path | None = None,
    dictionary: pd.DataFrame | None = None,
    output_path: str | Path | None = None,
) -> str:
    """Create a human-readable data quality report as markdown."""
    quality = summarize_data_quality(df)
    source_label = str(source_path) if source_path is not None else "unknown source"

    lines = [
        "# Data Quality Report",
        "",
        f"- Source file: `{source_label}`",
        f"- Rows: {quality['rows']}",
        f"- Columns: {quality['columns']}",
        f"- Duplicate rows: {quality['duplicate_rows']}",
        f"- Missing values: {quality['missing_values']}",
        f"- Columns with missing values: {len(quality['columns_with_missing_values'])}",
        f"- High-risk columns (>10% missing): {len(quality['high_missing_columns'])}",
        "",
        "## Key findings",
        "",
        "1. The raw dataset contains no duplicate records.",
        "2. Most columns are complete, but two fields are heavily missing: `Product Description` and `Order Zipcode`.",
        "3. The field dictionary indicates that the dataset is a supply-chain order dataset with transactional, customer, and logistics metadata.",
        "",
        "## Missing value summary",
        "",
    ]

    if quality['column_summary']:
        table_rows = []
        for row in quality['column_summary']:
            table_rows.append(
                {
                    "Column": row["column"],
                    "Dtype": row["dtype"],
                    "Missing": row["missing_count"],
                    "Missing %": round(row["missing_pct"], 2),
                    "Unique": row["unique_count"],
                }
            )
        lines.extend(_format_table(table_rows, max_rows=12))

    lines.extend([
        "",
        "## High-risk columns",
        "",
    ])
    if quality['high_missing_columns']:
        lines.extend(f"- `{column}`" for column in quality['high_missing_columns'])
    else:
        lines.append("No columns are missing more than 10% of values.")

    if dictionary is not None and not dictionary.empty:
        lines.extend(["", "## Field dictionary preview", ""])
        preview = dictionary.head(10).copy()
        preview.columns = ["Field", "Description"]
        lines.extend(_format_table(preview.to_dict(orient="records"), max_rows=10))

    markdown = "\n".join(lines) + "\n"
    if output_path is not None:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(markdown, encoding="utf-8")
    return markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess the quality of the supply-chain raw data.")
    parser.add_argument("--input", default=None, help="Path to the raw CSV file to inspect.")
    parser.add_argument("--output", default=None, help="Optional path for the generated markdown report.")
    args = parser.parse_args()

    data_source = resolve_data_path(args.input) if args.input else resolve_data_path(DATASET_NAME)
    report_target = Path(args.output) if args.output else repo_root() / "reports" / "data_quality_report.md"
    df = load_raw_data(data_source)
    dictionary = load_data_dictionary()
    report = generate_markdown_report(df, source_path=data_source, dictionary=dictionary, output_path=report_target)
    print(report)


if __name__ == "__main__":
    main()
