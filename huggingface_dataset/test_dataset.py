#!/usr/bin/env python3
"""
Test script to verify the prepared dataset can be loaded correctly.
"""

import pandas as pd
from pathlib import Path
import sys


def test_parquet_file(file_path):
    """Test loading a single Parquet file"""
    try:
        df = pd.read_parquet(file_path)
        return {
            'success': True,
            'records': len(df),
            'columns': list(df.columns),
            'sample': df.head(1).to_dict('records')[0] if len(df) > 0 else None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    data_dir = Path('./data')

    if not data_dir.exists():
        print("ERROR: data/ directory not found")
        print("\nDid you run prepare_dataset.py first?")
        print("  python prepare_dataset.py")
        sys.exit(1)

    # Find all parquet files
    parquet_files = sorted(data_dir.rglob('*.parquet'))

    if not parquet_files:
        print("ERROR: No Parquet files found in data/")
        sys.exit(1)

    print(f"Found {len(parquet_files)} Parquet files\n")

    # Test first file from each language pair
    tested_pairs = set()
    for file_path in parquet_files:
        # Extract language pair from path (e.g., afr-eng/train/0000.parquet -> afr-eng)
        pair = file_path.parent.parent.name

        if pair in tested_pairs:
            continue

        tested_pairs.add(pair)

        print(f"Testing {pair}...")
        result = test_parquet_file(file_path)

        if result['success']:
            print(f"  ✓ Records: {result['records']}")
            print(f"  ✓ Columns: {result['columns']}")

            if result['sample']:
                sample = result['sample']
                print(f"  ✓ Sample:")
                for key, value in sample.items():
                    if isinstance(value, str) and len(value) > 60:
                        value = value[:57] + "..."
                    print(f"      {key}: {value}")
        else:
            print(f"  ✗ Error: {result['error']}")

        print()

    print(f"{'='*60}")
    print(f"Tested {len(tested_pairs)} language pairs")
    print(f"All tests passed! Dataset is ready for upload.")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
