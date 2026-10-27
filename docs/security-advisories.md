# Advisory Applicability Review - 2026-10-27

This is a bounded review of relevant published vendor advisories against this repository, not a clean bill of health, native acceptance or a stable release. This addon does not bundle PHP, WHMCS, phpseclib, libssh2, libcurl or libxml. Actual installed versions, vendor backports and configuration must be measured by the accountable operator; old inventory is not current patch evidence.

## Source Mitigation

The Plesk adapter posts XML using libcurl. [CVE-2026-92392](https://curl.se/docs/CVE-2026-92392.html) affects HTTP/2 uploads in curl 8.12.0 through 8.22.0. Upstream lists 8.23.0, selected maintained-branch fixes and avoiding HTTP/2 as remedies. The adapter now explicitly selects HTTP/1.1 and refuses a failed cURL option setup before any request. This removes that protocol path here without weakening TLS peer/name checks, the no-proxy/no-redirect policy, response caps or deadlines. It does not update libcurl, protect other applications or establish that a particular deployment was exploitable. Upgrade the vendor-managed library separately.

The transport already rejects DTD/entity declarations before parsing, uses LIBXML_NONET, and does not enable automatic response decompression. [CVE-2026-86414](https://curl.se/docs/CVE-2026-86414.html) requires an HTTP proxy; this adapter disables proxies. These controls narrow the reviewed paths, not the host's overall exposure.

## Host And Framework Action

- **PHP:** [PHP's October 21 advisory](https://www.php.net/archive/2026.php#2026-10-21-5) fixes critical CVE-2026-109618 and CVE-2026-109619 in 8.2.35, 8.3.36, 8.4.27 and 8.5.12. Use the patched branch supported by the installed WHMCS release or documented vendor backports. A plugin check cannot protect a request that fails before application code runs. Verify the web SAPI and job/CLI runtimes separately.
- **Windows dependencies:** [PHP's October 26 notice](https://www.php.net/archive/2026.php#2026-10-26-1) describes Windows rebuilds with Brotli 1.2.1 for CVE-2026-111497. The PHP runtime version alone does not distinguish those rebuilds. This is not a claim that WHMCS supports Windows hosting or that the adapter enables Brotli decoding.
- **WHMCS:** [CVE-2026-67398 guidance](https://help.whmcs.com/m/125386/l/2116695-cve-2026-67398-whmcs-security-update-2026-09-03) concerns its 2CheckOut gateway, not these addons. Vendor fixes include 8.13.7/9.0.8; the [8.13 changelog](https://docs.whmcs.com/releases/8-13/8-13-change-log/) also records CVE-2026-67399. Use a currently supported, patched release, not just those historical fix floors. Help4 neither ships nor changes payment modules.
- **phpseclib:** The cPanel adapter can use framework-provided phpseclib 2/3. [CVE-2026-40194](https://github.com/phpseclib/phpseclib/security/advisories/GHSA-r854-jrxh-36qx) is fixed in 2.0.53/3.0.51; upstream rates this SSH HMAC timing issue Low with significant exploitation constraints. [CVE-2026-84308](https://github.com/phpseclib/phpseclib/security/advisories/GHSA-q97c-8qh3-fpc6) concerns pure-PHP Curve25519 timing, fixed in 3.0.57; no side-channel or affected deployed version has been demonstrated here. Have the framework owner update its supported dependencies. Do not overwrite WHMCS vendor files or treat a host-key pin as proof that pre-authentication library parsing is patched.
- **Native SSH:** PHP ssh2 uses the separately maintained libssh2. Verify that library's build and vendor fixes, including pre-authentication packet handling, against [upstream changes](https://github.com/libssh2/libssh2/blob/master/RELEASE-NOTES). This addon uses SSH command execution, not SFTP operations. No host library was inspected or upgraded in this review.
- **Plesk target:** Patch both the panel engine and hosted PHP handlers using [Plesk's PHP2Shell advisory](https://support.plesk.com/hc/en-us/articles/44397729587351-Vulnerability-CVE-2026-109618-and-CVE-2026-109619-PHP2Shell-Remote-code-execution-in-PHP-shipped-with-Plesk). Native Plesk installation and bridge enablement remain separate, manual actions.

## Verification And Release Boundary

Offline transport fixtures assert HTTP/1.1, no request on failed option setup, handle closure, TLS verification, no redirects/proxies and bounded output/time. Package tests preserve original import hashes while separately identifying this intentional Transport.php change. These tests do not exercise an installed WHMCS/MySQL framework, real TLS endpoint, native panel roles or a CVE exploit.

Existing 0.1.0 preview archives made before this change do not contain the mitigation. A source commit is not an installed update. Build fresh exact-commit candidates privately, verify inventories/checksums, and complete the native matrix and version-matched release approval before publication. Upgrade active addon directories in place; do not deactivate, rename IDs/tables, widen parsers or weaken endpoint trust.

Built by [Help4 Network](https://help4network.com/).
