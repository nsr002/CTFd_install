# 🔧 CTFd Thai CSV Fix - Quick Installation Guide

## 🚀 Quick Start (แบบใช้งานเร็ว)

### สำหรับผู้ดูแลระบบ CTFd ที่ต้องการแก้ปัญหาภาษาไทยเพี้ยนใน CSV

1. **ดาวน์โหลดไฟล์**
```bash
cd /tmp
git clone https://github.com/nsr002/CTFd_install.git
cd CTFd_install
```

2. **คัดลอก utility ไปยัง CTFd**
```bash
# คัดลอก thai_csv_utils.py ไปที่ CTFd
sudo cp thai_csv_utils.py /var/www/CTFd/CTFd/utils/
sudo chown ctfd:ctfd /var/www/CTFd/CTFd/utils/thai_csv_utils.py
```

3. **แก้ไขไฟล์ CTFd ที่เกี่ยวข้อง**

ดูรายละเอียดการแก้ไขใน `THAI_CSV_FIX.md`

4. **Restart CTFd**
```bash
sudo systemctl restart ctfd
```

## 📦 ไฟล์ที่มีให้

| ไฟล์ | คำอธิบาย |
|------|----------|
| `thai_csv_utils.py` | Python utility สำหรับจัดการ CSV ภาษาไทย (ใช้ใน CTFd) |
| `THAI_CSV_FIX.md` | คู่มือแก้ไขปัญหาแบบละเอียด (ภาษาไทย) |
| `thai_csv_fix_export.patch` | Patch สำหรับแก้ Export function |
| `thai_csv_fix_import.patch` | Patch สำหรับแก้ Import function |
| `create_sample_csv.py` | Script สร้างไฟล์ CSV ตัวอย่าง |
| `test_import_csv.py` | Script ทดสอบการ Import |
| `sample_challenges_thai.csv` | ไฟล์ CSV ตัวอย่างภาษาไทย |

## ✅ ทดสอบว่าใช้งานได้

```bash
# ทดสอบการทำงานของ utility
python3 thai_csv_utils.py

# สร้างไฟล์ CSV ตัวอย่าง
python3 create_sample_csv.py

# ทดสอบการ Import
python3 test_import_csv.py
```

## 🎯 ผลลัพธ์ที่ได้

- ✅ Export CSV จาก CTFd ภาษาไทยแสดงผลถูกต้องใน Excel
- ✅ Import CSV ที่มีภาษาไทยเข้า CTFd ได้โดยไม่เพี้ยน
- ✅ รองรับ UTF-8 with BOM standard
- ✅ เข้ากันได้กับทั้ง Windows Excel และ LibreOffice Calc

## 📖 เอกสารเพิ่มเติม

อ่านเอกสารแบบละเอียดได้ที่: [THAI_CSV_FIX.md](THAI_CSV_FIX.md)

## 🐛 รายงานปัญหา

หากพบปัญหาหรือข้อผิดพลาด กรุณาสร้าง Issue ใน GitHub

## 📝 License

MIT License - ใช้งานได้อย่างอิสระ
