#!/bin/bash

echo "==========================================================================="
echo "🔍 Final Validation of Thai CSV Fix"
echo "==========================================================================="
echo ""

# Check all required files exist
echo "📂 Checking Files..."
files=(
    "thai_csv_utils.py"
    "thai_csv_fix_export.patch"
    "thai_csv_fix_import.patch"
    "THAI_CSV_FIX.md"
    "THAI_CSV_README.md"
    "INTEGRATION_EXAMPLE.md"
    "BEFORE_AFTER.md"
    "INDEX.md"
    "comprehensive_test.py"
    "test_import_csv.py"
    "create_sample_csv.py"
    "sample_challenges_thai.csv"
)

all_present=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
        all_present=false
    fi
done
echo ""

# Run Python validation
echo "🐍 Running Python Tests..."
if python3 thai_csv_utils.py > /dev/null 2>&1; then
    echo "  ✅ thai_csv_utils.py - Works correctly"
else
    echo "  ❌ thai_csv_utils.py - Has errors"
    all_present=false
fi

if python3 comprehensive_test.py > /dev/null 2>&1; then
    echo "  ✅ comprehensive_test.py - All tests pass"
else
    echo "  ❌ comprehensive_test.py - Tests failed"
    all_present=false
fi

if python3 test_import_csv.py > /dev/null 2>&1; then
    echo "  ✅ test_import_csv.py - Import test passes"
else
    echo "  ❌ test_import_csv.py - Import test failed"
    all_present=false
fi
echo ""

# Check CSV file has BOM
echo "🔬 Checking CSV Encoding..."
if xxd sample_challenges_thai.csv | head -1 | grep -q "efbb bf"; then
    echo "  ✅ sample_challenges_thai.csv has UTF-8 BOM"
else
    echo "  ❌ sample_challenges_thai.csv missing BOM"
    all_present=false
fi
echo ""

# Count Thai characters in sample
echo "📊 Checking Thai Content..."
thai_count=$(grep -o '[ก-๙]' sample_challenges_thai.csv | wc -l)
if [ "$thai_count" -gt 50 ]; then
    echo "  ✅ Sample CSV contains $thai_count Thai characters"
else
    echo "  ⚠️  Sample CSV only has $thai_count Thai characters"
fi
echo ""

# Final summary
echo "==========================================================================="
if [ "$all_present" = true ]; then
    echo "✅ VALIDATION PASSED - All files present and working!"
    echo ""
    echo "📦 Solution is ready for deployment"
    echo "📖 Start with INDEX.md or THAI_CSV_README.md"
else
    echo "❌ VALIDATION FAILED - Some issues detected"
fi
echo "==========================================================================="
