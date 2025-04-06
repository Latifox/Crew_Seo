#!/bin/bash
# Cleanup script for CrewAI SEO Production project
# This script removes test files, debug scripts, and other unnecessary files

echo "Starting project cleanup..."

# Remove test files
echo "Removing test files..."
rm -f test_*.py
rm -f *_test.py

# Remove debug and fix scripts
echo "Removing debug and fix scripts..."
rm -f debug_*.py
rm -f fix_*.py
rm -f *_fixed.py
rm -f upgrade_crewai.py

# Remove simple example files
echo "Removing simple example files..."
rm -f simple_*.py

# Remove duplicate runner scripts (keeping only the main ones)
echo "Removing duplicate runner scripts..."
rm -f run_*_fixed.py
rm -f run_*_direct.py
rm -f run_direct_*.py
rm -f run_combined_*.py
rm -f run_enhanced_*.py
rm -f run_seo_production_*.py
rm -f run_keyword_task.py
rm -f run_content_creation.py

# Keep only essential runner scripts
FILES_TO_KEEP="run_complete_seo_production.py run_seo_agency.py"
for file in run_*.py; do
    if ! echo "$FILES_TO_KEEP" | grep -q "$file"; then
        echo "Removing $file..."
        rm -f "$file"
    fi
done

# Remove log files
echo "Removing log files..."
rm -f *.log

# Remove Python cache directories
echo "Removing Python cache..."
find . -name "__pycache__" -type d -exec rm -rf {} +

# Remove example directory if empty
echo "Checking examples directory..."
if [ -z "$(ls -A examples 2>/dev/null)" ]; then
    echo "Removing empty examples directory..."
    rmdir examples
fi

# Remove reports directory if empty
echo "Checking reports directory..."
if [ -z "$(ls -A reports 2>/dev/null)" ]; then
    echo "Removing empty reports directory..."
    rmdir reports
fi

# Remove generated test data script
echo "Removing test data generator..."
rm -f generate_test_data.py

echo "Cleanup complete!"
echo "Remaining files:"
ls -la