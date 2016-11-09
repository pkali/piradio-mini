<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="shortcut icon" href="/PiRadio16.gif" />
	<link rel="stylesheet" href="styles.css">
	<title>PiRadio mini web interface - hardware config page</title>
</head>
<body>
<b>PiRadio</b><div id="config"><a href="config.php">config</a></div></br>
<hr>
Audio device config<br>
<form action="changeconf.php?file=audio" method="post">
<pre>
  <input type="radio" name="output" value="internal" checked> internal audio
  <input type="radio" name="output" value="USB"> USB audio card<br>
<button type="submit" name="submit">Save audio device config</button>
</pre>
</form>
<hr>
Remote config<br>
<form action="changeconf.php?file=remote" method="post">
<pre>
<?php
$remote = file_get_contents( "/etc/lirc/lircd.conf" );
preg_match('/\n# *brand: *.*/', $remote, $matches);
$currentremotename = preg_replace("/\n# *brand: */", "", $matches[0]);
$dir    = '/usr/share/radio/hardware/remotes/';
$remoteconfigs = scandir($dir);
for ($i = 0; $i < count($remoteconfigs); $i++) {
	if (preg_match('/.conf/',$remoteconfigs[$i])) {
		$remote = file_get_contents( "/usr/share/radio/hardware/remotes/".$remoteconfigs[$i] );
		preg_match('/\n# *brand: *.*/', $remote, $matches);
		$remotename = preg_replace("/\n# *brand: */", "", $matches[0]);
		echo '  <input type="radio" name="remote" value="';
		echo $remoteconfigs[$i].'"';
		if ($remotename==$currentremotename) {
			echo ' checked';
		}
		echo "> ".$remotename."\n";
	}
}
?>
<br><button type="submit" name="submit">Save remote config and reboot</button>
</pre>
</form>
<hr>
Update to last build from github
<a href="update.php"><button>PiRadio update</button></a>
<hr>
<a href="changeconf.php?file=restart"><button>PiRadio restart</button></a>
<a href="changeconf.php?file=reboot"><button>System reboot</button></a>
</body>
