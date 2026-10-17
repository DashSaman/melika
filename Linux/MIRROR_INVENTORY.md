# فهرست شواهد میرورهای ایران

تاریخ بررسی: 2026-10-17. این فهرست، نقطه آغاز قابل توسعه است؛ ادعای کشف تمام میرورها یا آزمون همه فایل‌ها ندارد. [رجیستری ماشین‌خوان](MIRROR_SOURCES.yaml)، [منابع](SOURCES.md).

## ۱. چه چیزی واقعاً بررسی شد؟

متن صفحات رسمی، راهنماها و directory listingها در ابزار پژوهش بررسی شد. هیچ نشست دانلود کامل از IP تأییدشده داخل ایران اجرا نشد. بنابراین در تمام ردیف‌ها: **raw HTTP status، صحت TLS، Range، سرعت، آخرین تاریخ امضاشده متادیتا، تست فایل نمونه، بقای قطعی و استقلال مسیر = نامعلوم مگر بعداً شواهد جدا ثبت شود**. باز شدن HTML در ابزار به‌عنوان «HTTP 200 آزمایش‌شده» ثبت نشده است.

نوع «mirror» در نام یا صفحه بازاریابی، اثبات full mirror نیست. مسیر archive با مسیر security می‌تواند فرق داشته باشد. زمان نمایش داده‌شده کنار یک پوشه نیز آخرین همگام‌سازی معتبر کل مخزن نیست.

## ۲. منابع دارای شواهد مستقیم یا مستندات رسمی

| ارائه‌دهنده | URL دقیقِ مشاهده/مستندشده | پوشش قابل استناد | نوع / وضعیت |
|---|---|---|---|
| آروان | https://mirror.arvancloud.ir/ubuntu/ | Ubuntu؛ صفحه رسمی Debian، Arch، Alpine، Manjaro، OpenSUSE و CentOS را نیز معرفی می‌کند. | Mirror معرفی‌شده؛ کامل‌بودن نامعلوم. DOCUMENTED، S01. |
| ایران‌سرور | https://mirror.iranserver.com/ubuntu/ | تنظیمات Ubuntu شامل jammy/noble/resolute و pocketهای معمول در صفحه موجود است. | Mirror معرفی‌شده؛ فایل‌ها آزمایش نشده‌اند. DOCUMENTED، S02. |
| مبین‌هاست | https://mirror.mobinhost.com/ | listing شامل Ubuntu، Debian/security، Alpine، Arch، Alma، Fedora، EPEL، MariaDB، MongoDB و موارد دیگر. | Directory observed؛ کامل‌بودن نامعلوم. DOCUMENTED، S03. |
| دانشگاه صنعتی اصفهان | https://repo.iut.ac.ir/repo/ | Ubuntu، Debian، Alpine، Arch، Fedora، Rocky در مسیر `rocky-linux`، EPEL، OpenSUSE، TeX و موارد دیگر. | Directory observed؛ prefix `/repo/` ضروری است. DOCUMENTED، S04. |
| شاتل | https://mirror.shatel.ir/ | Debian و Debian-security در راهنمای مشاهده‌شده. | Ubuntu تأیید نشده؛ فقط پوشش مستند را فعال کنید. DOCUMENTED، S05. |
| LinuxMirrors | https://repo.linuxmirrors.ir/ubuntu/ | listing دایرکتوری‌های Ubuntu از جمله dists/pool. | ثبت در فهرست رسمی Ubuntu کمک به شناسایی است، نه تست جاری. DOCUMENTED، S06–S07. |
| لیارا | http://linux-mirror.liara.ir/repository/ubuntu/ و http://linux-mirror.liara.ir/repository/ubuntu-security/ | Ubuntu archive/security جدا؛ مستندات عمومی طیف وسیع رجیستری و لینوکس را معرفی می‌کنند. | راهنمای Ubuntu صریحاً کش را توضیح می‌دهد. DOCUMENTED، S08–S09. |
| چابکان | https://mirror2.chabokan.net/ | PyPI، npm، Docker، Composer، NuGet، Debian، Ubuntu و WordPress در داشبورد. | Caching proxy؛ وجود فایل خاص باید اثبات شود. DOCUMENTED، S10. |
| رانفلر | https://runflare.com/mirrors/ | مجموعه سرویس‌های توسعه در صفحه رسمی؛ تعیین endpoint هر سرویس از راهنمای همان سرویس. | محدودیت ۵۰۰ درخواست رایگان/IP؛ دوره سهمیه روشن نیست. DOCUMENTED، S11. |
| مایکت | https://maven.myket.ir/ | Maven، Gradle wrapper، Android SDK و Flutter. | مجموعه خدمات تخصصی، نه آرشیو تمام GitHub. DOCUMENTED، S12/S17. |
| هم‌روش | https://repo.hmirror.ir/ubuntu و https://repo.hmirror.ir/debian | همچنین npm، Python، Go، NuGet، Maven و apk طبق راهنمای ارائه‌دهنده. | Cache معرفی‌شده. DOCUMENTED، S13. |
| HamDocker | https://hub.hamdocker.ir/ | Docker Hub؛ میزبان‌های جدا برای mcr/gcr/quay/elastic در راهنما. | Container cache؛ namespace و digest مهم‌اند. DOCUMENTED، S13. |
| 1Platform | https://mirror.1platform.net/ | صفحه ارائه‌دهنده پوشش متنوع لینوکس و بسته‌های توسعه نشان می‌دهد. | اعلام پوشش؛ داخلی‌بودن مسیر و residency نامعلوم. DOCUMENTED، S14. |

