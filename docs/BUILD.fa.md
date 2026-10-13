# بازتولید و حفظ نسخه تحویلی

## نسخه نهایی ثابت است

Word و PDF تحویلی همان hashهای `qa/FINAL_QA.json` را دارند. برای جلوگیری از تغییر ناخواسته فایل‌های بازبینی‌شده، تغییر README یا سایر مستندات دیگر باعث بازتولید و جایگزینی خودکار آن‌ها نمی‌شود. گردش کار **Build seminar review candidate** فقط دستی اجرا می‌شود و خروجی را به‌صورت نامزد بازبینی در بخش Actions قرار می‌دهد؛ روی main منتشر نمی‌کند. پس از بازبینی واقعی نسخه تازه می‌توان آن را منتشر و QA را به‌روز کرد.

## مواد ساخت

مرجع متن `manuscript/seminar.fa.md`، جدول‌ها/منابع/چکیده `scripts/content_assets.py` و سازنده `scripts/build_seminar.py` است. محیط آزموده‌شده Debian 13، LibreOffice 25.2.3.2، python-docx 1.2.0 و matplotlib 3.10.8 است. قلم فارسی Noto Naskh Arabic و قلم لاتینِ جایگزین در PDF تحویلی Tinos است. هیچ فایل قلم در بسته منتشر نمی‌شود.

## ساخت محلی

```bash
python3 -m venv .venv
.venv/bin/pip install python-docx==1.2.0 matplotlib==3.10.8
MPLBACKEND=Agg .venv/bin/python scripts/build_seminar.py --font-size 11.5
soffice -env:UserInstallation=file:///tmp/melika-uno --headless --accept='socket,host=localhost,port=2003;urp;StarOffice.ServiceManager' --norestore --nodefault --nofirststartwizard &
python3 scripts/update_indexes.py artifacts/Personality_and_Suicide_Seminar.fa.docx
soffice -env:UserInstallation=file:///tmp/melika-export --headless --convert-to pdf --outdir artifacts artifacts/Personality_and_Suicide_Seminar.fa.docx
```

Python سیستمی باید python3-uno داشته باشد و LibreOffice/فونت‌ها نصب باشند. فهرست‌های Word با انتخاب متن و F9 قابل‌به‌روزرسانی‌اند. پس از هر ویرایش، بازبینی ارجاعات، شماره‌ها، اعداد و همه صفحات لازم است؛ موفقیت ساخت به معنی تأیید علمی نیست.

`restore_verified_source.py` ابزار بازیابی bootstrap است و روی منابع خوانای جدید اجرا نمی‌شود. نمودارها از CSV مستند ساخته شده‌اند و آماره‌های HR، OR و r جدا باقی می‌مانند. گردش کار **Package final delivery** فقط ZIP و checksum را همسان می‌کند؛ Word/PDF بازبینی‌شده را نمی‌سازد و تغییر نمی‌دهد.
