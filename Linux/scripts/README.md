# ابزار پروب پژوهشی

از داخل پوشه Linux اجرا شود؛ فقط Python استاندارد لازم است. targets ورودیِ بازبینی‌شده مدیر است، نه ورودی کاربران عمومی.

```bash
python3 -m unittest discover -s tests -p 'test_probe_sources.py' -v
python3 scripts/probe_sources.py --targets scripts/PROBE_TARGETS.json \
  --vantage authorized-test-host --output /tmp/melika-probes.json
```

هر هدف یک GET با Range کوچک و حداکثر ۴۰۹۶ بایت دریافت دارد؛ میان هدف‌ها یک ثانیه فاصله است. redirect دنبال نمی‌شود و URL دارای query/credentials پذیرفته نمی‌شود. IPها پیش از اتصال کنترل و pin می‌شوند و TLS غیرفعال نمی‌شود. هیچ firewall، تنظیم APT، حساب یا فایل سیستم بیرون خروجی تعیین‌شده تغییر نمی‌کند.

این اسکریپت محدوده کشور، ماندگاری فایل، امضای InRelease، تمام‌بودن hash یا نصب آفلاین را ثابت نمی‌کند. DNS از resolver سیستم استفاده می‌کند و timeout کلی DNS در این ابزار پژوهشی تضمین نشده است؛ برای محیط نامطمئن یک deadline بیرونی در نظر بگیرید. برنامه اصلی به worker دارای budget/deadline/full-hash نیاز دارد و نباید این ابزار کوچک را جای تمام آن قابلیت‌ها بگذارد.

`sample_sha256` فقط هش sample است. پاسخ خطا/DNS به unknown تبدیل می‌شود، نه اثبات عدم‌وجود در ایران. پیش از اشتراک خروجی، جزئیات زیرساخت و هر داده حساس را بررسی کنید. نتایج این نشست در [دفتر شواهد](../evidence/RESEARCH_LOG.md) آمده‌اند.
