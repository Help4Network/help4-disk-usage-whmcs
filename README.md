# Help4 Disk Usage For WHMCS

Standalone WHMCS integration for **both cPanel/WHM and Plesk Linux/Windows**. Install these addons on the WHMCS host, not inside a hosting control panel. Native collectors and interfaces are separate deployments:

- [cPanel/WHM plugin](https://github.com/Help4Network/help4-disk-usage)
- [Plesk extension](https://github.com/Help4Network/help4-disk-usage-plesk)

**Free to use, customize and redistribute.** No Help4 product key, activation, subscription, server fee or paid tier. Retain the included notices and small linked **Built by [Help4 Network](https://help4network.com/)** byline. WHMCS, Plesk and operating-system requirements are separate vendor requirements.

## Status And Capabilities

Independent distribution **0.1.0 development preview**, not an approved stable WHMCS release. Extraction preserves the existing cPanel addon version1.0.2 and Plesk addon version0.3.0. Distribution, addon and native panel versions are separate; components.json records them. Existing installations keep their exact addon IDs, settings and tables. Source/fixture CI is not native WHMCS/MySQL/TLS or panel certification.

| Adapter | Existing addon ID | Transport | Administrator capabilities |
| --- | --- | --- | --- |
| cPanel/WHM | help4_disk_usage | Independently pinned SSH | Check, native plugin Deploy/Update, bounded account Sync, cached health/widget and account drill-down |
| Plesk | help4_disk_usage_plesk | Authenticated verified-HTTPS XML API bridge | Connect/Approve/Disconnect, bounded extension-health Check, scoped reports/exports/refresh/File Manager |

The Plesk bridge must be separately installed and explicitly enabled. **WHMCS's native Plesk provisioning module does not install this extension automatically.** Plesk extension installation/update is currently a manual native administrator operation on Linux or Windows; no Linux SSH installer is sent to Windows. cPanel never manages Plesk records. Both adapters keep their own limits, authorization and private data.

Health describes the extension, not every host service or hardware. Unknown/stale/partial/failed reports are not healthy-zero. File actions expose metadata and native panel navigation, not privileged contents/deletion or reusable SSO links.

## Build And Test

Python3.10+ builds packages. PHP/extensions must match the installed WHMCS release. Candidate CI exercises PHP8.3/8.4 with cURL, DOM and PDO SQLite; this is not a blanket WHMCS-version support claim.

```sh
git clone https://github.com/Help4Network/help4-disk-usage-whmcs.git
cd help4-disk-usage-whmcs
python3 scripts/test.py
python3 scripts/package.py
python3 scripts/package.py --component cpanel
python3 scripts/package.py --component plesk
```

Windows development uses `py -3`; PHP must be on PATH. The WHMCS host's supported OS is independent of remote Plesk Windows support. Artifacts:

```text
dist/help4-disk-usage-whmcs-0.1.0.zip
dist/help4-disk-usage-whmcs-cpanel-0.1.0.zip
dist/help4-disk-usage-whmcs-plesk-0.1.0.zip
```

Every ZIP has a SHA-256 sidecar and internal SHA256SUMS. Verify and extract outside the web root, then copy only the desired modules/addons directories. Packages exclude native code/installers, test fixtures, private evidence, credentials and customer reports. The builder checks an explicit inventory and rejects links/reparse points before traversal. Use trusted quiescent source: path validation and temporary ZIP replacement are not concurrent-replacement protection or an atomic ZIP/checksum transaction.

## Install And Upgrade

Read [installation](docs/install.md), [migration/upgrade/removal](docs/upgrade.md), [compatibility](docs/compatibility.md), [native acceptance](docs/validation.md), [cPanel operations](docs/cpanel.md) and [Plesk operations](docs/plesk.md).

Activate/configure each desired addon separately. Preserve IDs and private tables; do not deactivate/drop/rename an installed addon or reinstall a native plugin merely because its source moved. Review administrator role access and keep new customer reporting disabled until native isolation tests pass. Installing files does not activate modules or connect/deploy a server.

A Git pull changes source only. Build, verify and deploy reviewed addon files separately from native panel releases. cPanel Check/Deploy/Update and Plesk Software updates target their own native components, not this WHMCS distribution. Addon releases live in [this repository](https://github.com/Help4Network/help4-disk-usage-whmcs/releases); no automatic addon download-and-execute pipeline is supplied. Keep identified previous immutable packages for rollback; no routine snapshots.

## Public Review

UPSTREAM.json records source commits/import hashes. Twelve runtime files were initially imported byte-for-byte. Seven native files under tests/fixtures/plesk are pinned offline protocol fixtures only, never production payloads. H4DU_PLESK_SOURCE can select an identified native checkout for tests, not a running panel. See [security policy](SECURITY.md) and [acceptance gates](docs/validation.md).

No billing, tickets, chargebacks, customer provisioning, automatic fleet deployment or privileged deletion operation is added. No vendor endorsement, certification or marketplace approval is claimed.

Built by [Help4 Network](https://help4network.com/).
