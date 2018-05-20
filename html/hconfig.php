<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="shortcut icon" href="/PiRadio16.gif" />
	<link rel="stylesheet" href="styles.css">
	<title>PiRadio mini web interface - hardware config page</title>
</head>
<body>
<?php
$piradio_version = str_replace("\n","",file_get_contents( "/usr/share/radio/version" ));
echo "<b>PiRadio v. ".$piradio_version."</b>";
?>
<div id="config"><a href="config.php">config</a></div></br>
<hr>
Audio device config<br>
<form action="changeconf.php?file=audio" method="post">
<b><pre>
<?php
$hqa = file_get_contents( "/boot/config.txt" );
preg_match('/\n *audio_pwm_mode *=.*/', $hqa, $matches);
$hqa_v = preg_replace("/\n *audio_pwm_mode *= */", "", $matches[0]);
$audio = file_get_contents( "/lib/modprobe.d/aliases.conf" );
preg_match('/\n# USB audio card as first device/', $audio, $matches);
$audio_usb = isset($matches[0]);
preg_match('/\n# Internal audio card as first device/', $audio, $matches);
$audio_int = isset($matches[0]);
echo '  <input type="radio" name="output" value="internal" ';
if ( $audio_int ) {
  echo 'checked';
}
echo '> internal audio  (<input type="checkbox" name="hda" value="hdaudio" ';
if ( $hqa_v == 2 ) {
  echo 'checked>';
  } else {
  echo '>';
  }
echo ' - high quality output)'."\n";
echo '  <input type="radio" name="output" value="usb" ';
if ( $audio_usb ) {
  echo 'checked';
}
echo '> USB audio card<br>'."\n";
echo '<input type="hidden" name="output_old" value="';
if ( $audio_int ) {
  echo 'internal';
} elseif ( $audio_usb ) {
  echo "usb";
} else {
  echo "none";
}
echo '">';
echo '<input type="hidden" name="hda_old" value="';
if ( $hqa_v == 2 ) {
  echo 'hdaudio';
}
echo '">';
?>
  <button type="submit" name="submit">Save audio device config and reboot</button>
</pre></b>
</form>
<hr>
Remote config<br>
<form action="changeconf.php?file=remote" method="post">
<b><pre>
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
		echo "> ".$remotename;
		if ($i < count($remoteconfigs)-1) {
			echo "\n";
		} else {
			echo "<br>\n";
		}
	}
}
?>
  <button type="submit" name="submit">Save remote config and reboot</button>
</pre></b>
</form>
<hr>
Update to last build from github<br>
<b><pre>
<?php
$local_version_date = filemtime("/usr/share/radio/README.md");
$local_version = str_replace("\n","",file_get_contents( "/usr/share/radio/version" ));
$github_version_date = filemtime("/usr/share/piradio-mini-master/README.md");
$github_version = str_replace("\n","",file_get_contents( "/usr/share/piradio-mini-master/version" ));
echo "Your PiRadio version: <b>".$local_version."</b>. Last commit: <b>".date("d.m.Y H:i:s",$local_version_date)."</b>.";
?>
<br>
<a href="update.php"><button>PiRadio update</button></a>
</pre></b>
<hr>
Maintenance<br>
<b><pre>
<?php
$end = shell_exec("df | grep '/dev/root'");
$end = preg_replace('/\s+/', ' ', $end);
$end=trim($end);
$values = explode(" ", $end);
$system_capacity = floatval($values[1]);
$system_free = floatval($values[3]);
$system_capacity = $system_capacity/1024;
$system_free = $system_free/1028;
echo "PiRadio SD card size: ".round($system_capacity,2)." MB.<br>";
echo "free: ".round($system_free,2)." MB (".$values[4]." used)<br>";
?>
<br><a href="changeconf.php?file=clear_caches"><button>Clear logs and caches</button></a><br>
<?php
$end = shell_exec("uname -a");
echo $end."<br>";
?>
<form action="changeconf.php?file=rpi_update" method="post"><button type="submit" name="submit" value="confirm">Raspberry Pi update</button></form></pre></b>
<hr>
<a href="changeconf.php?file=restart"><button>PiRadio restart</button></a>
<a href="changeconf.php?file=reboot"><button>System reboot</button></a>
</body>
</html>