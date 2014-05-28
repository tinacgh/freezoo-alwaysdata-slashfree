<?php

/*
Data structures:
cedict [id trad(word) simp(word) pron en]
nodeschildren [key trad(char) simp(char) children(array) data(array)]
pron [zi(char or char+'en') value(english)]
"zero" file holding children of node 0 [trad. chars and keys]

Broken chains separate accumulated words
perhaps recurse in accumFallback? But does not guarantee correctness
Real example:
Tair uan dah ge dah
becomes tair / uan / da / Ge dah
instead of (better) Tair uan / dah / Ge dah
*/

mb_language('uni');
mb_internal_encoding('UTF-8');

$dbh = new PDO('mysql:host=mysql1.alwaysdata.com;dbname=freezoo_resources',"freezoo", "123abc!");

$dbh->exec("SET NAMES 'utf8'");
$dbh->exec("SET CHARACTER SET 'utf8'");

$zeroKey = array();
$handle = @fopen("childrenofzero.txt", "r");
if ($handle) {
  while(($buffer = fgets($handle, 4096)) !== false) {
    $zeroChildren = explode(",", $buffer);
    $zeroKey[$zeroChildren[0]] = $zeroChildren[1];
  }
}
fclose($handle);

function findKey($dbh, $zeroKey, $parentKey, $zi) {
  if($parentKey == 0) {
    if(array_key_exists($zi, $zeroKey)) {
      return $zeroKey[$zi];
    }
    else {
      return -1;
    }
  } else {
    $returnVal = -1;
    $findKey_stmt = "SELECT `children` FROM `nodeschildren` WHERE `key` = :key";
    $findKey_sth = $dbh->prepare($findKey_stmt);
    $findKey_sth->execute(array(':key' => $parentKey));
    $findKey_result = $findKey_sth->fetch();
    $childrenStr = $findKey_result[0];
    $childrenArr = explode(" ", $childrenStr);

    $findZi_stmt = "SELECT `trad` FROM `nodeschildren` WHERE `key` = :key";
    $findZi_sth = $dbh->prepare($findZi_stmt);

    foreach($childrenArr as $child) {
      $findZi_sth->execute(array(':key' => $child));
      $findZi_result = $findZi_sth->fetch();
      $ziForChild = $findZi_result[0];
      if($ziForChild == $zi) {
        $returnVal = $child;
      }
    }
    return $returnVal;
  }
}


//$inp = "龍一惡鬼局Sony一對一鬥";

//$inp = "（中央社記者許雅筑台北28日電）國家通訊傳播委員會（NCC）今天公布5大電信業者的行動電話資費調整方案，調降幅度介於3.58%至6.25%之間，預估超過2800萬用戶受惠。另外，中華電信將調降ADSL電路月租費。NCC副主任委員陳正倉今天表示，新資費方案由4月起適用至明年3月。包括中華電信、台灣大哥大、遠傳電信、亞太電信及威寶電信等5大電信業者在內，手機網內外通話、撥打市話或傳簡訊等，調降幅度介於3.58%至6.25%之間。NCC依照民國99年公布的電信資費調降公式，參考物價變動，計算出今年的最低降幅。根據NCC提供數據，行動電話資費在民國99年調降幅度達5.87%以上、100年則為4.04%以上，今年再調降3.58%，3年來共調降12.90656%。以中華電信3G簡訊為例，新方案實施後，網內簡訊將由現在的每則新台幣1.1707元降至1.1287元，網外簡訊則由1.5353元降至1.4803元。依中華電信3G月租型583方案試算，若每個月打網外通話100分鐘、傳50則網外簡訊，原本每個月電話費為754元，降價後則為726元，可省下28元。NCC表示，業者必須以明顯方式揭示資費調整內容，讓用戶清楚瞭解。另外，中華電信ADSL電路月租費也將同步調降，降幅介於3.53%及3.85%間，以1M的方案為例，原本電路月租費為135元，新費率實施後將降為130元，月省5元；4M則由460元降為454元，民眾每個月可省下16元。";

$inp = "有一天，有個老人砍了不少柴，十分吃力地挑著走了很遠的路。一路上他累極了，實在挑不動了，便將擔子放下，叫喊起死神來。死神來後，問他爲 什 麽 叫喊他，老人說：“儘管我已精疲力竭了，但還是請你把那擔子放在我肩上。” 這故事說明，生活的擋子不管多重，都不要輕言放棄。";

$inp = $_POST["s"];


