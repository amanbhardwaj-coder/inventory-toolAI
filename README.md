Inventory AI Agent V2 DataFrame Fix

This bundle fixes the repeated duplicate-column pandas issue.

Root cause:
df.rename() was creating duplicate column names when multiple vendor columns mapped
to the same accepted header. In pandas, duplicate column selection can return a
DataFrame instead of a Series, which caused .tolist() / .str errors.

Fix:
- create_normalized_file() now builds the normalized dataframe from scratch
- duplicate accepted headers are merged row-by-row
- no duplicate columns are created before Streamlit preview
- unmapped columns are preserved

Also included:
- AI Instructions box remains available
- basic pricing rule extraction for:
  "14k metal prices should be 500 and rest should be 1000"

Note:
The pricing rule is saved in mapping_config.json. Applying it to final expanded
inventory is the next integration step.