درباره میزبانی: مبین‌هاست محل Tehran DC1 را اعلام می‌کند؛ Myket و لیارا خدمات را داخلی معرفی می‌کنند. این اطلاعات، **اظهار ارائه‌دهنده** است، نه traceroute/ASN/آزمون قطع در این نشست. برای دیگران هویت ایرانی یا دانشگاهی با محل واقعی پاسخ‌دهی و مسیر ترافیک یکسان تلقی نشود. TLS معتبر و دامنه `.ir` نیز کشور مسیر را ثابت نمی‌کنند.

درباره ظرفیت: عدد حدود ۱۲۰TB مبین‌هاست یا آمار ۹۶۵GB داشبورد چابکان فقط اظهارات همان صفحات‌اند. این‌ها ظرفیت رایگان تخصیص‌یافته به پروژه ما، اندازه فایل‌های یکتا، میزان پوشش Ubuntu یا تضمین نگهداری نیستند. [S03/S10](SOURCES.md)

## ۳. نامزدهای اضافی؛ هنوز قابل فعال‌سازی نیستند

منبع کشف: فایل نگهداری‌شده توسط پروژه Mirava، نه تأیید اپراتور هر سرویس. [S15–S16](SOURCES.md)

| نامزد | نشانی کشف‌شده | بررسی لازم |
|---|---|---|
| AminIDC | http://mirror.aminidc.com/ | محتوای جاری، HTTPS، مسیر دقیق Ubuntu/Mint و مجوز. |
| KubarCloud | https://mirrors.kubarcloud.com/ | صفحه از ابزار قابل استفاده نشد؛ تست داخل ایران. |
| ITO portal | https://repo-portal.ito.gov.ir/repo/ | کنترل مسیر، دامنه مقصد redirect و موجودی. |
| ITO repository | https://repo.ito.gov.ir/ | رابطه با portal، نه فرض دو failure domain. |
| Pardis | https://mirrors.pardisco.co/ | مسیرهای واقعی و وضعیت جاری. |
| Afranet | http://mirror.afranet.com/ | HTTP/HTTPS و نوع مخزن. |
| Pishgaman | https://ubuntu.pishgaman.net/ | ریشه واقعی آرشیو و suiteهای جاری. |
| Ferdowsi CRAN | https://cran.um.ac.ir/ | CRAN/R؛ وضعیت و مجوز mirror. |
| 0-1 Cloud | https://mirror.0-1.cloud/ | پوشش و محل میزبانی. |
| KimiaHost | https://ubuntu-mirror.kimiahost.com/ | صحت path و metadata. |
| DigitalVPS | https://mirror.digitalvps.ir/ubuntu/ | suiteها، TLS و استقلال شبکه. |
| Sindad Ubuntu | https://ir.ubuntu.sindad.cloud/ | پیشوند `ir` مدرک جغرافیا نیست؛ مسیر شبکه لازم است. |
| Faraso | http://mirror.faraso.org/ | موجودی و منشأ اعتماد. |
| Parsdev | https://mirror.parsdev.com/ | پوشش و شرایط استفاده. |

