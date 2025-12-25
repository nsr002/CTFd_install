#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create sample Thai CSV files for testing
"""

from thai_csv_utils import ThaiCSVWriter
import os

# Create test data
test_challenges = [
    {
        'name': 'เว็บแอปพลิเคชันพื้นฐาน',
        'description': 'โจทย์นี้เกี่ยวกับช่องโหว่ SQL Injection ในเว็บไซต์',
        'category': 'Web Security',
        'value': 150,
        'state': 'visible'
    },
    {
        'name': 'การเข้ารหัสลับ',
        'description': 'ถอดรหัสข้อความที่เข้ารหัสด้วย Caesar Cipher',
        'category': 'Cryptography',
        'value': 100,
        'state': 'visible'
    },
    {
        'name': 'การวิเคราะห์ไฟล์',
        'description': 'หาข้อมูลที่ซ่อนอยู่ในไฟล์ภาพ PNG',
        'category': 'Forensics',
        'value': 200,
        'state': 'hidden'
    },
    {
        'name': 'Buffer Overflow',
        'description': 'โจทย์เกี่ยวกับการโจมตี Buffer Overflow ในโปรแกรม C',
        'category': 'Binary Exploitation',
        'value': 300,
        'state': 'visible'
    },
    {
        'name': 'การโจมตีเครือข่าย',
        'description': 'วิเคราะห์ packet capture file เพื่อหาข้อมูลสำคัญ',
        'category': 'Network',
        'value': 250,
        'state': 'visible'
    }
]

# Create CSV file
writer = ThaiCSVWriter()

# Write header with Thai column names
writer.writerow([
    'ลำดับ',
    'ชื่อโจทย์',
    'คำอธิบาย',
    'หมวดหมู่',
    'คะแนน',
    'สถานะ'
])

# Write challenge data
for idx, challenge in enumerate(test_challenges, 1):
    writer.writerow([
        idx,
        challenge['name'],
        challenge['description'],
        challenge['category'],
        challenge['value'],
        challenge['state']
    ])

# Save to file
output_file = 'sample_challenges_thai.csv'
with open(output_file, 'wb') as f:
    f.write(writer.getvalue())

print(f"✅ Created sample CSV file: {output_file}")
print(f"📊 Total challenges: {len(test_challenges)}")
print(f"📄 File size: {os.path.getsize(output_file)} bytes")
print()
print("🔍 File preview:")
print("-" * 80)
with open(output_file, 'r', encoding='utf-8-sig') as f:
    content = f.read()
    print(content)
