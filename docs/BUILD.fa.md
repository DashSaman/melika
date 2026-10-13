# بازتولید و کنترل نسخه تحویلی

مرجع محتوا: manuscript/seminar.fa.md و scripts/content_assets.py. محیط ساخت آزموده‌شده: Debian 13، LibreOffice 25.2.3.2، python-docx 1.2.0، matplotlib 3.10.8 و بسته‌های فونت Noto Core/Croscore/DejaVu. فایل قلم در مخزن توزیع نمی‌شود.

## مسیر آماده

در GitHub Actions، workflow «Build and publish seminar» را اجرا کنید. این گردش کار وابستگی‌ها را نصب، منبع خوانا را حفظ، رکورد منابع را صادر، DOCX را می‌سازد، فهرست‌ها را با UNO به‌روز و PDF را تولید می‌کند. خروجی و گزارش ساخت را روی شاخه main منتشر می‌کند. hash نسخه بازتولیدشده ممکن است به علت زمان/متادیتا متفاوت شود؛ تأیید نسخه تازه نیازمند QA است.

## ساخت محلی

```bash
python3 -m venv .venv
.venv/bin/pip install python-docx==1.2.0 matplotlib==3.10.8
MPLBACKEND=Agg .venv/bin/python scripts/build_seminar.py --font-size 11.5
soffice -env:UserInstallation=file:///tmp/melika-uno --headless --accept='socket,host=localhost,port=2003;urp;StarOffice.ServiceManager' --norestore --nodefault --nofirststartwizard &
python3 scripts/update_indexes.py artifacts/Personality_and_Suicide_Seminar.fa.docx
soffice -env:UserInstallation=file:///tmp/melika-export --headless --convert-to pdf --outdir artifacts artifacts/Personality_and_Suicide_Seminar.fa.docx
```

Python سیستمی باید python3-uno داشته باشد؛ فونت‌ها و LibreOffice نیز لازم‌اند. در Word می‌توان همه متن را انتخاب و فهرست‌ها را با F9 به‌روز کرد. پس از ویرایش، تمام صفحات و تطبیق شماره‌ها بررسی شوند.

`restore_verified_source.py` فقط ابزار بازیابی bootstrap است، نه مرحله لازم هر ساخت. گردش کار از بازنویسی خودکار منابع خوانای جدید با bootstrap جلوگیری می‌کند. نمودارهای کمی از CSV با آماره‌های جداگانه ساخته شده‌اند؛ مقادیر آن‌ها بدون منبع تازه تغییر نکنند.

گردش کار «Package final delivery» فقط بسته ZIP و فایل checksum را به‌روز می‌کند و Word/PDF بازبینی‌شده را تغییر نمی‌دهد. وجود SHA صحیح به‌تنهایی جایگزین بررسی علمی نیست.
