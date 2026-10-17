# Primary-source ledger

Research date: 2026-10-17. URLs below were consulted through a web research interface unless explicitly marked discovery-only. A rendered/indexed page is evidence of published content, not a raw HTTP transaction from Iran. Access date is not last upstream synchronization. No page text is reproduced wholesale. Statements about our proposed design are engineering decisions, not provider promises.

## Iranian providers

| ID | Primary URL | Evidence used / boundary |
|---|---|---|
| S01 | https://www.arvancloud.ir/fa/dev/linux-repository | Official distribution/configuration coverage; not full-file availability. |
| S02 | https://mirror.iranserver.com/ | Provider mirror documentation; some examples disable validation and must not be copied. |
| S03 | https://mirror.mobinhost.com/ | Directory entries and provider-stated Tehran DC1/120TB/100GE; not audited capacity or SLA. |
| S04 | https://repo.iut.ac.ir/repo/ | University directory listing and exact paths. |
| S05 | https://mirror.shatel.ir/ | Debian and Debian-security instructions visible. |
| S06 | https://repo.linuxmirrors.ir/ubuntu/ | Ubuntu directory listing. |
| S07 | https://launchpad.net/ubuntu/+archivemirrors | Official Ubuntu mirror discovery; cached status is not a live health check. |
| S08 | https://liara.ir/mirrors/ | Published ecosystem coverage. |
| S09 | https://docs.liara.ir/mirrors/ubuntu/ | Exact archive/security URLs and cache description. |
| S10 | https://mirror2.chabokan.net/ | Provider calls service a caching proxy; dashboard counts are self-reported. |
| S11 | https://runflare.com/mirrors/ | 500 free requests per IP in FAQ; no reset period established. |
| S12 | https://maven.myket.ir/ | Maven, Gradle, Android SDK and Flutter services; not an audit of all objects. |
| S13 | https://hamravesh.com/blog/container-registry-mirroring-and-caching/ | HamDocker and hmirror exact container/package cache endpoints. |
| S14 | https://mirror.1platform.net/ | Provider-listed broad coverage; domestic routing not established. |
| S15 | https://github.com/MiravaOrg/Mirava | Community project source; discovery only, not provider verification. |
| S16 | https://raw.githubusercontent.com/MiravaOrg/Mirava/main/mirrors_list.yaml | Candidate registry includes external entries and scope errors; must filter and test. |
| S17 | https://maven.myket.ir/services/maven.html | Maven-specific client documentation. |

## Rubika and pricing

| ID | Primary URL | Evidence used / boundary |
|---|---|---|
| S18 | https://rubika.ir/botapi | Official bot API base and distinction from private/personal clients. |
| S19 | https://rubika.ir/botapi/methods | requestSendFile/upload_url, multipart file, file_id, getFile/download_url. No durable-storage guarantee inferred. |
| S20 | https://rubika.ir/rules | Provider rights, private API restrictions and usage conditions; legal interpretation remains qualified. |
| S21 | https://rubika.ir/faq | Three-account app management and excessive-use warning; no verified 2GB bot quota found. |
| S22 | https://pypi.org/project/rubpy/ | Published package metadata/release evidence; repository license must be reconciled before reuse. |
| S23 | https://liara.ir/pricing/ | IaaS table, separate IPv4 and traffic prices; not PaaS prices. |
| S24 | https://www.arvancloud.ir/fa/pricing/cloud-storage | Free tier, plans and tariffs; storage-overage table and FAQ conflict. |

## Trust, package and archive protocols

| ID | Primary URL | Evidence used |
|---|---|---|
| S25 | https://manpages.debian.org/trixie/apt/apt-secure.8.en.html | Release/index/package hash trust chain and dedicated signing keys. |
| S26 | https://manpages.debian.org/trixie/apt/sources.list.5.en.html | Signed-By, By-Hash, date and Valid-Until controls. |
| S27 | https://lists.ubuntu.com/archives/ubuntu-announce/2026-April/000323.html | Ubuntu 26.04 release announcement, resolute. |
| S28 | https://docs.docker.com/docker-hub/image-library/mirror/ | Pull-through caching, revalidation and upstream dependence. |
| S29 | https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository | Git mirror and LFS backup workflow. |
| S30 | https://pip.pypa.io/en/stable/topics/secure-installs/ | Hash-checked dependency installation. |
| S31 | https://docs.npmjs.com/cli/v11/commands/npm-ci/ | Lock-based installation and lifecycle behavior. |
| S32 | https://go.dev/ref/mod | Module proxy, checksum database and vendoring semantics. |
| S33 | https://doc.rust-lang.org/cargo/commands/cargo-vendor.html | Vendored dependency source preparation. |

## Reusable software

| ID | Primary URL | Evidence used |
|---|---|---|
| S34 | https://github.com/openSUSE/MirrorCache | Fileless mirror redirector and metadata inventory; GNU GPL label on source page. |
| S35 | https://github.com/tuna/tunasync | Chinese mirror manager/worker design; GPL-3.0 source label. |
| S36 | https://github.com/aptly-dev/aptly | Repository management source and license/release metadata. |
| S37 | https://www.aptly.info/doc/aptly/mirror/create/ | Signature verification, filtering and dependency options. |
| S38 | https://manpages.debian.org/trixie/debmirror/debmirror.1.en.html | Partial-mirror workflow and GPL-2.0-or-later; source updated 2026-05-07. |
| S39 | https://pulpproject.org/pulp_deb/ | Repository synchronization/publication/signing documentation. |
| S40 | https://github.com/pulp/pulpcore | Core source/license, distinct from plugin licenses. |
| S41 | https://help.sonatype.com/en/formats.html | Format-specific proxy/host/group support; APT has no group in observed matrix. |
| S42 | https://help.sonatype.com/en/repository-types.html | Hosted/proxy/group semantics and cache-age checks. |
| S43 | https://support.sonatype.com/hc/en-us/articles/360037243413-How-to-Make-Proxy-Repositories-Act-Like-Hosted-Repositories | Explicit block-outbound mode for serving cached content. |
| S44 | https://goharbor.io/docs/main/administration/configure-proxy-cache/ | OCI proxy-cache behavior and setup. |
| S45 | https://www.verdaccio.org/docs/caching/ | npm cache storage and uplink behavior. |
| S46 | https://github.com/verdaccio/verdaccio | Source/license and release information. |
| S47 | https://docs.gitea.com/usage/repository/repo-mirror/ | Git repository mirroring, not universal GitHub dependency backup. |
| S48 | https://forgejo.org/docs/latest/user/repo-mirror/ | Forgejo pull/push mirroring. |
| S49 | https://github.com/rezaaa/walrus | Experimental Telegram-to-Rubika workflow; not audited storage software. |

## Inaccessible or discovery-only candidates

`mirror.aminidc.com`, `mirrors.kubarcloud.com`, `repo-portal.ito.gov.ir/repo`, `repo.ito.gov.ir`, and `mirrors.pardisco.co` did not yield usable live evidence in this research path. They remain candidates, not declared globally offline. Additional S16 entries are discovery-only in the YAML registry. No exact endpoint is promoted merely by adding `/ubuntu` to a domain.

## Revalidation policy

Before operating a source: record effective URL, DNS answers, TLS verification, test vantage, HTTP result, body type, bounded Range response, complete trusted digest for selected artifacts, signed metadata dates, permission decision, and failure-domain evidence. Keep `null` for missing data. Raw signed URLs and personal/client identifiers must remain private. Recheck commercial terms in the provider's purchase interface before spending money.
