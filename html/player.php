<?php
$line1 = file_get_contents( "/tmp/radiod/line1.txt" );
$czyplayer = strpos($line1, "*");
if ($czyplayer != false) {
	list($realHost,)=explode(':',$_SERVER['HTTP_HOST']);
	echo '<audio src="http://';
	echo $realHost;
	echo ':8001/mpd" type="audio/mp3" controls="true">Your browser does not support the audio element.</audio>';
}
?>
