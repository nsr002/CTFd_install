# 🚀 Deployment Guide - Thai CSV Fix for CTFd

## Overview

This guide will help you deploy the Thai CSV fix to your CTFd installation in production.

## ⏱️ Estimated Time: 10-15 minutes

## Prerequisites

- Root or sudo access to CTFd server
- CTFd already installed (version 3.x recommended)
- Basic knowledge of Linux command line

## 🛠️ Deployment Steps

### Step 1: Backup Your System

**⚠️ CRITICAL: Always backup before making changes!**

```bash
# Backup CTFd directory
sudo tar -czf /backup/ctfd_backup_$(date +%Y%m%d).tar.gz /var/www/CTFd/

# Backup database (if using MariaDB/MySQL)
sudo mysqldump -u ctfd -p ctfd_db > /backup/ctfd_db_$(date +%Y%m%d).sql

# Verify backup exists
ls -lh /backup/
```

### Step 2: Download the Fix

```bash
# Go to temporary directory
cd /tmp

# Clone the repository
git clone https://github.com/nsr002/CTFd_install.git
cd CTFd_install

# Verify files
ls -la *.py *.patch *.md
```

### Step 3: Copy Utility to CTFd

```bash
# Copy the main utility file
sudo cp thai_csv_utils.py /var/www/CTFd/CTFd/utils/

# Set correct ownership
sudo chown ctfd:ctfd /var/www/CTFd/CTFd/utils/thai_csv_utils.py

# Set correct permissions
sudo chmod 644 /var/www/CTFd/CTFd/utils/thai_csv_utils.py

# Verify
ls -l /var/www/CTFd/CTFd/utils/thai_csv_utils.py
```

### Step 4: Locate CTFd API Files

```bash
# Find the challenges API file
find /var/www/CTFd -name "challenges.py" -path "*/api/v1/*"

# Typical location: /var/www/CTFd/CTFd/api/v1/challenges.py
```

### Step 5: Modify Export Function

```bash
# Edit the challenges.py file
sudo -u ctfd nano /var/www/CTFd/CTFd/api/v1/challenges.py
```

**Find the export function** (search for `export` or `csv`):

```python
# ADD THIS IMPORT at the top of the file
from CTFd.utils.thai_csv_utils import ThaiCSVWriter, ThaiCSVReader
```

**Replace the export code:**

```python
# OLD CODE (remove or comment out):
# output = io.StringIO()
# writer = csv.writer(output)

# NEW CODE:
writer = ThaiCSVWriter()
# ... write your rows ...
csv_data = writer.getvalue_str()
```

### Step 6: Modify Import Function

**In the same file, find the import function:**

```python
# OLD CODE (remove or comment out):
# csv_data = file.read().decode('utf-8')
# stream = io.StringIO(csv_data)
# reader = csv.reader(stream)

# NEW CODE:
csv_data = file.read()  # Read as bytes
reader = ThaiCSVReader(csv_data)
# ... process rows as before ...
```

### Step 7: Test in Development (Recommended)

If you have a dev environment:

```bash
# Copy to dev environment first
rsync -av /tmp/CTFd_install/ user@dev-server:/tmp/thai-fix/

# Test on dev
# ... make changes on dev ...
# ... test import/export with Thai text ...

# If working, proceed to production
```

### Step 8: Apply to Production

```bash
# Stop CTFd service
sudo systemctl stop ctfd

# Apply your changes
# (You already did this in steps 5-6)

# Start CTFd service
sudo systemctl start ctfd

# Check status
sudo systemctl status ctfd
```

### Step 9: Verify Logs

```bash
# Check for any errors
sudo journalctl -u ctfd -n 50 --no-pager

# Check application logs
sudo tail -f /var/www/CTFd/CTFd/logs/ctfd.log
```

### Step 10: Test the Fix

1. **Login as Admin** to your CTFd instance

2. **Test Export:**
   - Go to Admin Panel > Challenges
   - Create a test challenge with Thai name: "ทดสอบภาษาไทย"
   - Export challenges to CSV
   - Download and open in Excel
   - **Verify:** Thai text displays correctly ✅

3. **Test Import:**
   - Create a CSV with Thai content (use `sample_challenges_thai.csv`)
   - Import via Admin Panel > Challenges > Import
   - **Verify:** Thai text appears correctly in challenges ✅

