# بازبینی ثبت پروژه و نمودار — نه QA نهایی سمینار

تاریخ: ۲۰۲۶-۱۰-۱۳
checkpoint علمی/اجرایی بررسی‌شده: `CP03-initial-research`
commit بررسی‌شده: `83c8d147b2045037e491fba4782dca2c2ac2ec3d`

## بررسی‌های انجام‌شده
- **PASS:** درخت بازگشتی همین commit از GitHub دوباره خوانده شد؛ پاسخ درخت `truncated:false` بود و ۱۷ فایل ثبت‌شده را نشان داد.
- **PASS:** پرامپت نسخه ۲ با blob SHA برابر `e88ab896a87434b52637a362e19cb465de1bcb57` و اندازه ۲۸۴۵۴ بایت در مخزن وجود دارد.
- **PASS:** README از شاخه `main` دوباره خوانده شد؛ درصد ۲۵، checkpoint و اعلام آماده‌نبودن Word در آن مشاهده شد. مقصدهای لینک‌های داخلی README با درخت موجود تطبیق داده شدند.
- **PASS:** PROGRESS.json و progress.svg از `main` دوباره خوانده شدند. نسخه متنی منتقل‌شده به محیط بررسی با محاسبه Git blob SHA دقیقاً با فایل‌های GitHub برابر بود: JSON=`8a22922b327bed447d327f34f42d2c1ac785f9ac`؛ SVG=`80894a12f110239acf00649b47f074e6e9204288`.
- **PASS:** محاسبه با Python: مجموع وزن هشت مرحله ۱۰۰؛ مجموع امتیازها ۲۵؛ امتیاز هیچ مرحله از وزنش بیشتر نیست.
- **PASS:** XML نمودار معتبر است؛ طول بخش پُر ۱۳۰ از ۵۲۰ واحد، دقیقاً ۲۵٪ است. SVG با CairoSVG به PNG رندر و تصویر از نظر خوانایی و بریدگی بازبینی شد.
- **PASS:** فیلدهای Word، PDF و شمار صفحات در JSON برابر null هستند؛ وضعیت NOT_READY است. از QA زیرساخت برای افزایش امتیاز مرحله بازبینی نهایی استفاده نشده است.

## خروجی آزمون اجراشده
```text
PASS: Local JSON and SVG exactly match GitHub blob hashes.
PASS: Eight stage weights sum to 100; earned points sum to 25.
PASS: All earned points remain within their stage weights.
PASS: SVG bar length is exactly 25 percent; XML parses and PNG renders.
PASS: No final document or page-count claim exists in progress JSON.
NOT_TESTED: final seminar, complete article critiques, Word rendering, citation matching, similarity.
```

## محدودیت اجرای بررسی
دریافت یکجای ZIP مخزن در محیط محلی به علت محدودیت شبکه/DNS و محدودیت ابزار دانلود موفق نشد. به‌جای ادعای داشتن clone کامل، درخت و فایل‌های لازم از اتصال GitHub بازخوانی شدند؛ برای JSON/SVG نسخه محلی با هش یکسان بررسی شد. بنابراین این گزارش آزمون کامل همه فایل‌ها، clone مستقل مخزن یا تست تمام ابزارهای آینده نیست.

## همچنان ناتمام
نقد کامل سه مقاله، تأیید نهایی همه منابع/اعداد، متن سمینار، جدول‌ها/شکل‌های علمی، ساخت و رندر Word، تطابق دوطرفه منابع، همانندجویی و بازبینی نهایی ارائه نشده‌اند. این فایل تنها صحت ثبت checkpoint و نمودار را بررسی می‌کند؛ مرحله P8 همچنان صفر است.
