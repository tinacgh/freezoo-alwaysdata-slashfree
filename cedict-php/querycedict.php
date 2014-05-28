<?php
mb_language('uni');
mb_internal_encoding('UTF-8');

$dbh = new PDO('mysql:host=mysql1.alwaysdata.com;dbname=freezoo_resources',"freezoo", "123abc!");


$dbh->exec("SET NAMES 'utf8'");
$dbh->exec("SET CHARACTER SET 'utf8'");

echo '<!DOCTYPE html>';
echo '<html>';
echo '<head>';
echo '<meta charset="UTF-8">';
echo '<style type="text/css">';
echo ' body { font-size: 12px; }';
echo ' .zi { font-size: 20px; }';
echo '</style>';
echo '</head>';

$pron = $_GET["pron"];

$stmt = "SELECT * FROM `cedict` WHERE `pron`=:pron";
$sth = $dbh->prepare($stmt);
$sth->execute(array(':pron' => $pron));
$result = $sth->fetchAll();

echo "<body onload=\"document.getElementById('text_pron').focus()\">";
echo "Uses CC-CEDICT <br>";
echo <<<EOT
  <form action="querycedict.php" method="get">
    <input type="text" id="text_pron" name="pron">
    <input type="submit">
  </form>
EOT;
echo $pron;

echo "<table>";
for($i = 0; $i < count($result); $i++) {
  echo "<tr><td class='zi'>{$result[$i]['trad']}</td><td>{$result[$i]['pron']}</td><td>{$result[$i]['en']}</td></tr>";
}
?>