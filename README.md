# AI Inventory Studio V3

This is the first full V3 package.

## What it does

1. Upload vendor inventory CSV/XLSX
2. Enter English instructions
3. Analyze columns against accepted headers
4. Review/edit mapping
5. Create normalized input
6. Create expanded inventory
7. Generate QA report
8. Download CSV/XLSX/config/report

## Folder structure

configs/headers/
- jewelry.csv
- diamond.csv
- lab-grown.csv

These files should contain:
- Setter name
- Header variations

## Important

This V3 package includes a starter expansion engine in `core/expander.py`.

Later, we can replace that module with your original production inventory
expansion logic while keeping the AI Studio UI and agent workflow.
