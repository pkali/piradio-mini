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
Global PiRadio config<br>
<form action="changeconf.php?file=radio" method="post">
<pre>
<?php
$piradio = file_get_contents( "/etc/radiod.conf" );
$piradio_array = parse_ini_string($piradio);
$write_conf = false;
if (!isset($piradio_array['startup'])) {
	$piradio = $piradio."\r\n# Startup option either RADIO, MEDIA (USB stick) or PANDORA\r\nstartup=RADIO\r\n";
	$write_conf = true;
}
if (!isset($piradio_array['rss'])) {
	$piradio = $piradio."\r\n# RSS in standby (Pecus)\r\nrss=no\r\n";
	$write_conf = true;
}
if (!isset($piradio_array['bright'])) {
	$piradio = $piradio."\r\n# LCD backlight high brightness (Pecus)\r\nbright=no\r\n";
	$write_conf = true;
}
if (!isset($piradio_array['media_update'])) {
	$piradio = $piradio."\r\n# Always (after switch to media player) update media library (Pecus)\r\nmedia_update=no\r\n";
	$write_conf = true;
}
if (!isset($piradio_array['pandora_available'])) {
	$piradio = $piradio."\r\n# Is Pandora account available (Pecus)\r\npandora_available=no\r\n";
	$write_conf = true;
}
if (!isset($piradio_array['volume_min'])) {
	$piradio = $piradio."\r\nvolume_min=0\r\n";
	$write_conf = true;
}
if (!isset($piradio_array['volume_max'])) {
	$piradio = $piradio."\r\nvolume_max=100\r\n";
	$write_conf = true;
}
if ($write_conf) {
	file_put_contents('/etc/radiod.conf', $piradio);
}
echo "<b>";
echo '<input type="checkbox" name="rss" value="rss" ';
if ( $piradio_array['rss'] ) {
  echo 'checked>';
  } else {
  echo '>';
  }
echo ' RRS in standby.<br>';
echo '<input type="checkbox" name="bright" value="bright" ';
if ( $piradio_array['bright'] ) {
  echo 'checked>';
  } else {
  echo '>';
  }
echo ' LCD high brightness.<br>';
echo '<input type="checkbox" name="media_update" value="media_update" ';
if ( $piradio_array['media_update'] ) {
  echo 'checked>';
  } else {
  echo '>';
  }
echo ' Always update library.<br>';
echo '<input type="checkbox" name="pandora_available" value="pandora_available" ';
if ( $piradio_array['pandora_available'] ) {
  echo 'checked>';
  } else {
  echo '>';
  }
echo ' Pandora available.';
echo '</b><br>';
echo "Startup source: <select name='startup'>\r\n";
echo "  <option value='RADIO'";
if ( $piradio_array['startup'] == 'RADIO' ) {
  echo "selected>";
  } else {
  echo ">";
  }
echo "SHOUTcast radio</option>\r\n";
echo "  <option value='MEDIA'";
if ( $piradio_array['startup'] == 'MEDIA' ) {
  echo "selected>";
  } else {
  echo ">";
  }
echo "Media player</option>\r\n";
echo "  <option value='PANDORA'";
if ( $piradio_array['startup'] == 'PANDORA' ) {
  echo "selected>";
  } else {
  echo ">";
  }
echo "Pandora radio</option>\r\n";
echo "</select>\r\n";
?>
<button type="submit" name="submit">Save Global PiRadio config</button>
</pre>
</form>
<pre>
<?php
$local_version_date = filemtime("/usr/share/radio/README.md");
$local_version = str_replace("\n","",file_get_contents( "/usr/share/radio/version" ));
$github_version_date = filemtime("/usr/share/piradio-mini-master/README.md");
$github_version = str_replace("\n","",file_get_contents( "/usr/share/piradio-mini-master/version" ));
echo "Your PiRadio version: <b>".$local_version."</b>. Last commit: <b>".date("d.m.Y H:i:s",$local_version_date)."</b>.";
?>
</pre>
<a href="hconfig.php"><button>Hardware Configuration & Update</button></a>
<hr>
Media network folder config
<form action="changeconf.php?file=network" method="post">
<?php
/* Folder /var/lib/radiod/ musi miec uprawnienia 755
   inaczej nie da sie stad odczytac plik w nim umieszczony */
$netshare = file_get_contents( "/var/lib/radiod/share" );
preg_match('/user=\".*\",pass/', $netshare, $matches);
preg_match('/\".*\"/', $matches[0], $matches);
$share_user = substr($matches[0], 1 ,-1);
preg_match('/password=\".*\",ro/', $netshare, $matches);
preg_match('/\".*\"/', $matches[0], $matches);
$share_password = substr($matches[0], 1 ,-1);
preg_match('/ro \".*\"/', $netshare, $matches);
preg_match('/\".*\"/', $matches[0], $matches);
$share_link = substr($matches[0], 1 ,-1);
echo "<pre><b>";
echo "Network path: <input type='text' name='media_link' value='".$share_link."' style='width: 80%'><br>";
echo "Login: <input type='text' name='user' value='".$share_user."'><br>";
echo "Password: <input type='text' name='password' value='".$share_password."'></b><br>";
?>
<button type="submit" name="submit" value="confirm">Save network folder config</button>
</pre></form>
<hr>
RSS config
<form action="changeconf.php?file=rss" method="post">
<?php
/* Folder /var/lib/radiod/ musi miec uprawnienia 755
   inaczej nie da sie stad odczytac plik w nim umieszczony */
$rss = file_get_contents( "/var/lib/radiod/rss" );
echo "<input type='text' name='rss_link' value='";
echo $rss;
echo "' style='width: 100%'>";
?>
<br><button type="submit" name="submit">Save RSS config</button>
</form>
<hr>
Pandora config
<form action="changeconf.php?file=pandora" method="post"><pre>
<?php
/* Folder /home/pi/.config/ musi miec uprawnienia 755
   inaczej nie da sie stad odczytac plik w nim umieszczony */
$pandora = file_get_contents( "/home/pi/.config/pianobar/config" );
$pandora_array = parse_ini_string($pandora);
/* print_r($pandora_array); */
echo "<b>";
echo "Login: <input type='text' name='login' value='".$pandora_array['user']."'><br>";
echo "Password: <input type='text' name='password' value='".$pandora_array['password']."'><br>";
echo "Proxy: <input type='text' name='proxy' value='".$pandora_array['control_proxy']."'></b><br>";
?>
<button type="submit" name="submit">Save Pandora config</button>
</pre></form>
<hr>
Radio stations config
<form action="changeconf.php?file=stations" method="post">
<?php
/* Folder /var/lib/radiod/ musi miec uprawnienia 755
   inaczej nie da sie stad odczytac plik w nim umieszczony */
$stations = file_get_contents( "/var/lib/radiod/stationlist" );
echo '<textarea rows="20" name="stations" style="width: 100%">';
echo $stations;
echo '</textarea>';
?>
<br><button type="submit" name="submit" value="new">Save radio stations list</button>
<button type="submit" name="submit" value="old">Restore previous list</button>
</form>
<hr>
<a href="changeconf.php?file=restart"><button>PiRadio restart</button></a>
<a href="changeconf.php?file=reboot"><button>System reboot</button></a>
</body>
