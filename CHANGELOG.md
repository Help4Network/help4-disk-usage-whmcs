# Changelog

## 0.1.0 Development Preview

- Establish one standalone WHMCS repository for cPanel/WHM and Plesk Linux/Windows integrations.
- Preserve twelve imported runtime files, existing addon IDs, module versions, private table names, protected credentials and backend-specific transport/security controls.
- Separate distribution version, packaging, installation and upgrade ownership from both native panel repositories.
- Supply combined and backend-specific WHMCS-only archives with exact inventories and internal/outer checksums. Native installers/collectors/test fixtures are excluded.
- Move customer isolation, transport, report, lifecycle/framework, health and service-selection fixtures with the addons, with pinned native protocol fixtures and distinct coexistence/package tests.
- Keep the native Plesk bridge in its own repository and exercise the source contract across independently pinned repositories on Linux/Windows CI.
- Preserve all native WHMCS/MySQL/TLS/role, Linux/Windows panel/lifecycle and explicit stable approval gates. This extraction performs no production activation, schema renaming, deployment or final launch.

Built by [Help4 Network](https://help4network.com/).
