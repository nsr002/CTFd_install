# 🇹🇭 แก้ปัญหาภาษาไทยแสดงผลเพี้ยนใน CSV Import/Export ของ CTFd

## 📌 ปัญหา (Problem)

เมื่อใช้ CTFd Export/Import โจทย์ในรูปแบบ CSV ที่มีภาษาไทย จะพบปัญหา:
- ภาษาไทยแสดงผลเพี้ยน (เป็นอักขระพิเศษแปลกๆ)
- ไฟล์ CSV ที่ Export ออกมาเปิดด้วย Excel แสดงภาษาไทยผิด
- Import ไฟล์ CSV ที่มีภาษาไทยเข้าไปแล้วข้อมูลเพี้ยน

## 🔍 สาเหตุ (Root Cause)

ปัญหาเกิดจากการ encode/decode CSV ไม่ถูกต้อง:
1. **Export:** ไม่ได้ใช้ UTF-8 with BOM (Byte Order Mark) ทำให้ Excel อ่านไม่ถูก
2. **Import:** ไม่ได้รองรับการอ่าน UTF-8 with BOM ทำให้ภาษาไทยผิดเพี้ยน

## ✅ วิธีแก้ไข (Solution)

### วิธีที่ 1: ใช้ Python Script (แนะนำ)

เราได้สร้าง Python utility script ที่รองรับภาษาไทยอย่างสมบูรณ์

1. **คัดลอกไฟล์** `thai_csv_utils.py` ไปที่ CTFd installation directory:
```bash
sudo cp thai_csv_utils.py /var/www/CTFd/CTFd/utils/
sudo chown ctfd:ctfd /var/www/CTFd/CTFd/utils/thai_csv_utils.py
```

2. **แก้ไขไฟล์ Export** ใน CTFd (ตัวอย่างสำหรับ `/var/www/CTFd/CTFd/api/v1/challenges.py`):

```python
# เพิ่ม import
from CTFd.utils.thai_csv_utils import ThaiCSVWriter

# ใน function export_challenges():
@challenges_namespace.route("/export/csv")
class ChallengeExportCSV(Resource):
    @check_challenge_visibility
    def get(self):
        # ใช้ ThaiCSVWriter แทน csv.writer ปกติ
        writer = ThaiCSVWriter()
        
        writer.writerow(['id', 'name', 'description', 'category', 'value', 'state'])
        
        challenges = Challenges.query.all()
        for challenge in challenges:
            writer.writerow([
                challenge.id,
                challenge.name,
                challenge.description,
                challenge.category,
                challenge.value,
                challenge.state
            ])
        
        # Return CSV with proper encoding
        csv_data = writer.getvalue_str()
        return Response(
            csv_data,
            mimetype='text/csv; charset=utf-8',
            headers={
                'Content-Disposition': 'attachment; filename=challenges.csv'
            }
        )
```

3. **แก้ไขไฟล์ Import** ใน CTFd:

```python
# เพิ่ม import
from CTFd.utils.thai_csv_utils import ThaiCSVReader

# ใน function import_challenges():
@challenges_namespace.route("/import/csv")
class ChallengeImportCSV(Resource):
    @admins_only
    def post(self):
        csv_file = request.files['file']
        csv_data = csv_file.read()
        
        # ใช้ ThaiCSVReader แทน csv.reader ปกติ
        reader = ThaiCSVReader(csv_data)
        
        # Skip header
        next(reader)
        
        for row in reader:
            challenge = Challenges(
                name=row[1],
                description=row[2],
                category=row[3],
                value=int(row[4]),
                state=row[5]
            )
            db.session.add(challenge)
        
        db.session.commit()
        return {"success": True}
```

### วิธีที่ 2: ใช้ Patch Files

ถ้าต้องการแก้ไขโดยตรงด้วย patch:

```bash
# 1. ไปที่ directory ของ CTFd
cd /var/www/CTFd

# 2. Apply export patch
sudo -u ctfd patch -p1 < /path/to/thai_csv_fix_export.patch

# 3. Apply import patch
sudo -u ctfd patch -p1 < /path/to/thai_csv_fix_import.patch

# 4. Restart CTFd
sudo systemctl restart ctfd
```

## 🧪 ทดสอบการทำงาน (Testing)

### ทดสอบด้วย Python Script

