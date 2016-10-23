<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="shortcut icon" href="/PiRadio16.gif" />
	<link rel="stylesheet" href="styles.css">
	<title>PiRadio mini web interface - config page</title>
</head>
<body>
<b>PiRadio</b><div id="config"><a href="index.html">radio</a></div></br>
<hr>
<?php
$msg = $_GET['file'];
if (isset($msg)) {
	if ($msg == "restart") {
		$end = "xxx";
	} elseif ($msg == "stations") {
		echo "Not implemented...";
	} elseif ($msg == "network") {
		echo "Not implemented...";
	} elseif ($msg == "rss") {
		$rss_link = $_POST["rss_link"];
		file_put_contents('/var/lib/radiod/rss', $rss_link);
		chmod("/var/lib/radiod/rss", 0755);
		$rss_link_new = file_get_contents( "/var/lib/radiod/rss" );
		echo "New RSS config:<br>";
		echo "<b>".$rss_link_new."</b>";
	} elseif ($msg == "radio") {
		$rss = (isset($_POST['rss'])) ? "rss=yes" : "rss=no";
		$bright = (isset($_POST['bright'])) ? "bright=yes" : "bright=no";
		$media_update = (isset($_POST['media_update'])) ? "media_update=yes" : "media_update=no";
		$pandora_available = (isset($_POST['pandora_available'])) ? "pandora_available=yes" : "pandora_available=no";
		$piradio = file_get_contents( "/etc/radiod.conf" );
		$piradio_new = preg_replace("/\nrss *= *.*/", "\n".$rss, $piradio);
		$piradio_new = preg_replace("/\nbright *= *.*/", "\n".$bright, $piradio_new);
		$piradio_new = preg_replace("/\nmedia_update *= *.*/", "\n".$media_update, $piradio_new);
		$piradio_new = preg_replace("/\npandora_available *= *.*/", "\n".$pandora_available, $piradio_new);
		$piradio_array = parse_ini_string($piradio_new);
		$rss = ($piradio_array['rss']) ? "yes" : "no";
		$bright = ($piradio_array['bright']) ? "yes" : "no";
		$media_update = ($piradio_array['media_update']) ? "yes" : "no";
		$pandora_available = ($piradio_array['pandora_available']) ? "yes" : "no";
		echo "New Global PiRadio config:<br>";
		echo "<b>";
		echo "RSS in standby: ".$rss."<br>";
		echo "LCD high brightness: ".$bright."<br>";
		echo "Always update library: ".$media_update."<br>";
		echo "Pandora available: ".$pandora_available."<br>";
		file_put_contents('/etc/radiod.conf', $piradio_new);
		chmod("/etc/radiod.conf", 0755);
	} elseif ($msg == "pandora") {
		$login = 'user = '.$_POST["login"];
		$password = 'password = '.$_POST["password"];
		$proxy = 'control_proxy = '.$_POST["proxy"];
		/* Folder /home/pi/.config/ musi miec uprawnienia 755
		inaczej nie da sie stad odczytac plik w nim umieszczony */
		$pandora = file_get_contents( "/home/pi/.config/pianobar/config" );
		$pandora_new = preg_replace("/\nuser *= *.*/", "\n".$login, $pandora);
		$pandora_new = preg_replace("/\npassword *= *.*/", "\n".$password, $pandora_new);
		$pandora_new = preg_replace("/\ncontrol_proxy *= *.*/", "\n".$proxy, $pandora_new);
		$pandora_array = parse_ini_string($pandora_new);
		echo "New Pandora config:<br>";
		echo "<b>";
		echo "Login: ".$pandora_array['user']."<br>";
		echo "Password: ".$pandora_array['password']."<br>";
		echo "Proxy: ".$pandora_array['control_proxy']."</b><br>";
		file_put_contents('/home/pi/.config/pianobar/config', $pandora_new);
		chmod("/home/pi/.config/pianobar/config", 0755);
	}
}
?>
<hr>
<a href="config.php?command=restart"><button>PiRadio restart</button></a>
<a href="config.php?command=reboot"><button>System reboot</button></a>
</body>
