<?php

// to compress
$tocomp = $_GET['plain'];

// to uncompress
$touncomp = $_GET['code'];

$thecode = bin2hex(gzcompress($tocomp));

echo $thecode;

echo gzuncompress(convert_uudecode($touncomp));

echo <<<EOT
<form action="compression.php" method="GET">
<textarea name="plain" rows="10"></textarea>
<input type="submit">
</form>
EOT;

echo "<a href=\"compression.php?code=$thecode\">uncompress</a>";

?>