## 🔄 Alternative: Using Patch Files

If you prefer to use patch files:

```bash
cd /var/www/CTFd

# Backup original file
sudo cp CTFd/api/v1/challenges.py CTFd/api/v1/challenges.py.backup

# Apply patches
sudo -u ctfd patch -p1 < /tmp/CTFd_install/thai_csv_fix_export.patch
sudo -u ctfd patch -p1 < /tmp/CTFd_install/thai_csv_fix_import.patch

# Restart service
sudo systemctl restart ctfd
```

## 🐛 Troubleshooting

### Issue: ImportError for thai_csv_utils

**Error:**
```
ImportError: No module named 'CTFd.utils.thai_csv_utils'
```

**Solution:**
```bash
# Verify file exists
ls -l /var/www/CTFd/CTFd/utils/thai_csv_utils.py

# Check Python path
sudo -u ctfd python3 -c "import sys; print('\n'.join(sys.path))"

# Restart CTFd
sudo systemctl restart ctfd
```

### Issue: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Fix ownership
sudo chown -R ctfd:ctfd /var/www/CTFd/

# Fix permissions
sudo chmod -R 755 /var/www/CTFd/CTFd/
```

### Issue: Thai Still Garbled

**Symptoms:** Thai text still shows as ??????

**Solution:**
```bash
# Check if changes were applied
grep -n "ThaiCSVWriter" /var/www/CTFd/CTFd/api/v1/challenges.py

# If not found, re-apply the changes
# Make sure you edited the correct file
```

### Issue: Service Won't Start

**Solution:**
```bash
# Check error logs
sudo journalctl -u ctfd -n 100 --no-pager

# Check Python syntax
sudo -u ctfd python3 -m py_compile /var/www/CTFd/CTFd/api/v1/challenges.py

# If syntax error, restore backup
sudo cp /var/www/CTFd/CTFd/api/v1/challenges.py.backup /var/www/CTFd/CTFd/api/v1/challenges.py
```

## 🔙 Rollback Procedure

If something goes wrong:

```bash
# Stop service
sudo systemctl stop ctfd

# Restore from backup
sudo tar -xzf /backup/ctfd_backup_YYYYMMDD.tar.gz -C /

# Or restore single file
sudo cp /var/www/CTFd/CTFd/api/v1/challenges.py.backup /var/www/CTFd/CTFd/api/v1/challenges.py

# Start service
sudo systemctl start ctfd
```

## ✅ Post-Deployment Checklist

- [ ] Backup completed
- [ ] thai_csv_utils.py copied to CTFd/utils/
- [ ] Import statements added to challenges.py
- [ ] Export function modified
- [ ] Import function modified
- [ ] CTFd service restarted successfully
- [ ] No errors in logs
- [ ] Export test passed with Thai text
- [ ] Import test passed with Thai text
- [ ] Original English content still works

## 📊 Performance Monitoring

After deployment, monitor:

```bash
# CPU usage
top -u ctfd

# Memory usage
free -h

# Disk space
df -h

# Service status
systemctl status ctfd
```

The Thai CSV fix has minimal performance impact (<5% overhead).

## 🎯 Success Criteria

You've successfully deployed when:

1. ✅ CTFd service is running without errors
2. ✅ Export CSV with Thai text → Opens correctly in Excel
3. ✅ Import CSV with Thai text → Displays correctly in CTFd
4. ✅ English content still works as before
5. ✅ No increase in error logs

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review logs: `sudo journalctl -u ctfd -f`
3. Consult [THAI_CSV_FIX.md](THAI_CSV_FIX.md) for detailed documentation
4. Create a GitHub issue with logs and error messages

## 🎓 Best Practices

1. **Always test in dev first** before production
2. **Keep backups** for at least 30 days
3. **Monitor logs** for the first 24 hours after deployment
4. **Document any customizations** you make
5. **Update documentation** if your CTFd version differs

## 📝 Notes

- This fix is compatible with CTFd 3.x
- For CTFd 2.x, file locations may differ
- The fix is backward compatible with English content
- No database schema changes required

---

**Deployment Complete!** 🎉

Your CTFd now fully supports Thai language in CSV import/export!
