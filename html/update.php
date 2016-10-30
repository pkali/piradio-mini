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
Update to last build from github<br><br>
Do you really want to update your PiRadio from github repository.<br>
After update your PiRadio will be rebooted!
<form action="changeconf.php?file=update" method="post">
<button type="submit" name="submit" value="yes">Yes - update and reboot</button>
<button type="submit" name="submit" value="no">No - no update</button>
<hr>
</body>
