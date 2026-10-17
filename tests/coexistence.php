<?php
define('WHMCS', true);
$root = dirname(__DIR__);
require $root . '/modules/addons/help4_disk_usage/help4_disk_usage.php';
require $root . '/modules/addons/help4_disk_usage_plesk/help4_disk_usage_plesk.php';
$hooks = [];
function add_hook($name, $priority, $callback) { $GLOBALS['hooks'][] = [$name, $priority, $callback]; }
require $root . '/modules/addons/help4_disk_usage/hooks.php';
require $root . '/modules/addons/help4_disk_usage_plesk/hooks.php';
$cpanel = help4_disk_usage_config();
$plesk = help4_disk_usage_plesk_config();
if ($cpanel['version'] !== '1.0.2' || $plesk['version'] !== '0.3.0' || count($hooks) < 2) {
    throw new RuntimeException('Independent addon versions/hooks did not coexist');
}
if (Help4\DiskUsagePlesk\Native::MODULE !== 'help4_disk_usage_plesk' ||
    $cpanel['fields']['updateManifestUrl']['Default'] !== H4DU_DEFAULT_UPDATE_MANIFEST_URL) {
    throw new RuntimeException('Addon identity or native update target changed');
}
echo "Both addon entrypoints and hooks coexist without activation, database or network access\n";
