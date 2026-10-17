# دستور مستقل اجرای MVP با Codex — Iran Smart Linux & Developer Mirror

## مأموریت و محدوده اختیار

در مخزن `https://github.com/DashSaman/melika` یک MVP واقعی بر اساس تحقیقات پوشه `Linux/` بساز. فقط فایل‌های همین پوشه را ایجاد/ویرایش کن. پروژه سمینار موجود در ریشه مستقل است؛ root README، AGENTS، workflowها، docs و artifacts آن را تغییر نده. مقصد تحویل، شاخه `main` است؛ هیچ force-push، پاک‌کردن تغییرات دیگران یا بازنویسی تاریخچه مجاز نیست.

هدف این است که کاربران در ایران بتوانند بسته‌های منتخب Ubuntu و فایل‌های ثبت‌شده توسعه را از یک آدرس ثابت بگیرند. فایل‌های موجود از mirrorهای داخلی تأییدشده تأمین شوند؛ فقط شکاف‌های اثبات‌شده و اقلام حیاتیِ فاقد کپی مستقل نزد خودمان نگهداری شوند. این پروژه ساخت mirror چندترابایتی یا proxy آزاد URL نیست.

بودجه هدف **۸ تا ۱۲ ساعت تلاش مهندسی برای MVP محدود** است؛ تضمین آماده‌شدن همه سرویس‌ها در یک روز نده. اجازه/پاسخ اپراتور، دسترسی ماشین داخل ایران، انتقال داده و آزمون ۲۴/۷۲ساعته روبیکا می‌توانند بیرون این بودجه بمانند. یک خروجی کوچک، امن، تست‌شده و با موانع شفاف بهتر از ادعای کامل‌بودن غیرواقعی است.

## ابتدا این کارها را انجام بده

1. مخزن و شاخه فعلی، آخرین head، `git status` و تغییرات دیگر عامل‌ها را واقعاً بخوان. چیزی را پاک نکن. `Linux/AGENTS.md` دستور scoped این پروژه است.
2. فایل‌های `Linux/RESEARCH.md`, `ARCHITECTURE.md`, `API_CONTRACT.md`, `IMPLEMENTATION_PLAN.md`, `SECURITY_AND_OFFLINE.md`, `MIRROR_SOURCES.yaml`, `RUBIKA_FEASIBILITY.md` و `evidence/RESEARCH_LOG.md` را کامل بخوان. `RELATED_PROJECTS.md` و `GAP_ANALYSIS.md` مرجع تصمیم‌های reuse و dependency هستند.
3. بررسی کن کدام فایل‌های برنامه واقعاً موجودند. این بسته در اصل پژوهش و ابزار پروب است، نه سرویس مستقرشده؛ وجود طرح را با وجود کد یکی ندان.
4. برنامه IMPLEMENTATION_PLAN را task-by-task اجرا کن. تصمیم‌های اصلی معماری را دوباره به بحث نامحدود تبدیل نکن. فقط در صورت شواهد جدیدِ ناسازگار، تغییر ضروری را به‌صورت ADR داخل Linux مستند کن و ریسک را توضیح بده.

## معماری قطعی P0

Python 3.12 + FastAPI + Jinja2 و CSS محلی، Nginx، SQLite/WAL، یک worker/scheduler و Docker Compose با سرویس‌های edge/app/worker. متادیتای معتبر محلی و Local CAS با کلید SHA-256؛ دانلود بدنه فایل موجود از mirror مجاز با 302. Redis/Celery/Kubernetes یا frontend build پیچیده لازم نیست. از APT و gpgv واقعی استفاده کن؛ dependency solver یا رمزنگاری اختصاصی ننویس.

Product code زیر `Linux/app/` است. نام ماژول‌ها، جدول‌های SQL، مدل‌ها، endpointها و signature تابع‌ها در API_CONTRACT و IMPLEMENTATION_PLAN دقیق تعیین شده‌اند. آن‌ها را یکپارچه اجرا کن؛ هر task نباید نام دلخواه متفاوتی برای همان interface بسازد.

ابتدا dependency و image version موجود را واقعاً resolve، security-check و lock کن. digest، نسخه یا checksum ساختگی ننویس. runtime باید با imageها/وابستگی‌های ازپیش‌دریافت‌شده بدون Docker Hub، pip، GitHub، Google Fonts، CDN جاوااسکریپت و login خارجی بالا بیاید. برای GitHub فقط در زمان توسعه/انتشار نیاز اتصال داریم، نه هنگام استفاده روزانه از gateway.

## پروفایل Ubuntu و مرز پذیرش

P0 فقط Ubuntu24.04، suiteهای `noble`, `noble-updates`, `noble-security`، component `main`، architecture `amd64` و `all`های مرتبط است. seeds: `ca-certificates`, `curl`, `git`, `nginx`, `openssh-client`, `rsync`, `unzip`, `jq`. عضویت component و نسخه را با APT واقعی کنترل کن؛ حذف seed یا افزودن مخفیانه component ممنوع است. نصب با سیاست مستند `--no-install-recommends` انجام شود.

