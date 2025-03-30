<?php
session_start();

$session_id = session_id();
$target_dir = "/var/www/html/uploads/$session_id/";

// Creating the session-specific upload directory if it doesn't exist
if (!is_dir($target_dir)) {
    mkdir($target_dir, 0755, true);
    chown($target_dir, 'www-data');
    chgrp($target_dir, 'www-data');
}
?>
<!DOCTYPE html>
<html>
  <title>Ascii Art Submissions</title>
  <h1>Ascii Art Submissions</h1>
  <style>
        body {
            font-family: monospace;
            background-color: #f0f0f0;
            text-align: center;
        }
        pre {
            display: inline-block;
            text-align: left;
            background-color: #fff;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
    </style>
<div>
  <p>Submit your best ascii art here!</p>
  <pre>
  /$$$$$$                      /$$ /$$        /$$$$$$              /$$    
 /$$__  $$                    |__/|__/       /$$__  $$            | $$    
| $$  \ $$  /$$$$$$$  /$$$$$$$ /$$ /$$      | $$  \ $$  /$$$$$$  /$$$$$$  
| $$$$$$$$ /$$_____/ /$$_____/| $$| $$      | $$$$$$$$ /$$__  $$|_  $$_/  
| $$__  $$|  $$$$$$ | $$      | $$| $$      | $$__  $$| $$  \__/  | $$    
| $$  | $$ \____  $$| $$      | $$| $$      | $$  | $$| $$        | $$ /$$
| $$  | $$ /$$$$$$$/|  $$$$$$$| $$| $$      | $$  | $$| $$        |  $$$$/
|__/  |__/|_______/  \_______/|__/|__/      |__/  |__/|__/         \___/  
                                                                          
  </pre>
  </br>
  <pre>
               ,----------------,              ,---------,
        ,-----------------------,          ,"        ,"|
      ,"                      ,"|        ,"        ,"  |
     +-----------------------+  |      ,"        ,"    |
     |  .-----------------.  |  |     +---------+      |
     |  |                 |  |  |     | -==----'|      |
     |  |  C:\>Submit     |  |  |/----|`---=    |      |
     |  |  C:\>Art.txt :D |  |  |   ,/|==== ooo |      ;
     |  |                 |  |  |  // |(((( [33]|    ,"
     |  `-----------------'  |," .;'| |((((     |  ,"
     +-----------------------+  ;;  | |         |,"     
        /_)______________(_/  //'   | +---------+
   ___________________________/___  `,
  /  oooooooooooooooo  .o.  oooo /,   \,"-----------
 / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
/_==__==========__==_ooo__ooo=_/'   /___________,"
  </pre>
</div>
<div>
  <h2>Submit your art</h2>
  <p>Submit the ASCII art here. Submissions will be hidden until after they are judged!</p>
  <form action="/" method="post" enctype="multipart/form-data">
    <input type="file" name="fileToUpload" id="fileToUpload"><br>
    <input type="submit" value="Submit Art" name="submit">
  </form>
<?php

if (isset($_FILES['fileToUpload'])) {
    $target_file = basename($_FILES["fileToUpload"]["name"]);
    $session_id = session_id();
    $target_dir = "/var/www/html/uploads/$session_id/";
    $target_file_path = $target_dir . $target_file;
    $uploadOk = 1;
    $lastDotPosition = strrpos($target_file, '.');

    // Check if file already exists
    if (file_exists($target_file_path)) {
        echo "Sorry, file already exists.\n";
        $uploadOk = 0;
    }
    
    // Check file size
    if ($_FILES["fileToUpload"]["size"] > 50000) {
        echo "Sorry, your file is too large.\n";
        $uploadOk = 0;
    }

    // If the file contains no dot, evaluate just the filename
    if ($lastDotPosition == false) {
        $filename = substr($target_file, 0, $lastDotPosition);
        $extension = '';
    } else {
        $filename = substr($target_file, 0, $lastDotPosition);
        $extension = substr($target_file, $lastDotPosition + 1);
    }

    // Ensure that the extension is a txt file
    if ($extension !== '' && $extension !== 'txt') {
        echo "Sorry, only .txt extensions are allowed.\n";
        $uploadOk = 0;
    }
    
    if (!(preg_match('/^[a-f0-9]{32}$/', $session_id))) {
    	echo "Sorry, that is not a valid session ID.\n";
        $uploadOk = 0;
    }

    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
        echo "Sorry, your file was not uploaded.\n";
    } else {
        // If everything is ok, try to upload the file
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file_path)) {
            echo "The file " . htmlspecialchars(basename($_FILES["fileToUpload"]["name"])) . " has been uploaded.";
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }

    $old_path = getcwd();
    chdir($target_dir);
    // make unreadable - the proper way
    shell_exec('chmod -- 000 *');
    chdir($old_path);
}
?>

