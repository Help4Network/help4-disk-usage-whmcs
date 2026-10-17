# WHMCS cPanel/WHM Adapter

Canonical addon source is now [help4-disk-usage-whmcs](https://github.com/Help4Network/help4-disk-usage-whmcs). The native [cPanel/WHM plugin](https://github.com/Help4Network/help4-disk-usage) stays separate on managed Linux servers. Existing addon ID help4_disk_usage, version1.0.2 and its private tables are preserved by extraction. Independent distribution0.1.0 is a preview; native/framework acceptance remains separate.

## Requirements

Use a supported WHMCS installation, its matching PHP runtime and current cPanel server records. Remote Check/Deploy/Update/Sync needs PHP ssh2 or WHMCS-bundled phpseclib2/3, SSH reachability, a decryptable administrative SSH credential in the protected native server record and an independently verified server host-key pin. The addon uses a separate SSH port setting, not the native WHM API port such as2087. Keep all credentials out of Git, URLs, screenshots and logs.

If SSH transport is unavailable, install the native panel plugin manually and do not claim the addon can perform remote operations. This adapter does not manage Plesk servers or send shell installers to Windows.

## Package And Install

```sh
python3 scripts/test.py
python3 scripts/package.py --component cpanel
```

Use dist/help4-disk-usage-whmcs-cpanel-0.1.0.zip and its adjacent SHA-256. Follow [installation](install.md) to verify outer/internal manifests, extract privately outside the web root, then copy only modules/addons/help4_disk_usage into the matching WHMCS addon directory. This is the new package layout; do not extract the entire archive under modules/addons or assume the historical top-level help4_disk_usage ZIP layout.

Lint the copied help4_disk_usage.php and hooks.php with the WHMCS PHP CLI before new activation. In System Settings > Addon Modules activate Help4 Disk Usage only for a new installation, restrict administrator roles and review settings. Existing active modules do not need deactivation merely to change source. Open Addons > Help4 Disk Usage.

Activation creates only:
```text
mod_help4_disk_usage_servers
mod_help4_disk_usage_accounts
mod_help4_disk_usage_events
```

No existing table, addon name, service association or schema is renamed by extraction. Deactivation intentionally retains reporting tables.

## Initial Settings And Server Identity

| Setting | Initial operation |
| --- | --- |
| Native Update Manifest URL | https://raw.githubusercontent.com/Help4Network/help4-disk-usage/main/update.json |
| Release Tarball URL | Reviewed immutable native package fallback; deployment requires checksum-bearing manifest |
| Default SSH Port |22, independently verify actual endpoint |
| SSH Host Fingerprints | Explicit independently verified pin per participating server |
| Allow Unpinned SSH | Off; never enable to overcome a mismatch |
| Sync Account Limit | Start with2 before deliberately increasing;0 means all accounts within the whole-run budget |
| Whole Sync Scan Max Seconds | Start with15 before raising after observation |
| Client Area Reports | Explicitly review/off for a new unvalidated install; historical config default is on |
| Display Name / Credit Prefix | Operator title and prefix, retaining linked Help4 byline |

For each intended cPanel server confirm native WHMCS server type, current endpoint, protected administrative SSH credentials and SSH port. Obtain host-key fingerprints from an independently trusted server console, not solely from the connection being validated:

```sh
for key in /etc/ssh/ssh_host_*_key.pub; do
  ssh-keygen -lf "$key" -E sha256
done
```

Save the correct negotiated algorithm's fingerprint in addon JSON keyed by exact server ID/hostname/IP:
```json
{"cpanel-a.example.test":"SHA256:independently-verified-console-fingerprint"}
```

A missing/mismatched pin stops before password authentication. Verify endpoint, port, key algorithm and authorized rotation/rebuild provenance before changing trust. Do not use a different algorithm's fingerprint or enable unsafe unpinned SSH.

## Native Operations And Health

For an existing native installation select Check, then small bounded Sync; repeat Sync for explicitly partial batches. For a missing plugin select Check, separately authorize Deploy, verify native manifest/package checksum, Check again, then small Sync. Update targets the native cPanel plugin, not this WHMCS addon distribution. Native server OS/cPanel/root/reseller/install/lifecycle acceptance and fleet authority remain required.

Remote scan actions share the native nonblocking scanner lock and whole-run/account budget. No parallel unbounded all-account scan or routine backup job is added by extraction. Do not keep clicking Sync while an operation is busy.

The addon Servers & Deploy, Server Health and account drill-down pages show native plugin/version/last-seen/scan coverage/account severity/partial/error state and next actions. The admin-home widget requires Perform Server Operations. Cached state is not fresh collection, complete host-service monitoring or hardware health; partial is not a transport failure, and missing history is not healthy-zero.

## Customer Reports And Native File Manager

The existing mapping uses current tblhosting.server plus cPanel username and current active service ownership. Former/terminated service associations must not authorize reused-account reports. Unmapped accounts stay admin-only. Client navigation is under Services when enabled; every rendered account row is checked against current client/service/server/username, and service links are regenerated instead of storing reusable SSO URLs.

Reports include summary and retained large-file/tree/cache-log-temp offender metadata with last-scan state and cautious remediation hints. No file-content or privileged cleanup endpoint is supplied. Native File Manager is reached after signing into the customer's current cPanel service and opening Files > Disk Usage Audit; direct report links must preserve native authentication/navigation. See [file workflows](cpanel-file-workflows.md). Extraction does not add Plesk-style direct File Manager redirects to this adapter.

## Upgrade, Recovery And Acceptance

Follow [independent migration/upgrade/removal](upgrade.md), not the native scanner version. Git pull only changes source. Quiesce addon operations, verify an identified package and replace only the intended runtime; preserve settings and all private tables. An unchanged addon version during extraction does not imply a database migration. Keep the previous immutable compatible addon archive/checksum for rollback; no routine snapshots.

Keep the native scanner/plugin installed separately. Removing this WHMCS addon does not remove hosting files or native panel software. Table deletion or production rollout is a separate explicit administrator action.

Before stable approval verify the actual WHMCS framework/PHP/database, role/CSRF/client ownership boundaries, SSH implementations/known-key rejection, bounded Sync/deployment, cached health/error rendering, native root/reseller/account GUI and File Manager behavior. Offline fixtures do not prove that native matrix.

Official references: [Addon installation](https://developers.whmcs.com/addon-modules/installation-uninstallation/), [configuration](https://developers.whmcs.com/addon-modules/configuration/), [upgrades](https://developers.whmcs.com/addon-modules/upgrades/), [hooks](https://developers.whmcs.com/hooks/module-hooks/).

Built by [Help4 Network](https://help4network.com/).