metadata اصلی امضاشده را بدون تغییر نگه دار. InRelease -> index hashes -> package SHA-256/size زنجیره اعتماد است. suite/security base ممکن است متفاوت باشد؛ از suite_map رجیستری استفاده کن. bundleها atomic منتشر شوند، by-hash و نسخه‌های قبلی لازم حفظ شوند، و path/hash conflict مسدود شود. منقضی‌شدن metadata با خاموش‌کردن Valid-Until یا عقب‌بردن ساعت حل نشود. recovery repository با کلید مستقل یک فاز بعدی است، نه امضای مجدد مخفیانه به نام Ubuntu.

دو وضعیت مستقل گزارش کن:

- `gateway_preview`: تست نرم‌افزار، کاتالوگ و routing در محیط معتبر پاس شده‌اند.
- `apt_profile_accepted`: روی baseline پاک و مشخص، با کلید معتبر و فقط مسیرهای مجاز، `apt-get update` و نصب واقعی کل پروفایل انجام شده و لاگ/manifest آن وجود دارد.

یک mocked 200، partial download، صفحه HTML قابل مشاهده یا تست واحد نمی‌تواند وضعیت دوم را true کند. اگر ماشین مجاز داخل ایران یا منبع قابل تأیید در دسترس نیست، fixtureهای امضاشده آزمایشگاهی را اجرا کن و تست تولیدی را `blocked/not_run` اعلام کن. شبکه ایران را از محل سیستم کاربر یا نام دامنه حدس نزن.

## منابع و ذخیره‌سازی

فایل MIRROR_SOURCES دارای ۲۷ source entry است، نه ۲۷ اپراتور مستقل. همه پیش‌فرض غیرفعال‌اند. DOCUMENTED یعنی اعلام ارائه‌دهنده، نه آزمایش فایل/کش/کشور. ابتدا منابع Ubuntu مرتبط را با ابزار کم‌حجم آماده و سپس بررسی کامل امضا/بسته آزمایش کن. از cache miss، timeout، 403، 429 یا خطای DNS، نتیجه «این فایل در ایران نیست» نگیر. missing_in_tested_set فقط برای source-set مرتبطِ واقعاً بررسی‌شده و پاسخ قطعی absent است.

موجودی آروان، ایران‌سرور، مبین، IUT، LinuxMirrors و دیگران را از paths ثبت‌شده بررسی کن. portal عمومی چابکان/رانفلر را به‌اشتباه APT base نکن. چند دامنه یا حساب روی یک زیرساخت، افزونگی مستقل نیستند. شرایط استفاده و سهمیه‌ها را رعایت کن؛ حساب/IP را برای دورزدن محدودیت عوض نکن.

Local CAS فعال باشد: streaming hash/size verification، temp+fsync+rename، کنترل quota، جلوگیری از symlink/path escape، و serving داخلی Nginx. سقف طراحی P0: ۱GiB metadata و ۵GiB CAS، نه ادعای اندازه واقعی پروفایل. فایل حیاتی و metadata مرجع زنده را برای بازشدن جا حذف نکن.

`RubikaBackend` در P0 غیرفعال و قابل تعویض است. بدون token مجاز، API رسمی، پاسخ روشن درباره استفاده و آزمون round-trip/full-hash/TTL/Range/دسترسی ناشناس، ادعای backend عملیاتی نکن. API شخصی غیررسمی، دریافت OTP، pooling حساب برای دورزدن quota، خرید سرویس یا ساخت حساب جدید جزو اختیار این مأموریت نیست. کلید و URL دارای token هرگز در Git/لاگ عمومی قرار نگیرد.

## API و رفتار حداقلی

این مسیرها را طبق API_CONTRACT پیاده کن: `/`, `/healthz`, `/readyz`, `/v1/sources`, `/v1/artifacts`, `/v1/artifacts/{sha256}`, `/v1/artifacts/{sha256}/resolve`, `/download/{sha256}/{filename}`, `/v1/gaps`, `/v1/profiles/{id}`, `/ubuntu/dists/{suite}/{path}`, `/ubuntu/pool/{path}`, `/openapi.json`.

GET/HEAD فایل فقط از mapping ثبت‌شده. شناسه نامعلوم 404، تضاد اعتماد 409، نداشتن کپی قابل استفاده 503 و rate limit برابر 429 است. URL دلخواه از کاربر نگیر. redirect تصمیم موقت با no-store است؛ پس از 302 نمی‌توان انتقال نیمه‌قطع‌شده را به‌طور جادویی به منبع دوم منتقل کرد. این محدودیت را در UI/راهنما و تست منعکس کن.

mutation مدیریتی فقط CLI محلی. UI فارسی، واکنش‌گرا و سبک با نمایش زمان شواهد، وضعیت واقعی منبع و پیام unknown باشد. Swagger/CDN خارجی بدون self-hosting وارد نکن؛ OpenAPI JSON و راهنمای محلی کافی است.

## امنیت و بودجه‌ها