```bash
# รัน script ทดสอบ
cd /home/runner/work/CTFd_install/CTFd_install
python3 thai_csv_utils.py
```

ผลลัพธ์ที่ได้ควรแสดงภาษาไทยถูกต้อง:

```
=== Testing Export ===
ชื่อโจทย์,คำอธิบาย,หมวดหมู่,คะแนน,สถานะ
โจทย์ทดสอบ 1,คำอธิบายโจทย์เป็นภาษาไทย,Web,100,visible
โจทย์ทดสอบ 2,ทดสอบการเข้ารหัส UTF-8 กับภาษาไทย,Crypto,200,visible

=== Testing Import ===
Challenge 1:
  Name: โจทย์ทดสอบ 1
  Description: คำอธิบายโจทย์เป็นภาษาไทย
  Category: Web
  Value: 100
```

### ทดสอบใน CTFd

1. **Export Test:**
   - เข้า CTFd Admin Panel
   - ไปที่ Challenges > Export
   - เลือก CSV format
   - ดาวน์โหลดไฟล์ CSV
   - เปิดด้วย Excel → ภาษาไทยต้องแสดงถูกต้อง ✅

2. **Import Test:**
   - สร้างไฟล์ CSV ที่มีภาษาไทย (บันทึกเป็น UTF-8 with BOM)
   - เข้า CTFd Admin Panel
   - ไปที่ Challenges > Import
   - Upload ไฟล์ CSV
   - ตรวจสอบโจทย์ที่ Import → ภาษาไทยต้องแสดงถูกต้อง ✅

## 🔧 รายละเอียดทางเทคนิค (Technical Details)

### การใช้ UTF-8 with BOM

```python
import codecs
import io

# สำหรับ Export
output = io.BytesIO()
output.write(codecs.BOM_UTF8)  # เพิ่ม BOM
text_wrapper = io.TextIOWrapper(output, encoding='utf-8', newline='')
writer = csv.writer(text_wrapper)

# สำหรับ Import
if csv_data.startswith(codecs.BOM_UTF8):
    csv_data = csv_data[len(codecs.BOM_UTF8):]  # ลบ BOM ออก
csv_data = csv_data.decode('utf-8')
```

### ทำไมต้องใช้ BOM?

- **BOM (Byte Order Mark)** คือ special marker ที่บอก Excel ว่าไฟล์นี้เป็น UTF-8
- Windows Excel ต้องการ BOM เพื่ออ่านภาษาไทยได้ถูกต้อง
- `0xEF 0xBB 0xBF` = UTF-8 BOM bytes

### Encoding Flow

```
Export: ข้อมูล → UTF-8 → เพิ่ม BOM → CSV file → Excel อ่านได้ ✅
Import: CSV file → ตรวจสอบ BOM → ลบ BOM → UTF-8 → ข้อมูล ✅
```

## 📚 ไฟล์ที่เกี่ยวข้อง (Related Files)

1. **thai_csv_utils.py** - Python utility สำหรับจัดการ CSV ภาษาไทย
2. **thai_csv_fix_export.patch** - Patch สำหรับแก้ Export
3. **thai_csv_fix_import.patch** - Patch สำหรับแก้ Import
4. **THAI_CSV_FIX.md** - เอกสารนี้

## ⚠️ ข้อควรระวัง (Warnings)

1. **Backup ข้อมูลก่อนแก้ไข**: สำรองฐานข้อมูลและไฟล์ CTFd ก่อนทำการแก้ไข
2. **ทดสอบก่อน Deploy**: ทดสอบใน development environment ก่อน
3. **Version ของ CTFd**: Solution นี้ทดสอบกับ CTFd v3.x ถ้าใช้ version อื่นอาจต้องปรับแต่ง

## 🎯 สรุป (Summary)

การแก้ไขนี้จะทำให้ CTFd รองรับภาษาไทยอย่างสมบูรณ์:
- ✅ Export CSV ภาษาไทยแสดงผลถูกต้องใน Excel
- ✅ Import CSV ภาษาไทยเข้าระบบได้โดยไม่เพี้ยน
- ✅ ใช้ UTF-8 with BOM standard
- ✅ รองรับทั้ง Python 3.x

## 📞 ติดต่อและรายงานปัญหา

หากพบปัญหาหรือมีคำถาม กรุณาสร้าง Issue ใน GitHub repository นี้
