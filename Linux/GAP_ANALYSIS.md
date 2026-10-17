# تحلیل شکاف: محتوا، وابستگی و ظرفیت

تاریخ: 2026-10-17. این سند **الگوریتم و اولویت تحقیق** را مشخص می‌کند. در نبود اسکن کاملِ نسخه/فایل از داخل ایران، فهرست قطعی «بسته‌های ناموجود در ایران» تولید نشده است. وضعیت فعلی آن داده‌ها `UNVERIFIED` است، نه صفر و نه فهرست حدسی.

## ۱. مدل پوشش

سه مجموعه جدا نگه دارید:

- `required`: نیاز واقعی پروفایل‌های کاربران با نسخه و پلتفرم دقیق.
- `observed`: نسخه‌ها و فایل‌هایی که وجود/عدم‌وجود آن‌ها در منبع مشخص واقعاً بررسی شده است.
- `retained`: فایل‌هایی که نسخه قابل بازیابی تحت کنترل پروژه یا تعهد نگهداری معتبر دارند.

مقایسه فهرست توزیع‌ها یا شمارنده داشبورد، جای مقایسه این مجموعه‌ها را نمی‌گیرد. کامل‌بودن metadata و residency بدنه فایل دو محور مستقل‌اند.

## ۲. ماتریس حوزه‌ها و اولویت

پوشش زیر از مستندات اپراتورها استخراج شده، نه آزمون تمام نسخه‌ها. مراجع: [S01–S17](SOURCES.md).

| حوزه | منابع مستند/نامزد | شکاف محتمل برای آزمون، نه ادعای فقدان | اولویت و شیوه ارائه |
|---|---|---|---|
| Ubuntu 24.04 amd64 | آروان، ایران‌سرور، مبین، IUT، LinuxMirrors، لیارا، hmirror | نسخه دقیق security/updates، dependency closure و rollback | P0؛ APT metadata اصلی + redirect فایل معتبر |
| Ubuntu 22.04 و 26.04 | مسیرهای اعلام‌شده اپراتورها | تفاوت suite، وابستگی، معماری و نسخه قدیمی/جدید | P1؛ پروفایل و آزمون مستقل؛ 26.04 = resolute، S27 |
| Debian | شاتل، مبین، IUT، آروان، hmirror و دیگران | security جدا، bookworm/trixie و non-free/firmware | P1؛ کلید و metadata مخصوص Debian |
| Alpine / OpenWrt | Alpine در چند فهرست؛ OpenWrt در این بررسی پوشش جامع تأییدشده ندارد | نسخه دقیق firmware/target/ABI؛ kernel moduleها قابل جایگزینی دلخواه نیستند | P1/P2؛ index امضاشده و feeds همان build |
| Rocky / Alma / Fedora | IUT، مبین و پوشش مستند لیارا | EPEL/CRB، architecture، repodata و release consistency | P2؛ DNF/YUM-aware؛ صحت GPG حفظ شود |
| Arch | آروان، مبین، IUT | rolling snapshot و جلوگیری از partial upgrade | P2؛ آزمون snapshot هماهنگ، نه انتخاب جدیدترین بسته مستقل |
| pip / PyPI / AI | لیارا، چابکان، hmirror، رانفلر | wheel مناسب Python/ABI/CUDA، build dependencies و model weights | P1 برای پروژه‌های منتخب؛ wheelhouse با hashes |
| npm / pnpm / Yarn | لیارا، چابکان، hmirror، رانفلر | lockfile tarballs، optional/native packages، install scripts و دانلود خارجی | P1/P2؛ Verdaccio یا آرشیو project-specific |
| Go | لیارا، hmirror | module zip/mod/info، sumdb و toolchain download | P1/P2؛ vendor یا proxy/checksum policy صریح |
| Maven / Gradle | Myket، hmirror و سرویس‌های تخصصی | pluginها، parent POM، Gradle distribution و Android SDK licenses | P1 برای پروژه منتخب؛ cache/proxy تخصصی |
| NuGet | لیارا، چابکان، hmirror | registration/index، nupkg، SDK/runtime و platform packs | P2؛ restore واقعی بدون external fallback |
| Composer | لیارا و چابکان | dist/source URL خارجی، PHP extensions و lockfile | P2؛ archive/vendor مطابق مجوز |
| RubyGems / Cargo | 1Platform پوشش اعلام می‌کند؛ residency آزمون نشده | crate/gem نسخه دقیق و native build toolchain | P2؛ Cargo vendor و cache پروژه‌ای |
| DockerHub | HamDocker، لیارا، چابکان، رانفلر | همه layerها، manifests، platform، retention و authentication | P1/P2؛ OCI digest، registry تخصصی، نه URL rewriting عمومی |
| GHCR / Quay | لیارا و cacheهای تخصصی | token server، OCI index و معماری‌ها؛ GHCR سورس GitHub نیست | P2؛ registry جدا با آزمون protocol |
| GitHub code / Git / LFS | هیچ کدام از فهرست بالا آرشیو کامل GitHub را اثبات نمی‌کند | Git objects، submodules، LFS، releases، build dependencies | P1؛ Git bundle و manifests برای پروژه‌های تعیین‌شده |
| Terraform / OpenTofu | برخی نامزدهای فهرست جامعه | provider binary/OS/arch، checksums/signature، modules و registry discovery | P2؛ filesystem/network mirror رسمی همان ابزار |
| Ansible / Kubernetes / CI | رجیستری‌های عمومی و package mirrors بخشی را پوشش می‌دهند | collection roles، control-plane images، CNI/CSI، Helm charts، GitHub Actions dependencies | P1 برای bootstrap خود سامانه؛ P2 برای پوشش عمومی |
| Nginx/Apache/DB/SSH/monitoring | Ubuntu و RPM archives؛ مبین مسیرهای DB نیز نشان می‌دهد | edition/repository متفاوت، signing keys و dependencies | P0 فقط بسته‌های native پروفایل؛ نسخه vendor جدا |

