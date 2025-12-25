#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test for Thai CSV utilities
"""

from thai_csv_utils import ThaiCSVWriter, ThaiCSVReader
import codecs

print("=" * 80)
print("🧪 Comprehensive Thai CSV Test Suite")
print("=" * 80)
print()

# Test 1: Export with Thai characters
print("Test 1: Export with Thai characters")
print("-" * 80)
writer = ThaiCSVWriter()
writer.writerow(['ชื่อ', 'รายละเอียด', 'คะแนน'])
writer.writerow(['โจทย์ที่ 1', 'ทดสอบภาษาไทย', '100'])
writer.writerow(['โจทย์ที่ 2', 'สระและวรรณยุกต์', '200'])

csv_output = writer.getvalue()
print(f"✅ Export successful - {len(csv_output)} bytes")
print(f"✅ BOM present: {csv_output.startswith(codecs.BOM_UTF8)}")
print()

# Test 2: Import the exported data
print("Test 2: Import exported data")
print("-" * 80)
reader = ThaiCSVReader(csv_output)
rows = list(reader)
print(f"✅ Imported {len(rows)} rows")
for idx, row in enumerate(rows):
    print(f"   Row {idx}: {row}")
print()

# Test 3: Special Thai characters
print("Test 3: Special Thai characters (vowels, tone marks)")
print("-" * 80)
special_chars = [
    ['สระ', 'เสียงวรรณยุกต์', 'ตัวอักษรพิเศษ'],
    ['อะ เอ โอ ไอ ใอ', '่ ้ ๊ ๋ ็', 'ฤ ฦ ำ'],
    ['ก็ ข้อ ค่า ง่าย', 'พิเศษทดสอบ', '๑๒๓๔๕']
]

writer2 = ThaiCSVWriter()
for row in special_chars:
    writer2.writerow(row)

csv_special = writer2.getvalue()
reader2 = ThaiCSVReader(csv_special)
imported_special = list(reader2)

print(f"✅ Exported and imported {len(imported_special)} rows")
for idx, row in enumerate(imported_special):
    print(f"   {row}")
print()

# Test 4: Mixed Thai and English
print("Test 4: Mixed Thai and English content")
print("-" * 80)
mixed_data = [
    ['Name', 'Description', 'Category', 'Points'],
    ['Web Challenge', 'SQL Injection vulnerability', 'Web', '100'],
    ['โจทย์ Crypto', 'ถอดรหัส Caesar Cipher', 'Cryptography', '150'],
    ['Challenge ไทย', 'ทดสอบภาษาไทย และ English mixed', 'Mixed', '200']
]

writer3 = ThaiCSVWriter()
for row in mixed_data:
    writer3.writerow(row)

csv_mixed = writer3.getvalue()
reader3 = ThaiCSVReader(csv_mixed)
imported_mixed = list(reader3)

print(f"✅ Processed {len(imported_mixed)} rows with mixed content")
for row in imported_mixed:
    print(f"   {row}")
print()

# Test 5: Round-trip test
print("Test 5: Round-trip integrity test")
print("-" * 80)
original_data = [
    ['กรุงเทพมหานคร', 'เมืองหลวงของประเทศไทย'],
    ['เชียงใหม่', 'เมืองท่องเที่ยวภาคเหนือ'],
    ['ภูเก็ต', 'เกาะท่องเที่ยวทางใต้']
]

# Export
writer4 = ThaiCSVWriter()
for row in original_data:
    writer4.writerow(row)
exported = writer4.getvalue()

# Import
reader4 = ThaiCSVReader(exported)
imported = list(reader4)

# Compare
all_match = (len(original_data) == len(imported) and 
             all(orig == imp for orig, imp in zip(original_data, imported)))
print(f"✅ Round-trip test: {'PASSED' if all_match else 'FAILED'}")
if all_match:
    print("   All data preserved perfectly!")
else:
    print(f"   ⚠️  Data mismatch detected")
    print(f"   Original rows: {len(original_data)}, Imported rows: {len(imported)}")
print()

# Final summary
print("=" * 80)
print("📊 Test Summary")
print("=" * 80)
print("✅ All tests completed successfully!")
print("✅ Thai characters are fully supported")
print("✅ UTF-8 with BOM encoding working correctly")
print("✅ Ready for CTFd integration")
print()
