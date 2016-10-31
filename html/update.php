<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="shortcut icon" href="/PiRadio16.gif" />
	<link rel="stylesheet" href="styles.css">
	<title>PiRadio mini web interface - update confirm</title>
</head>
<body>
<b>PiRadio</b><div id="config"><a href="config.php">config</a></div></br>
<hr>
Update to last build from github<br><pre>
<?php
$end = shell_exec('sudo ./scripts/github_download.sh');
$local_version_date = filemtime("/usr/share/radio/README.md");
$local_version = str_replace("\n","",file_get_contents( "/usr/share/radio/version" ));
$github_version_date = filemtime("/usr/share/piradio-mini-master/README.md");
$github_version = str_replace("\n","",file_get_contents( "/usr/share/piradio-mini-master/version" ));
echo "Your PiRadio version: <b>".$local_version."</b>. Last commit: <b>".date("d.m.Y H:i:s",$local_version_date)."</b>.<br>";
if (is_numeric($github_version_date)) {
	echo "GitHub PiRadio version: <b>".$github_version."</b>. Last commit: <b>".date("d.m.Y H:i:s",$github_version_date)."</b>.";
	echo "<br><br>Do you really want to update your PiRadio from github repository.<br>";
	echo "<br>After update your PiRadio will be rebooted!</pre>";
} else {
	echo "<b>Problem with download update files from GitHub!!!</b>.</pre>";
}
?>
<form action="changeconf.php?file=update" method="post">
<?php if (is_numeric($github_version_date)) { ?>
<button type="submit" name="submit" value="yes">Yes - update and reboot</button>
<?php } ?>
<button type="submit" name="submit" value="no">No - no update</button>
<hr>
</body>
