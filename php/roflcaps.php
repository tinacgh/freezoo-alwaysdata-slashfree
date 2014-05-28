<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title> </title>
    <script type="text/javascript">

    </script>
  </head>
  <body>
    <?php
       $input = strip_tags($_POST['in']);
       for ($i = 0; $i < strlen($input); $i++) {
         if(rand(0,1)) {
           echo strtoupper($input[$i]);
         }
	 else {
	   echo strtolower($input[$i]);
         }
       }
    ?>
    <form action="roflcaps.php" method="POST">
      <input name="in">
      <input type="submit">
    </form>
  </body>
</html>
