# Hugging Face Dataset Preparation Instructions

This directory contains scripts to prepare and upload the Gov-ZA Cabinet Statements dataset to Hugging Face Hub.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Prepare the dataset (convert JSONL to Parquet with splits)
python prepare_dataset.py

# 3. Login to Hugging Face
huggingface-cli login

# 4. Upload to Hugging Face
python upload_to_hf.py --repo-id dsfsi/govza-sa-cabinet-statements-sentence-aligned
```

## Directory Structure

```
huggingface_dataset/
├── INSTRUCTIONS.md          # This file
├── README.md               # Hugging Face dataset card (will be uploaded)
├── requirements.txt        # Python dependencies
├── prepare_dataset.py      # Script to convert data to Parquet
├── upload_to_hf.py        # Script to upload to Hugging Face
└── data/                  # Generated Parquet files (created by prepare_dataset.py)
    ├── afr-eng/
    │   ├── train/
    │   │   └── 0000.parquet
    │   ├── test/
    │   │   └── 0000.parquet
    │   └── eval/
    │       └── 0000.parquet
    ├── afr-nbl/
    │   └── [same structure]
    └── ... [55 language pair directories]
```

## Detailed Steps

### Step 1: Install Dependencies

```bash
cd huggingface_dataset
pip install -r requirements.txt
```

**Dependencies:**
- `pandas` - Data manipulation
- `scikit-learn` - Train/test/eval splitting
- `pyarrow` - Parquet file support
- `datasets` - Hugging Face datasets library
- `huggingface-hub` - Upload to HF Hub

### Step 2: Prepare the Dataset

The `prepare_dataset.py` script converts the sentence-aligned JSONL files into Parquet format with train/test/eval splits.

**Basic usage:**

```bash
python prepare_dataset.py
```

**Advanced options:**

```bash
python prepare_dataset.py \
  --input-dir ../data/opt_aligned_out \
  --output-dir ./data \
  --test-size 0.15 \
  --eval-size 0.15
```

**Parameters:**
- `--input-dir`: Directory with aligned JSONL files (default: `../data/opt_aligned_out`)
- `--output-dir`: Where to save Parquet files (default: `./data`)
- `--test-size`: Proportion for test set (default: 0.15 = 15%)
- `--eval-size`: Proportion for eval set (default: 0.15 = 15%)

**What it does:**
1. Reads all `aligned-{lang1}-{lang2}.jsonl` files
2. For each language pair:
   - Loads the aligned sentence pairs
   - Renames columns to language codes (e.g., `src` → `afr`, `tgt` → `eng`)
   - Splits into train (70%), test (15%), eval (15%)
   - Saves as Parquet files in `{lang1}-{lang2}/{split}/0000.parquet`
3. Creates a summary CSV with statistics

**Output:**
```
Processing afr-eng...
  Loaded 16385 aligned sentence pairs
  Split: train=11469, test=2458, eval=2458
  Saved train: data/afr-eng/train/0000.parquet
  Saved test: data/afr-eng/test/0000.parquet
  Saved eval: data/afr-eng/eval/0000.parquet
...
```

### Step 3: Login to Hugging Face

You need to authenticate with Hugging Face to upload datasets.

**Option 1: Using CLI** (recommended)

```bash
huggingface-cli login
```

This will prompt you to enter your Hugging Face token. Get your token from:
https://huggingface.co/settings/tokens

**Option 2: Using environment variable**

```bash
export HUGGING_FACE_HUB_TOKEN=your_token_here
```

**Option 3: Pass token to script**

```bash
python upload_to_hf.py --token your_token_here
```

### Step 4: Upload to Hugging Face

The `upload_to_hf.py` script uploads the prepared dataset to Hugging Face Hub.

**Basic usage:**

```bash
python upload_to_hf.py --repo-id dsfsi/govza-sa-cabinet-statements-sentence-aligned
```

**Advanced options:**

```bash
python upload_to_hf.py \
  --repo-id your-org/dataset-name \
  --data-dir ./data \
  --readme ./README.md \
  --private
```

**Parameters:**
- `--repo-id`: Hugging Face repository ID (e.g., `dsfsi/govza-sa-cabinet-statements`)
- `--data-dir`: Directory with Parquet files (default: `./data`)
- `--readme`: Path to README file (default: `./README.md`)
- `--token`: HF token (optional if you used `huggingface-cli login`)
- `--private`: Create a private repository

**What it does:**
1. Creates the repository if it doesn't exist
2. Uploads README.md as the dataset card
3. Uploads all Parquet files maintaining directory structure
4. Uploads the summary CSV

**Output:**
```
✓ Repository created/verified: dsfsi/govza-sa-cabinet-statements-sentence-aligned
✓ Uploaded README.md

Uploading Parquet files...
Found 165 Parquet files to upload
  [1/165] ✓ Uploaded afr-eng/train/0000.parquet
  [2/165] ✓ Uploaded afr-eng/test/0000.parquet
  ...
✓ Uploaded dataset_summary.csv

