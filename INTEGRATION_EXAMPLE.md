# Integration Example for CTFd

This file shows how to integrate the Thai CSV fix into CTFd's actual codebase.

## File: CTFd/api/v1/challenges.py

### Before (Original Code - with Thai encoding issues):

```python
from flask import Response
from flask_restx import Resource
import csv
import io

@challenges_namespace.route("/export/csv")
class ChallengeExportCSV(Resource):
    @check_challenge_visibility
    def get(self):
        """Export challenges as CSV"""
        # PROBLEM: Using StringIO without UTF-8 BOM
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['id', 'name', 'description', 'category', 'value'])
        
        challenges = Challenges.query.all()
        for challenge in challenges:
            writer.writerow([
                challenge.id,
                challenge.name,
                challenge.description,
                challenge.category,
                challenge.value
            ])
        
        # PROBLEM: No UTF-8 BOM, Thai characters will be corrupted
        csv_data = output.getvalue()
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=challenges.csv'}
        )
```

### After (Fixed Code - with Thai support):

```python
from flask import Response
from flask_restx import Resource
from CTFd.utils.thai_csv_utils import ThaiCSVWriter  # ADD THIS IMPORT

@challenges_namespace.route("/export/csv")
class ChallengeExportCSV(Resource):
    @check_challenge_visibility
    def get(self):
        """Export challenges as CSV with Thai language support"""
        # FIX: Use ThaiCSVWriter instead of regular csv.writer
        writer = ThaiCSVWriter()
        
        writer.writerow(['id', 'name', 'description', 'category', 'value'])
        
        challenges = Challenges.query.all()
        for challenge in challenges:
            writer.writerow([
                challenge.id,
                challenge.name,
                challenge.description,
                challenge.category,
                challenge.value
            ])
        
        # FIX: Get UTF-8 with BOM encoded string
        csv_data = writer.getvalue_str()
        return Response(
            csv_data,
            mimetype='text/csv; charset=utf-8',  # FIX: Specify UTF-8
            headers={'Content-Disposition': 'attachment; filename=challenges.csv'}
        )
```

## File: CTFd/api/v1/challenges.py (Import)

### Before (Original Code - with Thai encoding issues):

```python
from flask import request
from flask_restx import Resource
import csv
import io

@challenges_namespace.route("/import/csv")
class ChallengeImportCSV(Resource):
    @admins_only
    def post(self):
        """Import challenges from CSV"""
        csv_file = request.files['file']
        
        # PROBLEM: Not handling UTF-8 BOM
        csv_data = csv_file.read().decode('utf-8')
        stream = io.StringIO(csv_data)
        reader = csv.reader(stream)
        
        # Skip header
        next(reader)
        
        for row in reader:
            # PROBLEM: Thai characters may be corrupted here
            challenge = Challenges(
                name=row[1],
                description=row[2],
                category=row[3],
                value=int(row[4])
            )
            db.session.add(challenge)
        
        db.session.commit()
        return {"success": True}
```

### After (Fixed Code - with Thai support):

```python
from flask import request
from flask_restx import Resource
from CTFd.utils.thai_csv_utils import ThaiCSVReader  # ADD THIS IMPORT

@challenges_namespace.route("/import/csv")
class ChallengeImportCSV(Resource):
    @admins_only
    def post(self):
        """Import challenges from CSV with Thai language support"""
        csv_file = request.files['file']
        
        # FIX: Read as bytes first
        csv_data = csv_file.read()
        
        # FIX: Use ThaiCSVReader which handles UTF-8 BOM automatically
        reader = ThaiCSVReader(csv_data)
        
        # Skip header
        next(reader)
        
        for row in reader:
            # FIX: Thai characters are now preserved correctly
            challenge = Challenges(
                name=row[1],
                description=row[2],
                category=row[3],
                value=int(row[4])
            )
            db.session.add(challenge)
        
        db.session.commit()
        return {"success": True}
```

## Summary of Changes

### Key Points:
1. **Import ThaiCSVWriter and ThaiCSVReader** from `CTFd.utils.thai_csv_utils`
2. **Replace csv.writer** with `ThaiCSVWriter`
3. **Replace csv.reader** with `ThaiCSVReader`
4. **Read file as bytes** for import (not as string)
5. **Use getvalue_str()** for export to get UTF-8 string
6. **Specify charset** in Content-Type header

### Benefits:
- ✅ Thai characters display correctly in Excel
- ✅ No more corrupted Thai text
- ✅ UTF-8 with BOM standard compliance
- ✅ Works on Windows, Mac, and Linux
- ✅ Compatible with Excel, LibreOffice, Google Sheets

## Testing

After making these changes:

1. Start CTFd: `sudo systemctl restart ctfd`
2. Login as admin
3. Create a challenge with Thai name/description
4. Export to CSV and open in Excel → Should display correctly
5. Import a CSV with Thai content → Should save correctly

## Minimal Change Approach

These changes are minimal and focused:
- Only 2 imports added
- Only 2 class replacements (writer and reader)
- No changes to business logic
- No changes to database schema
- Backward compatible with existing English content
