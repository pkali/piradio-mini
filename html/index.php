<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="shortcut icon" href="/PiRadio16.gif" />
	<link rel="stylesheet" href="styles.css">
	<title>PiRadio mini web interface</title>
	<script src="jquery-1.12.4.min.js"></script>
	<?php
	require_once 'libs/Mobile_Detect.php';
	$detect = new Mobile_Detect;
	if ( $detect->isMobile() ) {
		echo "<script>\r\n";
		echo "$(document).ready(function() {\r\n";
		echo "	$('#wyswietlacz').load('lcd.php?scroll=True');\r\n";
		echo "	var refreshId = setInterval(function() {\r\n";
		echo "		$('#wyswietlacz').load('lcd.php?scroll=True');\r\n";
		echo "	}, 200);\r\n";
		echo "	$.ajaxSetup({ cache: false });\r\n";
		echo "	$('#player').load('player.php');\r\n";
		echo "});\r\n";
		echo "</script>\r\n";
	} else {
		echo "<script>\r\n";
		echo "$(document).ready(function() {\r\n";
		echo "	$('#wyswietlacz').load('lcd.php?scroll=False');\r\n";
		echo "	var refreshId = setInterval(function() {\r\n";
		echo "		$('#wyswietlacz').load('lcd.php?scroll=False');\r\n";
		echo "	}, 200);\r\n";
		echo "	$.ajaxSetup({ cache: false });\r\n";
		echo "	$('#player').load('player.php');\r\n";
		echo "});\r\n";
		echo "</script>\r\n";
	}
	?>
</head>
<body>
<?php
$piradio_version = str_replace("\n","",file_get_contents( "/usr/share/radio/version" ));
echo "<b>PiRadio v. ".$piradio_version."</b>";
?>
<div id="config"><a href="config.php">config</a></div><hr>
<div id="wyswietlacz">
<br><br><br><br>
</div>
<div id="kursory">
<button id="UPbutton">^</button><br>
<button id="LEFTbutton">&lt;</button>
<button id="OKbutton">OK</button>
<button id="RIGHTbutton">&gt;</button><br>
<button id="DOWNbutton">v</button>
<div id="speak">
<button id="LGbutton">LANGUAGE</button><br>
<button id="INFObutton">INFO</button><br>
<button id="STREAMTbutton">STREAM ON/OFF</button>
</div>
</div>
<div id="lewebuttony">
<button id="SLEEPbutton">&nbsp;&nbsp;SLEEP&nbsp;&nbsp;</button>
<button id="WAKEUPbutton">WAKEUP</button>
<br>
<button id="CHDOWNbutton">|&lt;&lt; PREV</button>
<button id="CHUPbutton">NEXT &gt;&gt;|</button>
<br>
<button id="RADIObutton">&nbsp;RADIO&nbsp;</button>
<button id="MEDIAbutton">PLAYER</button>
<button id="PANDORAbutton">PANDORA</button>
</div>
<div id="nadole">
<button id="VDOWNbutton">V-</button>
<button id="MUTEbutton">MUTE</button>
<button id="VUPbutton">V+</button>
<button id="TIMERbutton">SLEEP TIMER</button>
<div id="player">
</div>
</div>
<script>
 $("#OKbutton").click(function() {
   $.post("button.php?key=KEY_OK");
 });
 $("#UPbutton").click(function() {
   $.post("button.php?key=KEY_UP");
 });
 $("#DOWNbutton").click(function() {
   $.post("button.php?key=KEY_DOWN");
 });
 $("#LEFTbutton").click(function() {
   $.post("button.php?key=KEY_LEFT");
 });
 $("#RIGHTbutton").click(function() {
   $.post("button.php?key=KEY_RIGHT");
 });
 $("#SLEEPbutton").click(function() {
   $.post("button.php?key=KEY_SLEEP");
   setTimeout(function(){
     $("#player").load("player.php");
   }, 1500);
 });
 $("#WAKEUPbutton").click(function() {
   $.post("button.php?key=KEY_WAKEUP");
   setTimeout(function(){
     $("#player").load("player.php");
   }, 1500);
 });
 $("#CHUPbutton").click(function() {
   $.post("button.php?key=KEY_CHANNELUP");
 });
 $("#CHDOWNbutton").click(function() {
   $.post("button.php?key=KEY_CHANNELDOWN");
 });
 $("#VUPbutton").click(function() {
   $.post("button.php?key=KEY_VOLUMEUP");
 });
 $("#VDOWNbutton").click(function() {
   $.post("button.php?key=KEY_VOLUMEDOWN");
 });
 $("#LGbutton").click(function() {
   $.post("button.php?key=KEY_LANGUAGE");
 });
 $("#INFObutton").click(function() {
   $.post("button.php?key=KEY_INFO");
 });
 $("#MUTEbutton").click(function() {
   $.post("button.php?key=KEY_MUTE");
 });
 $("#TIMERbutton").click(function() {
   $.post("button.php?key=KEY_TIME");
 });
 $("#RADIObutton").click(function() {
   $.post("button.php?key=KEY_RADIO");
 });
 $("#MEDIAbutton").click(function() {
   $.post("button.php?key=KEY_MEDIA");
 });
 $("#PANDORAbutton").click(function() {
   $.post("button.php?key=KEY_PANDORA");
 });
 $("#STREAMTbutton").click(function() {
   $.post("button.php?key=STREAMING_TOGGLE");
   setTimeout(function(){
     $("#player").load("player.php");
   }, 4000);
 });
</script>
</body>