## ۳. تعریف فایل و شکاف

کلید artifact: اکوسیستم، نام، نسخه، معماری/ABI، SHA-256 و اندازه. برای APT، `Filename` و `SHA256` و `Size` باید از Packages با زنجیره امضای معتبر آمده باشند. برای یک release asset از GitHub، HTTPS/نام فایل به‌تنهایی امضای ناشر نیست؛ شواهد provenance و checksum ناشر را ثبت کنید. [S25، S29](SOURCES.md)

```text
eligible = منابعی که واقعاً آن اکوسیستم/مسیر را پشتیبانی می‌کنند و استفاده‌شان مجاز است
if یک location دارای digest کامل معتبر و evidence تازه است:
    available (یا fragile، در صورت یک failure domain)
elif eligible غیرخالی و همه eligible در بازه جاری absent قطعی هستند:
    missing_in_tested_set
else:
    unknown
```

اگر هیچ منبع مرتبطی هنوز شناخته نشده، نتیجه `unknown/no_eligible_sources` است؛ ادعای نبود در تمام کشور نکنید. `403`, `429`, TLS failure، HTML 200 و timeout به absent تبدیل نشوند. علت و بازه زمانی همراه خروجی بماند.

هش مفقود، version mismatch و path mismatch هر کدام علت مستقل هستند. اگر دو منبع یک فایل را با hash متفاوت ارائه دهند، داده مشکوک قرنطینه می‌شود؛ «اکثریت mirrorها» جای اعتماد به متادیتای معتبر نیست.

## ۴. Ubuntu dependency closure

baseline نخست یک Ubuntu 24.04 amd64 پاک و از پیش دریافت‌شده است. مقدار digest آن باید در روز اجرا ثبت شود؛ این تحقیق digest ساختگی تعیین نمی‌کند. منابع خارجی میزبان، APT cache و لیست‌های قبلی وارد آزمایش نشوند.

ورودی seed از RESEARCH خوانده می‌شود؛ هر seed با نسخه واقعی و منبع metadata ثبت می‌گردد. نصب با `--no-install-recommends` و سپس خروجی resolved plan ثبت شود. تصمیم درباره Recommends بخشی از تعریف پروفایل است، نه روشی پنهانی برای کم‌کردن شمار شکست‌ها. Pre-Depends، alternatives، packages معماری all و بسته‌های از قبل نصب‌شده در baseline مستند شوند.

برای بازیابی کامل یک ماشین خالی، closure نسبت به rootfs خالی با closure نسبت به Ubuntu نصب‌شده فرق دارد. P0 فقط سناریوی دوم با baseline مشخص را گواهی می‌کند. ابزارهای تشخیصی باید با machine manifest و `apt` واقعی این قرارداد را کنترل کنند؛ یک لیست بازگشتی نام بسته‌ها کافی نیست.

## ۵. طرح GitHub قابل استفاده هنگام قطعی

برای هر پروژه منتخب، commit/tag مرجع، remote اصلی، مجوز، repository mirror یا Git bundle، LFS objects، submodule URL/commitها و Release Assets را جدا نگه دارید. mirror clone به‌تنهایی تمام پیوست‌ها یا سرویس‌های GitHub را نمی‌گیرد. [S29](SOURCES.md)

