#!/usr/bin/env python3
"""
Upload the Gov-ZA Cabinet Statements dataset to Hugging Face Hub.

Before running this script:
1. Install dependencies: pip install -r requirements.txt
2. Login to Hugging Face: huggingface-cli login
3. Prepare the data: python prepare_dataset.py
"""

import argparse
from pathlib import Path
from huggingface_hub import HfApi, create_repo
import os


def upload_dataset(repo_id, data_dir, readme_path, token=None, private=False):
    """
    Upload dataset to Hugging Face Hub.

    Args:
        repo_id: Repository ID (e.g., "dsfsi/govza-sa-cabinet-statements")
        data_dir: Directory containing the prepared Parquet files
        readme_path: Path to README.md file
        token: Hugging Face API token (optional, uses cached token if None)
        private: Whether to create a private repository
    """
    api = HfApi()

    # Create repository if it doesn't exist
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            token=token,
            private=private,
            exist_ok=True
        )
        print(f"✓ Repository created/verified: {repo_id}")
    except Exception as e:
        print(f"Error creating repository: {e}")
        return False

    data_dir = Path(data_dir)
    readme_path = Path(readme_path)

    # Upload README
    try:
        api.upload_file(
            path_or_fileobj=str(readme_path),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
        print(f"✓ Uploaded README.md")
    except Exception as e:
        print(f"Error uploading README: {e}")
        return False

    # Upload all Parquet files
    print("\nUploading Parquet files...")
    parquet_files = sorted(data_dir.rglob("*.parquet"))

    if not parquet_files:
        print(f"ERROR: No Parquet files found in {data_dir}")
        return False

    print(f"Found {len(parquet_files)} Parquet files to upload")

    for i, file_path in enumerate(parquet_files, 1):
        # Calculate relative path from data_dir
        rel_path = file_path.relative_to(data_dir)

        try:
            api.upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=str(rel_path),
                repo_id=repo_id,
                repo_type="dataset",
                token=token
            )
            print(f"  [{i}/{len(parquet_files)}] ✓ Uploaded {rel_path}")
        except Exception as e:
            print(f"  [{i}/{len(parquet_files)}] ✗ Error uploading {rel_path}: {e}")

    # Upload summary CSV if it exists
    summary_file = data_dir / "dataset_summary.csv"
    if summary_file.exists():
        try:
            api.upload_file(
                path_or_fileobj=str(summary_file),
                path_in_repo="dataset_summary.csv",
                repo_id=repo_id,
                repo_type="dataset",
                token=token
            )
            print(f"\n✓ Uploaded dataset_summary.csv")
        except Exception as e:
            print(f"\nError uploading summary: {e}")

    print(f"\n{'='*60}")
    print(f"✓ Dataset uploaded successfully!")
    print(f"View at: https://huggingface.co/datasets/{repo_id}")
    print(f"{'='*60}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Upload Gov-ZA dataset to Hugging Face Hub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload to your account (you'll be prompted for repo name)
  python upload_to_hf.py

  # Upload to specific repository
  python upload_to_hf.py --repo-id dsfsi/govza-sa-cabinet-statements-sentence-aligned

  # Upload as private dataset
  python upload_to_hf.py --repo-id your-org/dataset-name --private

Note: You must be logged in to Hugging Face CLI first:
  huggingface-cli login
        """
    )
    parser.add_argument(
        '--repo-id',
        default='dsfsi/govza-sa-cabinet-statements-sentence-aligned',
        help='Hugging Face repository ID (default: dsfsi/govza-sa-cabinet-statements-sentence-aligned)'
    )
    parser.add_argument(
        '--data-dir',
        default='./data',
        help='Directory containing prepared Parquet files (default: ./data)'
    )
    parser.add_argument(
        '--readme',
        default='./README.md',
        help='Path to README file (default: ./README.md)'
    )
    parser.add_argument(
        '--token',
        help='Hugging Face API token (optional, uses cached token if not provided)'
    )
    parser.add_argument(
        '--private',
        action='store_true',
        help='Create private repository'
    )

    args = parser.parse_args()

    # Verify files exist
    data_dir = Path(args.data_dir)
    readme_path = Path(args.readme)

    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        print("\nDid you run prepare_dataset.py first?")
        print("  python prepare_dataset.py")
        return

    if not readme_path.exists():
        print(f"ERROR: README not found: {readme_path}")
        return

    # Confirm upload
    print("=" * 60)
    print("Gov-ZA Dataset Upload to Hugging Face")
    print("=" * 60)
    print(f"Repository ID: {args.repo_id}")
    print(f"Data directory: {data_dir}")
    print(f"README: {readme_path}")
    print(f"Private: {args.private}")
    print("=" * 60)

    # Count files
    parquet_count = len(list(data_dir.rglob("*.parquet")))
    print(f"\nFiles to upload: {parquet_count} Parquet files + README")

    response = input("\nProceed with upload? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Upload cancelled.")
        return

    # Upload
    success = upload_dataset(
        repo_id=args.repo_id,
        data_dir=data_dir,
        readme_path=readme_path,
        token=args.token,
        private=args.private
    )

    if success:
        print("\n✓ All done! Your dataset is now available on Hugging Face.")
    else:
        print("\n✗ Upload encountered errors. Please check the messages above.")


if __name__ == '__main__':
    main()
