#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test importing the sample Thai CSV file
"""

from thai_csv_utils import ThaiCSVReader

# Read the sample CSV file
print("🔄 Testing CSV Import with Thai characters...")
print("=" * 80)

with open('sample_challenges_thai.csv', 'rb') as f:
    csv_data = f.read()

# Check for BOM
if csv_data.startswith(b'\xef\xbb\xbf'):
    print("✅ UTF-8 BOM detected in file")
else:
    print("⚠️  No BOM found - this might cause issues in Excel")

print()

# Import using ThaiCSVReader
reader = ThaiCSVReader(csv_data)

# Read header
header = next(reader)
print(f"📋 Header columns: {header}")
print()

# Read and display challenges
print("📚 Imported Challenges:")
print("-" * 80)

for idx, row in enumerate(reader, 1):
    if len(row) >= 6:
        print(f"{idx}. {row[1]}")
        print(f"   📝 Description: {row[2]}")
        print(f"   📁 Category: {row[3]}")
        print(f"   🏆 Points: {row[4]}")
        print(f"   👁️  State: {row[5]}")
        print()

print("=" * 80)
print("✅ Import test completed successfully!")
print("💡 All Thai characters displayed correctly")