URL allowlist، رد IPهای خصوصی/loopback/link-local و IPv6 mapped، بررسی تمام DNS answers و pin کردن اتصال با Host/SNI صحیح الزامی است. بررسی DNS اولیه و سپس resolution مجدد بدون کنترل کافی نیست. redirectها به‌صورت دستی و فقط به مقصد مجاز، بدون انتقال credentials بین originها بررسی شوند. TLS را هرگز خاموش نکن؛ استثنای HTTP برای metadata امضاشده فقط طبق policy مشخص source است، نه مجوز دانلود عمومی ناامن.

پروب: ۴ هم‌زمان global، ۱ در هر source، sample حداکثر ۴۰۹۶بایت، timeout و deadline محدود، فاصله هر host حداقل ۱ثانیه، بودجه نمونه ۱۰۰۰ درخواست/روز و full-verify پیش‌فرض ۱GiB/روز. سقف هر artifact برای P0 برابر ۵۱۲MiB است؛ بزرگ‌ترها نیازمند تغییر صریح و مجاز cap هستند. quotaها با restart صفر نشوند. Rate-limit ارائه‌دهنده اگر کمتر است اولویت دارد. حالت DOMESTIC_ONLY هیچ fallback خارجی پنهانی ندارد.

## روش اجرا و آزمایش

برای هر task ابتدا test شکست‌خورنده بنویس، شکست درست را ببین، حداقل کد لازم را اضافه کن، test را سبز کن و بعد refactor کن. تست موجود research probe را حفظ کن. تست‌ها باید شامل SSRF/rebinding، 200 HTML، Range غلط، signature/hash mismatch، metadata expiry/rollback، by-hash قدیمی، pool conflict، disk-full، source failure، jobs deduplication، secrets و bootstrap آفلاین باشند.

ابزار `scripts/probe_sources.py` یک پروب پژوهشی با ۱۸ تست است؛ آن را با production worker که quota/deadline/full-hash/job persistence دارد یکی ندان. label محیط آزمون را خودش کشور واقعی تلقی نمی‌کند.

دستورهای تحویل از داخل `Linux/` باید واقعاً قابل اجرا باشند:

```bash
python3 -m unittest discover -s tests -p 'test_probe_sources.py' -v
python3 -m pytest tests -q
docker compose -f compose.yaml config --quiet
make validate
make integration
make offline-test
```

Make targetها را با exit-code واقعی و ابزارهای موجود ایجاد کن؛ دستوری که وجود ندارد یا محیطی که Docker ندارد «PASS» نمی‌شود. تست قطعی در محیط disposable و جدا از شبکه مدیریتی اجرا شود؛ firewall یا اتصال SSH میزبان production را قطع نکن. mockهای mirror و client می‌توانند روی شبکه internal Docker باشند، ولی این تست را موفقیت واقعی شبکه ایران معرفی نکن.

## اولویت و کنترل دامنه

P0 به‌ترتیب: config/schema -> guarded fetch -> signed metadata/catalog -> profile/gaps -> routing/Local CAS/API/UI -> scheduler/admin/backup -> Compose/acceptance.

P1/P2 را امروز بی‌دلیل اضافه نکن: full mirror، تمام نسخه‌های Ubuntu، Docker registry، npm/PyPI عمومی، Git server، چند edge، مدل‌های AI بزرگ و Rubika production. برای این‌ها در docs backlog واقعی وجود دارد. اگر زمان محدود شد، امنیت/تست را حذف نکن؛ قابلیت APT را غیرفعال نگه دار و preview سالم تحویل بده.

## تحویل و Git

`Linux/RUNBOOK.md` شامل نصب، preload آفلاین، تغییر mode، افزودن منبع، rollback، backup/restore و عیب‌یابی باشد. `Linux/DELIVERY_REPORT.md` شامل commit مبنا، محیط/نسخه ابزارها، فایل‌های ساخته‌شده، تست‌های واقعی با exit-code، وضعیت preview، وضعیت APT profile، بودجه واقعی و blockers دقیق باشد.

گزارش سه بخش جدا داشته باشد: software tests، real provider probes، in-Iran offline install. نمونه/fixture/فرض/اعلام ارائه‌دهنده/آزمون واقعی را مخلوط نکن. هیچ URL، hash، داده تماس، quota، قیمت، نتیجه تست یا commit ساختگی ننویس.

قبل از commit همه تغییرات را بازبینی کن: فقط Linux، بدون secret و بدون بازنویسی کار دیگران. آخرین main را بررسی و تغییرات concurrent را حفظ کن. فایل‌ها را commit و بدون force به main push کن؛ اگر سیاست شاخه مانع است، روی شاخه مجاز نتیجه را نگه دار و محدودیت را گزارش کن، نه اینکه push موفق اعلام کنی. در پایان head و اسناد منتشرشده را دوباره بخوان و لینک واقعی/commit SHA بده.

**از بررسی وضعیت فعلی مخزن شروع کن و کار را در همین اجرا انجام بده. برای تحقیق مجدد نامحدود یا پرسش تکراری متوقف نشو؛ در نقطه نیاز به اختیار واقعی، هزینه یا زیرساخت ناموجود، آن بخش را مسدود گزارش کن و بخش‌های مستقلِ مجاز را تکمیل کن.**
