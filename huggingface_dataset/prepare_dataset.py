#!/usr/bin/env python3
"""
Prepare Gov-ZA Multilingual dataset for Hugging Face upload.

This script converts the sentence-aligned JSONL files into Parquet format
with train/test/eval splits, matching the structure of vukuzenzele-sentence-aligned.
"""

import json
import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
import argparse


def load_jsonl(file_path):
    """Load JSONL file into list of dicts"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def prepare_language_pair(input_file, output_dir, lang1, lang2, test_size=0.15, eval_size=0.15, random_state=42):
    """
    Convert JSONL aligned data to Parquet with train/test/eval splits.

    Args:
        input_file: Path to input JSONL file
        output_dir: Directory to save Parquet files
        lang1: First language code
        lang2: Second language code
        test_size: Proportion for test set (default 0.15 = 15%)
        eval_size: Proportion for eval set (default 0.15 = 15%)
        random_state: Random seed for reproducibility
    """
    print(f"Processing {lang1}-{lang2}...")

    # Load data
    data = load_jsonl(input_file)
    print(f"  Loaded {len(data)} aligned sentence pairs")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Rename columns to match language codes
    df = df.rename(columns={'src': lang1, 'tgt': lang2})

    # Add index column (matching vukuzenzele structure)
    df['__index_level_0__'] = range(len(df))

    # Split into train/temp (temp = test + eval)
    train_df, temp_df = train_test_split(
        df,
        test_size=(test_size + eval_size),
        random_state=random_state
    )

    # Split temp into test/eval
    test_df, eval_df = train_test_split(
        temp_df,
        test_size=(eval_size / (test_size + eval_size)),
        random_state=random_state
    )

    print(f"  Split: train={len(train_df)}, test={len(test_df)}, eval={len(eval_df)}")

    # Create output directory structure
    pair_dir = Path(output_dir) / f"{lang1}-{lang2}"
    pair_dir.mkdir(parents=True, exist_ok=True)

    # Save as Parquet files
    for split_name, split_df in [('train', train_df), ('test', test_df), ('eval', eval_df)]:
        split_dir = pair_dir / split_name
        split_dir.mkdir(parents=True, exist_ok=True)

        output_file = split_dir / "0000.parquet"
        split_df.to_parquet(output_file, index=False)
        print(f"  Saved {split_name}: {output_file}")

    return {
        'pair': f"{lang1}-{lang2}",
        'total': len(df),
        'train': len(train_df),
        'test': len(test_df),
        'eval': len(eval_df)
    }


def main():
    parser = argparse.ArgumentParser(description='Prepare Gov-ZA dataset for Hugging Face')
    parser.add_argument('--input-dir', default='../data/opt_aligned_out',
                        help='Directory containing aligned JSONL files')
    parser.add_argument('--output-dir', default='./data',
                        help='Output directory for Parquet files')
    parser.add_argument('--test-size', type=float, default=0.15,
                        help='Test set proportion (default: 0.15)')
    parser.add_argument('--eval-size', type=float, default=0.15,
                        help='Eval set proportion (default: 0.15)')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Language code mapping
    lang_map = {
        'afr': 'Afrikaans',
        'eng': 'English',
        'nbl': 'isiNdebele',
        'nso': 'Sepedi',
        'sot': 'Sesotho',
        'ssw': 'Siswati',
        'tsn': 'Setswana',
        'tso': 'Xitstonga',
        'ven': 'Tshivenda',
        'xho': 'isiXhosa',
        'zul': 'isiZulu'
    }

    # Find all aligned JSONL files
    aligned_files = sorted(input_dir.glob('aligned-*.jsonl'))

    if not aligned_files:
        print(f"ERROR: No aligned JSONL files found in {input_dir}")
        return

    print(f"Found {len(aligned_files)} aligned language pairs")
    print("=" * 60)

    stats = []

    for file_path in aligned_files:
        # Extract language codes from filename
        # Format: aligned-{lang1}-{lang2}.jsonl
        filename = file_path.stem  # removes .jsonl
        parts = filename.split('-')

        if len(parts) != 3 or parts[0] != 'aligned':
            print(f"Skipping {file_path.name} - unexpected format")
            continue

        lang1, lang2 = parts[1], parts[2]

        if lang1 not in lang_map or lang2 not in lang_map:
            print(f"Skipping {file_path.name} - unknown language code")
            continue

        try:
            pair_stats = prepare_language_pair(
                file_path,
                output_dir,
                lang1,
                lang2,
                test_size=args.test_size,
                eval_size=args.eval_size
            )
            stats.append(pair_stats)
        except Exception as e:
            print(f"  ERROR processing {lang1}-{lang2}: {e}")
            continue

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Create summary DataFrame
    stats_df = pd.DataFrame(stats)
    print(stats_df.to_string(index=False))

    # Save summary
    summary_file = output_dir / "dataset_summary.csv"
    stats_df.to_csv(summary_file, index=False)
    print(f"\nSummary saved to: {summary_file}")

    # Calculate totals
    print(f"\nTotal language pairs: {len(stats)}")
    print(f"Total aligned pairs: {stats_df['total'].sum():,}")
    print(f"Total train pairs: {stats_df['train'].sum():,}")
    print(f"Total test pairs: {stats_df['test'].sum():,}")
    print(f"Total eval pairs: {stats_df['eval'].sum():,}")


if __name__ == '__main__':
    main()
