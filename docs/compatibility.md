# Compatibility And Capability Matrix

Distribution0.1.0 is a development preview. Remote Plesk Windows support does not mean WHMCS itself supports a Windows host. Use WHMCS's supported OS/PHP/database for its exact installed release. Test runtimes are not blanket vendor compatibility claims.

| Capability | cPanel/WHM | Plesk |
| --- | --- | --- |
| Existing addon ID/version | help4_disk_usage /1.0.2 | help4_disk_usage_plesk /0.3.0 |
| Required native component | Separate Linux cPanel/WHM plugin | Separate Linux/Windows Server Plesk extension |
| WHMCS provisioning | Existing cPanel/WHM server records | Existing native Plesk server/product records |
| Transport | Independently pinned SSH, bounded output/runtime | Authenticated verified-HTTPS XML API, nonce/install/current identity |
| Native Deploy/Update from addon | cPanel native installer/updater only | Manual native administrator operation; no Windows SSH deployment |
| Admin reports | Server health/widget, bounded sync, account drill-down |20-record health page, per-server Check, explicit mapping management |
| Customer reports | Current active service/server/username cached reports | Current User/selected Client Account/permissions/service/approved subscription |
| File Manager | Current cPanel login, Files > Disk Usage Audit | Exact retained-path native jump, existing Plesk login required |
| Limits | Shared native lock, bounded sync/account batch | User/server/admin budgets plus native bridge/scanner caps |
| Contents/deletion/login minting | Not provided | Not provided |
| Complete host hardware/service monitoring | Not provided | Not provided |

Native acceptance remains separate for each adapter and panel OS. Genuine Windows effective ACL/task/lifecycle checks are required; CI fixtures/containers cannot clear them. macOS is developer/browser only. Consult each native repository for current supported OSes versus build-limited/ELS versions; this extraction expands no native platform claim.

Built by [Help4 Network](https://help4network.com/).
