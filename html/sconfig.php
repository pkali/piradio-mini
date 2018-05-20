<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="shortcut icon" href="/PiRadio16.gif" />
	<link rel="stylesheet" href="styles.css">
	<title>PiRadio mini web interface - configuration backup and restore</title>
</head>
<body>
<?php
$piradio_version = str_replace("\n","",file_get_contents( "/usr/share/radio/version" ));
echo "<b>PiRadio v. ".$piradio_version."</b>";
?>
<div id="config"><a href="config.php">config</a></div></br>
<hr>
<?php
$selected = $_FILES['file'];
if (isset($selected)) {
	if ($_FILES["file"]["error"] > 0)
	{
		echo "Error: " . $_FILES["file"]["error"] . "<br>";
	} else {
		echo "File: ";
		echo  $_FILES["file"]["name"] ;
		echo " loaded.<br>\r\n";
		move_uploaded_file($_FILES["file"]["tmp_name"], "/tmp/piradio.set");
		$tablica = explode('.', $_FILES["file"]["name"]);
		$ostatni = count($tablica);
		if($tablica[$ostatni-1] == 'set') {
			$end = shell_exec('sudo ./scripts/restore_config.sh unpack');
			if (file_exists("/tmp/radiod/config/version")) {
				echo "Setting new configuration.<br>\r\n";
				$end = shell_exec('sudo ./scripts/restore_config.sh apply');
				echo "O.K.<br>\r\n";
				$end = shell_exec('sudo ./scripts/reboot.sh');
				/* UWAGA! Folder z plikami uruchamianymi przez sudo
				musi byc dopisany w pliku /etc/sudoers     */
				echo "Reboot in progress.<br>\r\n";
				echo "Wait!<br>\r\n";
				echo "<script>\r\n";
				echo "// redirect to main after 30 seconds\r\n";
				echo "window.setTimeout(function() {\r\n";
				echo "  window.location.href = 'index.php';\r\n";
				echo "}, 30000);\r\n";
				echo "</script>\r\n";
			} else {
				echo "This is not PiRadio config file!!!<br>\r\n";
				echo "<script>\r\n";
				echo "// redirect to main after 2 seconds\r\n";
				echo "window.setTimeout(function() {\r\n";
				echo "  window.location.href = 'index.php';\r\n";
				echo "}, 2000);\r\n";
				echo "</script>\r\n";
			}
		} else {
			unlink("/tmp/piradio.set");
			echo "This is wrong file!<br>\r\n";
			echo "<script>\r\n";
			echo "// redirect to main after 2 seconds\r\n";
			echo "window.setTimeout(function() {\r\n";
			echo "  window.location.href = 'index.php';\r\n";
			echo "}, 2000);\r\n";
			echo "</script>\r\n";
		}
	}
} else {
	$end = shell_exec('sudo ./scripts/make_config_file.sh');
	echo "Backup PiRadio configuration<br>\r\n";
	echo "<pre>\r\nClick the 'Backup' button to download the configuration backup file to your computer.\r\n</pre>\r\n";
	echo '<a href="piradio.set"><button>Backup</button></a>';
	echo "<hr>\r\n";
	echo "Restore PiRadio configuration<br>\r\n";
	echo "<b><pre>After restoringing the reboot will be performed!</pre></b>\r\n";
	echo "<form action='sconfig.php' method='post' enctype='multipart/form-data'>\r\n";
	echo "  <pre><label for='file'>Please select a file to restore:</label></pre>\r\n";
	echo "  <input type='hidden' name='MAX_FILE_SIZE' value='30000'>\r\n";
	echo "  <input name='file' type='file' id='file'><br>\r\n";
	echo "  <button type='submit' name='submit'>Restore</button>\r\n";
	echo "</form>\r\n";
}
?>
<hr>
<a href="changeconf.php?file=restart"><button>PiRadio restart</button></a>
<a href="changeconf.php?file=reboot"><button>System reboot</button></a>
</body>
</html>