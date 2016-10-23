<?php
$msg = $_GET['key'];
if (isset($msg)) {
  $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
  $len = strlen($msg);
  socket_sendto($sock, $msg, $len, 0, 'localhost', 5100);
  socket_close($sock);
}
?>
