#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CTFd Thai Language CSV Encoding Fix
====================================

This script provides utilities to fix Thai language encoding issues
when importing/exporting CSV files in CTFd.

Thai characters require UTF-8 encoding with BOM (Byte Order Mark) to display
correctly in Excel and other CSV readers.
"""

import csv
import io
import codecs
from typing import List, Dict, Any


class ThaiCSVWriter:
    """
    CSV Writer that properly handles Thai characters using UTF-8 with BOM
    """
    
    def __init__(self):
        """Initialize the writer with UTF-8 BOM encoding"""
        self.output = io.BytesIO()
        # Write BOM at the beginning for Excel compatibility
        self.output.write(codecs.BOM_UTF8)
        self.text_wrapper = io.TextIOWrapper(
            self.output, 
            encoding='utf-8', 
            newline='',
            write_through=True
        )
        self.writer = csv.writer(self.text_wrapper, dialect='excel')
    
    def writerow(self, row: List[Any]):
        """Write a single row to CSV"""
        self.writer.writerow(row)
    
    def writerows(self, rows: List[List[Any]]):
        """Write multiple rows to CSV"""
        self.writer.writerows(rows)
    
    def getvalue(self) -> bytes:
        """Get the CSV content as bytes"""
        self.text_wrapper.flush()
        self.output.seek(0)
        return self.output.read()
    
    def getvalue_str(self) -> str:
        """Get the CSV content as UTF-8 string"""
        return self.getvalue().decode('utf-8')


class ThaiCSVReader:
    """
    CSV Reader that properly handles Thai characters from UTF-8 with BOM
    """
    
    def __init__(self, csv_data: Any):
        """
        Initialize the reader with automatic encoding detection
        
        Args:
            csv_data: Can be bytes, string, or file object
        """
        # Handle different input types
        if isinstance(csv_data, bytes):
            # Remove BOM if present
            if csv_data.startswith(codecs.BOM_UTF8):
                csv_data = csv_data[len(codecs.BOM_UTF8):]
            csv_data = csv_data.decode('utf-8')
        elif isinstance(csv_data, str):
            # Remove BOM character if present in string
            if csv_data.startswith('\ufeff'):
                csv_data = csv_data[1:]
        
        self.stream = io.StringIO(csv_data)
        self.reader = csv.reader(self.stream, dialect='excel')
    
    def __iter__(self):
        """Make the reader iterable"""
        return self.reader
    
    def __next__(self):
        """Get next row"""
        return next(self.reader)


def export_challenges_to_csv(challenges: List[Dict[str, Any]]) -> str:
    """
    Export challenges to CSV format with proper Thai encoding
    
    Args:
        challenges: List of challenge dictionaries
        
    Returns:
        CSV string with UTF-8 BOM encoding
    """
    writer = ThaiCSVWriter()
    
    # Write header
    writer.writerow([
        'ชื่อโจทย์',  # Challenge name
        'คำอธิบาย',  # Description
        'หมวดหมู่',  # Category
        'คะแนน',      # Points
        'สถานะ',      # State
    ])
    
    # Write challenge data
    for challenge in challenges:
        writer.writerow([
            challenge.get('name', ''),
            challenge.get('description', ''),
            challenge.get('category', ''),
            challenge.get('value', 0),
            challenge.get('state', 'visible'),
        ])
    
    return writer.getvalue_str()


def import_challenges_from_csv(csv_data: Any) -> List[Dict[str, Any]]:
    """
    Import challenges from CSV format with proper Thai encoding
    
    Args:
        csv_data: CSV data as bytes, string, or file object
        
    Returns:
        List of challenge dictionaries
    """
    reader = ThaiCSVReader(csv_data)
    challenges = []
    
    # Skip header
    try:
        next(reader)
    except StopIteration:
        return challenges
    
    # Read challenge data
    for row in reader:
        if len(row) >= 5:
            # Parse value with proper error handling
            try:
                value = int(row[3]) if row[3] else 0
            except (ValueError, IndexError):
                value = 0
            
            challenge = {
                'name': row[0],
                'description': row[1],
                'category': row[2],
                'value': value,
                'state': row[4] if row[4] else 'visible',
            }
            challenges.append(challenge)
    
    return challenges


# Example usage
if __name__ == '__main__':
    # Test with Thai characters
    test_challenges = [
        {
            'name': 'โจทย์ทดสอบ 1',
            'description': 'คำอธิบายโจทย์เป็นภาษาไทย',
            'category': 'Web',
            'value': 100,
            'state': 'visible'
        },
        {
            'name': 'โจทย์ทดสอบ 2',
            'description': 'ทดสอบการเข้ารหัส UTF-8 กับภาษาไทย',
            'category': 'Crypto',
            'value': 200,
            'state': 'visible'
        }
    ]
    
    # Export to CSV
    print("=== Testing Export ===")
    csv_output = export_challenges_to_csv(test_challenges)
    print(csv_output)
    print()
    
    # Import from CSV
    print("=== Testing Import ===")
    imported = import_challenges_from_csv(csv_output)
    for idx, challenge in enumerate(imported, 1):
        print(f"Challenge {idx}:")
        print(f"  Name: {challenge['name']}")
        print(f"  Description: {challenge['description']}")
        print(f"  Category: {challenge['category']}")
        print(f"  Value: {challenge['value']}")
        print()
