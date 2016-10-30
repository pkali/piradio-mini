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
Update to last build from github
<a href="update.php"><button>PiRadio update</button></a>
<hr>
<a href="changeconf.php?file=restart"><button>PiRadio restart</button></a>
<a href="changeconf.php?file=reboot"><button>System reboot</button></a>
</body>
