# Install The Standalone WHMCS Addons

Install on the WHMCS host. Native cPanel/WHM and Plesk plugins are separate managed-server installations. WHMCS's existing native cPanel or Plesk provisioning module stays configured; these addons supplement rather than replace it.

1. Select a reviewed immutable distribution and all/cpanel/plesk ZIP. The initial distribution is a preview, not a stable production recommendation.
2. Verify the adjacent checksum with `sha256sum -c <archive>.zip.sha256`, or compare PowerShell `Get-FileHash <archive>.zip -Algorithm SHA256` with its sidecar. Extract into private staging outside the web root and verify the internal SHA256SUMS there.
3. Identify the real WHMCS root containing init.php, configuration.php and modules/addons. No credentials belong in Git, screenshots, shell history or URLs.
4. Copy only modules/addons/help4_disk_usage and/or modules/addons/help4_disk_usage_plesk into the matching WHMCS directory. Do not put root-level docs/manifests or test/native fixtures into the web root. Preserve administrator-controlled ownership and normal PHP file permissions.
5. Lint copied PHP with the WHMCS host's matching CLI. File installation never activates modules or deploys a managed server.

For a new installation, activate only the intended addon in native WHMCS Addon Modules and explicitly select administrator roles. Existing active addons do not require deactivation merely to switch source. Keep new customer reporting off until acceptance: the imported cPanel default is historically on and must be reviewed explicitly; Plesk defaults off.

For cPanel follow [the runbook](cpanel.md): current server records, SSH network access, supported PHP SSH transport, independently verified per-server pins, small bounded initial Sync and approved native Deploy/Update. Keep Allow Unpinned SSH off.

For Plesk follow [the runbook](plesk.md): separately install the native Linux/Windows extension, verify runtime/private storage, enable the bridge explicitly, use current authenticated native admin identity/trusted HTTPS, Connect the exact server and explicitly approve subscriptions. A WHMCS Plesk service record does not establish bridge installation or an approved mapping. Plesk extension deployment remains manual; Windows never receives the cPanel SSH installer.

Both addons may coexist. Distinct menus/backend capabilities remain; no cross-panel fallback or automatic conversion. Complete [native acceptance](validation.md) before customer exposure.

Built by [Help4 Network](https://help4network.com/).
