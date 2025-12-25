# 🚀 CTFd Ultimate Installation (Final Patched)

> **อัปเดตแก้ไข:** ปัญหา Permission (502 Gateway) และรองรับ Nginx Official Repo เรียบร้อย

## 🇹🇭 แก้ปัญหาภาษาไทยใน CSV Import/Export

**NEW!** แก้ไขปัญหาภาษาไทยแสดงผลเพี้ยนเมื่อ Export/Import โจทย์เป็น CSV

👉 [คลิกที่นี่เพื่ออ่านวิธีแก้ไข (THAI_CSV_FIX.md)](THAI_CSV_FIX.md)

- ✅ Export CSV ภาษาไทยเปิดใน Excel ได้ถูกต้อง
- ✅ Import CSV ภาษาไทยไม่เพี้ยน
- ✅ รองรับ UTF-8 with BOM

---

### ✅ STEP 1: เตรียมเครื่อง & Nginx (Official + Fix Permission)

จุดที่เพิ่มมาคือบรรทัดสุดท้าย (`usermod`) ครับ สำคัญมาก\!

```bash
# 1. อัปเดตและติดตั้ง dependencies พื้นฐาน
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential python3 python3-pip python3-venv python3-dev libevent-dev

# 2. ติดตั้ง Nginx (Official Stable Version)
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
sudo apt update
sudo apt install -y nginx

# 3. สร้าง User ctfd
sudo useradd -m -s /bin/bash ctfd
# ⚠️ ระบบจะให้ตั้งรหัสผ่านใหม่
sudo passwd ctfd 

# 🛠️ [FIX] เพิ่ม user 'nginx' เข้ากลุ่ม 'www-data' เพื่อให้เข้าถึง Socket ได้
sudo usermod -aG www-data nginx
```

### ✅ STEP 2: ติดตั้ง CTFd & Python Environment

ส่วนนี้เหมือนเดิมครับ เพราะเป็น Best Practice แล้ว

```bash
# 1. เตรียมโฟลเดอร์
sudo mkdir -p /var/www/CTFd
sudo chown -R ctfd:ctfd /var/www/CTFd

# 2. เข้าไปทำในฐานะ user ctfd
su - ctfd

# 3. ดาวน์โหลดและติดตั้ง
cd /var/www/CTFd
git clone https://github.com/CTFd/CTFd.git .
python3 -m venv venv

# 4. ติดตั้ง Libraries (gevent เพื่อความแรง)
source venv/bin/activate
pip install -r requirements.txt
pip install gevent gunicorn

# 5. ออกจาก user ctfd
exit
```

### ✅ STEP 3: สร้าง Service (Gunicorn Socket)

ใช้ Socket file เพื่อความเร็วสูงสุด

```bash
sudo tee /etc/systemd/system/ctfd.service <<'EOF'
[Unit]
Description=CTFd Gunicorn Service (Ultimate Edition)
After=network.target

[Service]
User=ctfd
Group=www-data
WorkingDirectory=/var/www/CTFd
Environment="PATH=/var/www/CTFd/venv/bin"
# ใช้ gevent + unix socket
ExecStart=/var/www/CTFd/venv/bin/gunicorn --workers 3 --worker-class gevent --bind unix:/var/www/CTFd/ctfd.sock --access-logfile - --error-logfile - "CTFd:create_app()"

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# เริ่มทำงาน
sudo systemctl daemon-reload
sudo systemctl enable ctfd
sudo systemctl start ctfd
```

### ✅ STEP 4: ตั้งค่า Nginx (Static Optimize)

แยกการโหลดรูปภาพให้ Nginx ทำงานโดยตรง เว็บจะลื่นมาก

```bash
# 1. สร้างไฟล์ config
sudo tee /etc/nginx/conf.d/ctfd.conf <<'EOF'
server {
    listen 80;
    server_name _;

    # Optimization: ให้ Nginx ส่งไฟล์ Static เอง (Cache 30 วัน)
    location /static {
        alias /var/www/CTFd/CTFd/static;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /themes {
        alias /var/www/CTFd/CTFd/themes;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Proxy Pass
    location / {
        proxy_pass http://unix:/var/www/CTFd/ctfd.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }
    
    client_max_body_size 50M;
}
EOF

# 2. ลบ config เดิม
sudo rm /etc/nginx/conf.d/default.conf 2>/dev/null
```

### ✅ STEP 5: กำหนดสิทธิ์และเริ่มระบบ (Important Fix\!) 🛡️

นี่คือขั้นตอนที่เพิ่มเข้ามาเพื่อให้ **ไม่ต้องแก้ 502 ทีหลัง** ครับ

```bash
# 1. ปรับสิทธิ์โฟลเดอร์ให้กลุ่ม www-data (ที่มี nginx อยู่) เข้าถึงได้
sudo chown -R ctfd:www-data /var/www/CTFd
sudo chmod -R 750 /var/www/CTFd

# 2. รีสตาร์ท CTFd เพื่อสร้างไฟล์ Socket ใหม่
sudo systemctl restart ctfd

# 3. รอสัก 2 วินาที แล้วปรับสิทธิ์ไฟล์ Socket
sleep 2
sudo chmod 770 /var/www/CTFd/ctfd.sock 2>/dev/null

# 4. รีสตาร์ท Nginx เพื่อเริ่มใช้งาน
sudo nginx -t
sudo systemctl restart nginx
```

