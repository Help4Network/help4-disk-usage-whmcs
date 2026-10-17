# Migration, Upgrade, Rollback And Removal

## Move From A Native Panel Repository

Source ownership and packaging change, not installed identity. cPanel retains help4_disk_usage/version1.0.2 and mod_help4_disk_usage_servers/accounts/events. Plesk retains help4_disk_usage_plesk/version0.3.0 and mod_help4_du_plesk_servers/bindings/limits. Never rename addons, merge their data, drop tables or deactivate/reactivate a working installation merely to switch package source.

1. Record exact addon/WHMCS/native identities and reviewed candidate commit without exposing customer observations or credentials.
2. Test/build an immutable standalone source revision. Distribution VERSION is separate from each addon and native panel version.
3. Quiesce admitted addon work. Replace only the intended directory with verified staged runtime, preserving owner/PHP compatibility. Do not weaken pins to make a changed endpoint connect.
4. Follow native WHMCS addon upgrade behavior when the addon version changes. The initial extraction preserves module versions; distribution0.1.0 does not itself imply a schema migration. Verify settings, roles and private tables after replacement.
5. Test current admin/customer scopes, rejected foreign/changed ownership, mappings, bounded transport and actual panel destinations. Git pull and PHP lint are not deployment/acceptance evidence.

Native repositories no longer own addon runtime/artifacts after their matching extraction commits. Historical immutable releases remain historical; do not rewrite/delete their assets or checksums. Keep native plugins installed separately, using their own lifecycle/update channel. Test fixtures here are never native installation payloads.

## Independent Updates

Review this repository's releases, immutable commit and components.json, then build/verify/deploy addon files. Native cPanel Check/Deploy/Update and native Plesk Software updates continue targeting their own repositories; neither updates WHMCS addon files. No automatic download-and-execute addon updater is supplied.

## Rollback And Removal

Keep an identified prior immutable addon ZIP/checksum as rollback source; no routine snapshots. Quiesce requests and review private schema/mapping compatibility before restoring code. Never overwrite WHMCS core configuration or disable transport verification.

For removal disable customer reporting, stop new actions, wait for admitted operations, disconnect intended Plesk mappings if appropriate, deactivate the intended addon through WHMCS and remove only its files. Private addon tables are intentionally retained. Dropping tables requires separate explicit administrator authority and retention/quiescence review; there is no automatic purge. Addon removal does not uninstall panel plugins or delete hosting files, services, invoices or tickets.

Built by [Help4 Network](https://help4network.com/).