این فهرست از لحاظ وضعیت، `UNVERIFIED` است. نبود نتیجه از ابزار پژوهش، «down» محسوب نمی‌شود. URLهای نامزد پیش از کاربرد باید با صفحه اپراتور و پروب کم‌حجم تأیید شوند؛ با حدس‌زدن suffix، endpoint تولیدی نسازید.

## ۴. مواردی که نباید داخلی فرض شوند

فهرست‌های جامعه ممکن است mirrorهای MIT، Freedif یا ارائه‌دهندگان مستقر خارج ایران را هم داشته باشند. `ir.archive.ubuntu.com` نیز صرفاً یک نام انتخاب/ارجاع است و نام کشور، مسیر داخل ایران را تضمین نمی‌کند. تمام چنین مواردی تا وجود شواهد مسیر و residency از `DOMESTIC_ONLY` خارج می‌مانند. هشدار مهم‌تر: وجود چند دامنه متفاوت با CDN، دیتاسنتر یا upstream مشترک، افزونگی مستقل ایجاد نمی‌کند.

## ۵. اطلاعاتی که برای هر منبع باید تکمیل شود

برای معرفی عمومی یک backend، رکورد زیر لازم است: URL مؤثر و تمام redirectها؛ IPv4/IPv6 و ASN/مسیر از میزبان مجاز؛ زمان UTC؛ نسخه و checksum معتبر متادیتا؛ نمونه فایل کامل با اندازه/هش؛ Range/Resume؛ محدودیت درخواست و Retry-After؛ وضعیت قرارداد/مجوز redirect؛ منبع خارجی لازم برای cache miss؛ سیاست نگهداری/حذف؛ و failure domain.

permission_state می‌تواند `unreviewed`, `documented_public_use`, `operator_approved`, `restricted`, `denied` باشد. اعلام استفاده عمومی معمول، مجوز بار انبوه یا تبدیل‌شدن به backend یک سرویس ملی نیست. برای بار قابل توجه با اپراتور هماهنگ شود؛ هیچ مکانیزم چرخش حساب/IP برای دورزدن سهمیه طراحی نشود.

## ۶. ترتیب آزمون پیشنهادی

نخست آروان، ایران‌سرور، مبین‌هاست، IUT و LinuxMirrors برای نمونه متادیتای noble. پس از آن مسیرهای مستقل archive/security لیارا و hmirror. شاتل فقط برای مرحله Debian. رجیستری‌های Docker/PyPI/npm در موج جدا با client همان پروتکل آزمایش شوند. رانفلر از بار خودکار کنار گذاشته شود تا سیاست سهمیه روشن شود.

برای هر کاندید، ابتدا ۴KiB دریافت bounded؛ سپس روی تعداد محدودی فایل ثبت‌شده بررسی کامل انجام شود. ابزار `scripts/probe_sources.py` فقط بخشی از بررسی حمل‌ونقل است؛ نمی‌تواند کشور میزبانی، مجوز، آخرین sync، صحت امضا یا نصب موفق را به‌تنهایی اثبات کند.