manifest پیشنهادی:

```json
{
  "schema_version": 1,
  "project": "owner/repository",
  "commit": null,
  "git_bundle_sha256": null,
  "release_assets": [],
  "lfs_objects": [],
  "submodules": [],
  "build_profile": null,
  "license_review": "pending",
  "offline_build_test": "not_run"
}
```

مقادیر null باید از عملیات واقعی تکمیل شوند. برای کاربر، bundle + دستور clone از فایل و اسکریپت نصب آفلاین ارائه کنید. Git server کامل و pull آنلاین از نام داخلی فاز جداست؛ Forgejo/Gitea می‌توانند آن بخش را انجام دهند. private repository بدون مجوز منتشر نشود.

## ۶. وابستگی‌های مخفی اکوسیستم‌ها

Python: همه wheels/build backends برای Python و معماری مقصد؛ فایل hash-locked و نصب بدون index خارجی. یک wheel لینوکس برای تمام نسخه‌ها و CUDAها کافی نیست. [S30](SOURCES.md)

Node: lockfile ثابت و tarballهای واقعی، Git dependencies و lifecycle scripts؛ `npm ci` می‌تواند در install script ابزار دیگری از خارج دریافت کند. `--ignore-scripts` صرفاً تشخیص است و نباید نرم‌افزار ناقص را نصب موفق معرفی کرد. [S31](SOURCES.md)

Go: علاوه بر proxy، سیاست checksum database و toolchain را از پیش تعیین کنید. خاموش‌کردن کلی اعتبارسنجی برای پنهان‌کردن وابستگی خارجی مجاز نیست. vendoring در پروژه‌های منتخب می‌تواند سطح مسئله را کوچک کند. [S32](SOURCES.md)

Cargo: vendor و configuration مناسب قبل از قطعی آماده شود؛ build toolchain/native libraries نیز لازم‌اند. OCI: همه layers و manifests برای platform دقیق با digest نگهداری شود؛ tag mutable یک pin معتبر نیست. [S33/S28](SOURCES.md)

## ۷. ظرفیت: اندازه‌گیری، نه عددسازی

برای هر پروفایل این مقادیر را محاسبه کنید:

```text
required_bytes = sum(size_bytes برای SHAهای یکتای required)
verified_domestic_bytes = sum(size_bytes برای required دارای location معتبر)
missing_bytes = sum(size_bytes برای missing_in_tested_set)
unknown_bytes = sum(size_bytes برای unknown با اندازه معلوم)
critical_retention_bytes = sum(size_bytes برای اقلام حیاتی که باید مستقل نگهداری شوند)
local_needed = metadata + unique(missing ∪ critical_retention) + staging + DB/logs
```

نرخ پوشش باید denominator معلوم داشته باشد: درصد بسته و درصد بایت دو عدد متفاوت‌اند. اگر اندازه برخی فایل‌ها معلوم نیست، مجموع را «کران پایینِ اقلام اندازه‌معلوم» بنامید، نه ظرفیت کل. overlap بین توزیع‌ها و snapshots با SHA deduplicate شود. source packages و debug symbols جدا حساب شوند.

| موج | سقف طراحی آزمایش، نه حجم واقعی داده | معیار توقف |
|---|---|---|
| P0 | ۱GiB metadata، ۵GiB CAS، ۱GiB full-verify در روز | عبور از cap، incomplete closure یا metadata mismatch |
| Git/Python منتخب | سقف مصوب هر پروژه پس از dry manifest | مدل/asset فاقد مجوز، dependence کشف‌نشده یا حجم نامعلوم |
| پوشش عمومی | فعلاً برآورد عددی معتبر ندارد | پس از داده واقعی inventory و قرارداد اپراتورها تصمیم شود |

اولویت ذخیره با `criticality × demand × lack_of_independent_retention` سنجیده شود؛ هزینه بایت و licensing به‌عنوان قید. این امتیاز یک heuristic طراحی است و باید با داده کاربران کالیبره شود، نه مدل اثبات‌شده اقتصادی.

## ۸. خروجی ماشین‌خوان لازم در اجرا

`profiles/noble-core.manifest.json`, `evidence/gaps-<UTC>.json`, `evidence/coverage-<UTC>.json` و `evidence/offline-install-<UTC>.log` در محیط اجرای پروژه تولید شوند. فایل عمومی شواهد، tokens/IPهای شخصی و URL خصوصی را حذف کند. زمان، source-set و baseline هر گزارش تغییرناپذیر بماند تا مقایسه روز بعد معنی داشته باشد.