echo '<!DOCTYPE html>';
echo '<html>';
echo '<head>';
echo '<meta charset="UTF-8">';
echo <<<EOT
<style type="text/css">
      ruby {
        font-size: 24px;
        line-height: 300%;
      }
      rt {
        font-family: Arial, sans-serif;
        font-size: 12px;
        padding-right: 5px;
        padding-left: 5px
      }
    </style>
    <script type="text/javascript" src="/jquerymin.js"></script>
    <script type="text/javascript">
      $(document).ready(function () {
        $('#toggleRt').click(function() {
          $('rt').toggle();
        });
      });
    </script>
  </head>
  <body>
    <form action="children6.php" method="post">
      <textarea name="s" cols="60" rows="6">$inp</textarea><br><input type="submit">
      <input type="button" id="toggleRt">
    </form>
  <ruby>
EOT;
if($inp == "") {
  $inp = "Enter Chinese text above.";
}

// escape html etc in real thing

function parse($dbh, $inp, $zeroKey, $stop) {
$accumFallback = "";
$parentKey = 0;

if(mb_strlen($inp) == 1) {
  $stop = True;
}
$inp .= " ";

for ($i = 0; $i < mb_strlen($inp); $i++) {
  $curChar = mb_substr($inp, $i, 1);
  $nextChar = mb_substr($inp, $i+1, 1);
  if(array_key_exists($curChar, $zeroKey)) {
    $accumFallback .= $curChar;
  }
  $curKey = findKey($dbh, $zeroKey, $parentKey, $curChar);
  if($curKey != -1) {
    $nextKey = findKey($dbh, $zeroKey, $curKey, $nextChar);
    if($nextKey == -1) {
      $checkData_stmt = "SELECT `data` FROM `nodeschildren` WHERE `key` = :key";
      $checkData_sth = $dbh->prepare($checkData_stmt); 
      $checkData_sth->execute(array(':key' => $curKey));
      $checkData_result = $checkData_sth->fetch();
      $curData = $checkData_result[0];
      if($curData != "") {
        $outPron = "";
        $outRT = "";
        $outEn = "";
        $dataArr = explode(" ", $curData);
        foreach($dataArr as $dataref) {
          $cedict_stmt = "SELECT `pron`, `en` FROM `cedict` WHERE `id` = :id";
          $cedict_sth = $dbh->prepare($cedict_stmt);
          $cedict_sth->execute(array(':id' => $dataref));
          $cedict_result = $cedict_sth->fetch();

          if (strlen($cedict_result[pron]) > 0) {
            $outPron = "[" . $cedict_result[pron] . "] ";
            $outRT .= $cedict_result[pron] . "<br />";
            $outEn .= $outPron . " " . str_replace('"', '&quot;', $cedict_result[en]) . " ";
          }
        }
        echo "$cedict_result[2] <rb title=\"$outEn\">$accumFallback</rb><rt>$outRT</rt>";

        $outPron = "";
        $outEn = "";
      }
      else {
        /* for ($j = 0; $j < mb_strlen($accumFallback); $j++) {
            $pronFallback_stmt = "SELECT `value` FROM `pron` WHERE `zi` = :zi";
            $pronFallback_sth = $dbh->prepare($pronFallback_stmt);
            $pronFallback_sth->execute(array(':zi' => mb_substr($accumFallback, $j, 1)));
            $pronFallback_result = $pronFallback_sth->fetch();
            $pronFall = $pronFallback_result[0];

            $pronFallbackEn_stmt = "SELECT `value` FROM `pron` WHERE `zi` = :zi";
            $pronFallbackEn_sth = $dbh->prepare($pronFallback_stmt);
            $pronFallbackEn_sth->execute(array(':zi' => mb_substr($accumFallback, $j, 1) . "en"));
            $pronFallbackEn_result = $pronFallbackEn_sth->fetch();
            $pronFallEn = str_replace('"', '&quot;', $pronFallbackEn_result[0]);


            $outPronFallback = str_replace(" ", "<br />", $pronFall);
            echo "<rb title=\"$pronFallEn\">" . mb_substr($accumFallback, $j, 1) . "</rb><rt>$outPronFallback</rt>"; */

          if (!$stop) {
            parse($dbh, mb_substr($accumFallback, 0, mb_strlen($accumFallback) - 1), $zeroKey, False);
            parse($dbh, mb_substr($accumFallback, mb_strlen($accumFallback) - 1, 1), $zeroKey, False);
          }
        
    
      }
      $accumFallback = "";
      $parentKey = 0;
    }
    else {
        $parentKey = $curKey;
    }
  } 
  else {
    echo("<rb>$curChar</rb><rt>&nbsp;</rt>");
  }
}
}

parse($dbh, $inp, $zeroKey, False);


echo <<<EOT
  </ruby>Uses CC-CEDICT
</body></html>
EOT;
$dbh = null;

?>