✓ Dataset uploaded successfully!
View at: https://huggingface.co/datasets/dsfsi/govza-sa-cabinet-statements-sentence-aligned
```

### Step 5: Upload the Dataset Loading Script

**IMPORTANT:** After uploading the data, you must also upload the dataset loading script to make all 55 language pairs visible.

The dataset loading script (`govza-sa-cabinet-statements-sentence-aligned.py`) tells Hugging Face how to load and expose all language pair configurations.

**Upload manually via Hugging Face website:**

1. Go to your dataset repository on Hugging Face
2. Click "Files and versions" tab
3. Click "Add file" → "Upload files"
4. Upload `govza-sa-cabinet-statements-sentence-aligned.py` to the root directory
5. Commit the changes

**Or upload via command line:**

```bash
huggingface-cli upload dsfsi/govza-sa-cabinet-statements-sentence-aligned \
  govza-sa-cabinet-statements-sentence-aligned.py \
  --repo-type dataset
```

**Why this is needed:**

Without this script, Hugging Face will only auto-detect one configuration (afr-eng) instead of all 55 language pairs. The script explicitly defines all configurations and enables users to load any language pair:

```python
# Will work after uploading the script:
dataset = load_dataset("dsfsi/govza-sa-cabinet-statements-sentence-aligned", "afr-eng")
dataset = load_dataset("dsfsi/govza-sa-cabinet-statements-sentence-aligned", "xho-zul")
# ... and all other 53 pairs
```

## Dataset Structure

### Language Pairs

The dataset includes 55 language pair combinations:

**Format:** `{lang1}-{lang2}` where both languages are from:
- `afr` (Afrikaans)
- `eng` (English)
- `nbl` (isiNdebele)
- `nso` (Sepedi)
- `sot` (Sesotho)
- `ssw` (Siswati)
- `tsn` (Setswana)
- `tso` (Xitstonga)
- `ven` (Tshivenda)
- `xho` (isiXhosa)
- `zul` (isiZulu)

### Data Format

Each Parquet file contains:

| Column | Type | Description |
|--------|------|-------------|
| `{lang1}` | string | Source language sentence |
| `{lang2}` | string | Target language sentence (aligned) |
| `score` | float | Alignment confidence score (0.0-1.0) |
| `__index_level_0__` | int | Original index |

**Example:**

| afr | eng | score | __index_level_0__ |
|-----|-----|-------|-------------------|
| Die Kabinet het... | Cabinet expressed... | 0.8649 | 2 |

### Splits

Each language pair has three splits:
- **train**: ~70% of data
- **test**: ~15% of data
- **eval**: ~15% of data

## Verification

### Verify Parquet Files

```python
import pandas as pd

# Read a Parquet file
df = pd.read_parquet('data/afr-eng/train/0000.parquet')

print(f"Records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(df.head())
```

### Test Loading with Hugging Face Datasets

```python
from datasets import load_dataset

# Load from local directory (before upload)
dataset = load_dataset('parquet', data_dir='data/afr-eng')
print(dataset)

# After upload, load from Hub
dataset = load_dataset('dsfsi/govza-sa-cabinet-statements-sentence-aligned', 'afr-eng')
print(dataset)
```

## Troubleshooting

### Issue: "No aligned JSONL files found"

**Solution:** Make sure you're running from the `huggingface_dataset` directory and that `../data/opt_aligned_out/` contains the aligned JSONL files.

### Issue: "pyarrow not installed"

**Solution:**
```bash
pip install pyarrow
```

### Issue: "Authentication error" when uploading

**Solution:** Login to Hugging Face:
```bash
huggingface-cli login
```

Or provide token explicitly:
```bash
python upload_to_hf.py --token YOUR_TOKEN
```

### Issue: "Repository already exists"

**Solution:** The script will use the existing repository. If you want to overwrite, you can:
1. Delete the repository on Hugging Face first, or
2. The script will upload/update files (won't duplicate)

### Issue: Files taking long to upload

**Solution:** This is normal. With 55 language pairs × 3 splits = 165 Parquet files, uploading can take time. The script shows progress.

## Dataset Statistics

After running `prepare_dataset.py`, check `data/dataset_summary.csv` for statistics:

```csv
pair,total,train,test,eval
afr-eng,16385,11469,2458,2458
afr-nbl,5154,3607,773,774
...
```

## Next Steps

After uploading:

1. **Verify on Hugging Face**: Visit https://huggingface.co/datasets/dsfsi/govza-sa-cabinet-statements-sentence-aligned

2. **Test loading**:
   ```python
   from datasets import load_dataset
   ds = load_dataset('dsfsi/govza-sa-cabinet-statements-sentence-aligned', 'afr-eng')
   ```

3. **Update dataset card**: Edit README.md on Hugging Face if needed

4. **Add examples**: Consider adding example usage notebooks

## Additional Resources

- **Hugging Face Datasets Docs**: https://huggingface.co/docs/datasets
- **Dataset Cards Guide**: https://huggingface.co/docs/datasets/dataset_card
- **Parquet Format**: https://parquet.apache.org/

## Contact

For questions or issues:
- Open an issue: https://github.com/dsfsi/gov-za-multilingual/issues
- Contact: DSFSI Research Group, University of Pretoria
