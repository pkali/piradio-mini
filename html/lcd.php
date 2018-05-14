<?php
$msg = $_GET['scroll'];
if ($msg=="True") {
	$line1 = file_get_contents( "/tmp/radiod/line1s.txt" );
	$line2 = file_get_contents( "/tmp/radiod/line2s.txt" );
	$line3 = file_get_contents( "/tmp/radiod/line3s.txt" );
	$line4 = file_get_contents( "/tmp/radiod/line4s.txt" );
} else {
	$line1 = file_get_contents( "/tmp/radiod/line1.txt" );
	$line2 = file_get_contents( "/tmp/radiod/line2.txt" );
	$line3 = file_get_contents( "/tmp/radiod/line3.txt" );
	$line4 = file_get_contents( "/tmp/radiod/line4.txt" );
}
$line1 = str_replace(" ","&nbsp;",$line1);
$line2 = str_replace(" ","&nbsp;",$line2);
$line3 = str_replace(" ","&nbsp;",$line3);
$line4 = str_replace(" ","&nbsp;",$line4);
echo $line1;
echo "</br>";
echo $line2;
echo "</br>";
echo $line3;
echo "</br>";
echo $line4;
echo "</br>";
?>
