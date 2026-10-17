# پروژه‌های مشابه و تصمیم Build / Integrate / Buy

تاریخ ارزیابی: 2026-10-17. مقایسه بر اساس مستندات و مخازن اصلی است، نه نصب و benchmark همه محصولات. آخرین فعالیت فقط وقتی درج شده که شناسه و تاریخ مشخص دریافت شده باشد؛ زمان crawl صفحه، تاریخ توسعه نیست. قبل از pin کردن هر dependency، مجوز فایل‌های همان release و security advisoryهای آن بررسی شود.

## ۱. گزینه‌های نزدیک و ابزارهای تخصصی

| پروژه و مرجع اصلی | مجوز / فعالیت قابل تأیید در این بررسی | قابلیت مرتبط | محدودیت و تصمیم |
|---|---|---|---|
| [MirrorCache](https://github.com/openSUSE/MirrorCache) | برچسب GPL-2.0 در مخزن؛ آخرین commit مشاهده‌شده 2026-09-28، جدول پایین | redirector با کاتالوگ فایل و انتخاب mirror؛ نزدیک‌ترین نمونه به data plane پیشنهادی | ساختار موجود آن باید با منابع ناهمگون ایران، سیاست offline و evidence mapping تطبیق یابد. مرجع اصلی طراحی و نامزد جدی P1؛ جایگزین آزمون APT یا اجازه اپراتور نیست. |
| [aptly](https://github.com/aptly-dev/aptly) | MIT؛ آخرین commit مشاهده‌شده 2026-10-12 | mirror/filter، snapshot، dependency options، انتشار و امضای مخزن | برای recovery repository منتخب است. عملیات mirror معمول فایل‌ها را دریافت می‌کند؛ فرض «فقط metadata بدون disk» نکنید. [مستندات](https://www.aptly.info/doc/aptly/mirror/create/) |
| [debmirror](https://manpages.debian.org/trixie/debmirror/debmirror.1.en.html) | GPL-2.0-or-later در manual؛ source update درج‌شده 2026-05-07، نه الزاماً آخرین commit upstream | partial Debian/Ubuntu mirror با انتخاب بخش‌ها | برای ذخیره subset استاندارد مفید؛ موتور redirect/gap نیست. دستورالعمل mirror رسمی Debian را با partial archive اشتباه نگیرید. |
| [apt-cacher-ng](https://manpages.debian.org/trixie/apt-cacher-ng/apt-cacher-ng.8.en.html) | نسخه manual مشاهده‌شده 3.7.5-1؛ source timestamp آن 2024-07-22؛ آخرین release و مجوز دقیق در این بررسی تثبیت نشد | HTTP package caching proxy | مناسب کش محلی و کاهش دانلود تکراری؛ کش گرم و سیاست نگهداری لازم است. با full retained mirror یا zero-disk aggregator برابر نیست. |
| [Pulp / pulp_deb](https://pulpproject.org/pulp_deb/) | [pulpcore](https://github.com/pulp/pulpcore) GPL-2.0-or-later؛ مجوز pluginها جدا بازبینی شود؛ آخرین commit استخراج نشد | sync/publication/signing و مدیریت محتوای چند اکوسیستم | قابلیت زیاد، اما منابع و پیچیدگی استقرار بیشتر؛ نامزد P2 به‌جای ساخت registryهای متعدد از صفر. |
| [Nexus Repository](https://help.sonatype.com/en/formats.html) | محصول و edition دارای شرایط متفاوت؛ مجوز/قیمت نسخه انتخابی نیازمند بررسی؛ آخرین release اینجا ثبت نشد | hosted/proxy/group برای formatهای پشتیبانی‌شده | در ماتریس مشاهده‌شده، APT دارای proxy/hosted است ولی group ندارد. «یک group برای همه APTها» پیشنهاد نشود. حالت [block outbound](https://support.sonatype.com/hc/en-us/articles/360037243413-How-to-Make-Proxy-Repositories-Act-Like-Hosted-Repositories) برای کش آفلاین باید صریح تنظیم شود. |
| [TUNA tunasync](https://github.com/tuna/tunasync) | GPL-3.0؛ commit مشاهده‌شده 2026-05-15 | الگوی manager/worker برای همگام‌سازی mirror، نمونه مهم چینی | برنامه‌ریز sync است، نه درگاه تشخیص شکاف بی‌دیسک؛ P2 برای عملیات آرشیو بزرگ. |
| [Mirava](https://github.com/MiravaOrg/Mirava) | مجوز و آخرین commit دقیق در این پژوهش تثبیت نشد | رجیستری جامعه از mirrorها و ابزار انتخاب | فقط کشف نامزدها؛ داده شامل موارد خارجی و نیازمند بازبینی است. قبل از کپی کد LICENSE را بخوانید؛ insecure commands را اجرا نکنید. |
| [Gitea](https://github.com/go-gitea/gitea) | MIT طبق README؛ آخرین commit در این ارزیابی استخراج نشد | Git hosting و [repository mirroring](https://docs.gitea.com/usage/repository/repo-mirror/) | مناسب فاز Git server؛ خودبه‌خود LFS/releases/dependencyهای پروژه را کامل آرشیو نمی‌کند. |
| [Forgejo](https://forgejo.org/docs/latest/user/repo-mirror/) | طبق [FAQ رسمی](https://forgejo.org/faq/)، نسخه 9 به بعد GPL-3.0-or-later؛ نسخه‌های تا 8 MIT؛ آخرین commit ثبت نشد | self-hosted Git و pull/push mirroring | جایگزین P1/P2 برای میزبانی کپی Git؛ نگهداری سورس پروژه با حفظ build environment فرق دارد. |
| [Harbor](https://github.com/goharbor/harbor) | Apache-2.0 در مخزن؛ آخرین commit ثبت نشد | رجیستری OCI با [proxy cache](https://goharbor.io/docs/main/administration/configure-proxy-cache/) | برای Docker/GHCR/Quay از proxy عمومی مناسب‌تر؛ digest، platform، token و retention هنوز لازم‌اند. P2. |
| [Verdaccio](https://github.com/verdaccio/verdaccio) | MIT؛ آخرین commit دقیق ثبت نشد | npm registry/cache با uplink | گزینه منتخب npm در مرحله بعد؛ [سیاست caching](https://www.verdaccio.org/docs/caching/) و lockfile/install-scriptها باید آزمون شوند. |
| [Walrus](https://github.com/rezaaa/walrus) | مجوز و audit امنیت تثبیت نشده | نمونه اتصال فایل/Telegram به Rubika | صرفاً مطالعه امکان اتصال؛ dependency خارجی Telegram و سطح ورودی آن برای control plane آفلاین مناسب نیست. کپی کد بدون مجوز ممنوع. |

برای یک نمونه روسی مشخص، در این دور شواهد اولیه کافی برای توصیه محصول جداگانه تثبیت نشد؛ نام یا قابلیت ساختگی به جدول اضافه نشده است. نمونه چینی TUNA و نمونه‌های بین‌المللی و ایرانی بالا نیازهای اصلی طراحی را پوشش می‌دهند. این جدول inventory تمام نرم‌افزارهای جهان نیست.

## ۲. شواهد دقیق فعالیت سه نامزد اصلی

این‌ها پاسخ endpoint رسمی `commits?per_page=1` شاخه پیش‌فرض در تاریخ تحقیق هستند. تاریخ committer با author ممکن است متفاوت باشد؛ تاریخ زیر از committer است. commit جدید به معنی release پایدار، security review یا آزمایش این پروژه نیست.

| پروژه | commit | زمان UTC |
|---|---|---|
| MirrorCache | [29b7aa70c11f086bae17cc554f1f8bc77eb6e59b](https://github.com/openSUSE/MirrorCache/commit/29b7aa70c11f086bae17cc554f1f8bc77eb6e59b) | 2026-09-28T13:19:01Z |
| aptly | [516fcc6bfd08c46e1cd35e5395a04e82bc3ea4fe](https://github.com/aptly-dev/aptly/commit/516fcc6bfd08c46e1cd35e5395a04e82bc3ea4fe) | 2026-10-12T14:12:56Z |
| tunasync | [702c68c4397b1d8445a5e0e4e085814d3656576b](https://github.com/tuna/tunasync/commit/702c68c4397b1d8445a5e0e4e085814d3656576b) | 2026-05-15T09:46:02Z |

## ۳. ماتریس تصمیم نهایی

| نیاز | Build | Integrate | Buy / existing service | تصمیم |
|---|---|---|---|---|
| کاتالوگ شواهد و gap classification | کوچک و اختصاصی | استفاده از parser/SQLite استاندارد | پنل mirror فعلی این semantics را تضمین نمی‌کند | Build باریک P0 |
| verification امضا و dependency solver | پیاده‌سازی دوباره خطرناک | gpgv + archive keyring + native APT | لازم نیست | Integrate P0 |
| مسیر فایل و UI/API | چند endpoint محدود | FastAPI/Nginx؛ MirrorCache برای مرحله بزرگ‌تر | CDN عمومی نیازمند قرارداد | Build thin layer، نه پروتکل جدید |
| نگهداری نسخه بازیابی APT | از صفر نسازید | aptly/debmirror با دامنه کنترل‌شده | object store برای بدنه | Integrate P1 |
| ذخیره شکاف‌ها | Local CAS ساده | S3-compatible adapter | free tier محدود یا ظرفیت موجود؛ خرید با اجازه | Local P0، استاندارد P1 |
| Rubika | wrapper کوچک رسمی و مشروط | SDK فقط پس از audit و LICENSE | مجوز/سهمیه اپراتور روشن شود | آزمایشی خاموش؛ پیش‌شرط MVP نیست |
| Git/PyPI/npm/OCI | universal proxy نسازید | Git bundles، wheelhouse، Gitea/Forgejo، Verdaccio، Harbor | mirrorهای موجود پس از آزمون | پروتکل به پروتکل، P1/P2 |
| orchestration در مقیاس | Kubernetes از روز اول لازم نیست | Compose و worker کوچک؛ TUNA/Pulp بعداً | managed زیرساخت تنها با نیاز سنجیده | کوچک شروع شود |

**چرا MirrorCache فوراً نصب نشده است؟** این مأموریت پژوهش است، نه benchmark/deployment. از نظر کارکرد redirector بسیار نزدیک است؛ اما P0 به API شواهد، منابع با ریشه‌های متفاوت، profile محدود، سیاست unknown-vs-absent و اختیار storage نیاز دارد. انتخاب حاضر یک thin gateway با اجزای استاندارد است. اگر در اجرای اولیه مشخص شد پذیرش امن APT در بودجه نمی‌گنجد، scope به gateway preview محدود و پذیرش APT باز می‌ماند؛ نباید برای حفظ برنامه یک‌روزه بررسی امضا/هش حذف شود.

تخمین تغییرات کیفی است: thin gateway کم تا متوسط برای دامنه P0؛ MirrorCache متوسط برای integration منابع/سیاست؛ Pulp/Nexus/Harbor متوسط تا زیاد از نظر استقرار؛ Git bundle/wheelhouse کم برای چند پروژه مشخص. هیچ یک از این سطوح، نتیجه اندازه‌گیری زمان توسعه یا تضمین اجرا نیست.
