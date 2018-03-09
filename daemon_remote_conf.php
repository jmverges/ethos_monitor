<?php

//YOUR REMOTE CONF URL - Use http not https
$your_config_url = file_get_contents('/home/ethos/remote.url');

//TIME TO CHECK - IN SECONDS
$time_check = 180;

//ROUTE TO SAVE LENGTH
$LOCAL_CONF = '/home/ethos/length.txt';


while (true) {
    if (empty($your_config_url) == false) {
        check_file($LOCAL_CONF, retrieve_server_config($your_config_url));
    }else{
        $your_config_url = file_get_contents('/home/ethos/remote.url');
    }
    sleep($time_check);
}


function retrieve_server_config($url)
{
    $text = file_get_contents($url);
    $size = strlen($text);
    return $size;
}


function check_file($file, $size)
{
    //Use the function is_file to check if the file already exists or not.
    if (!is_file($file)) {
        file_put_contents($file, $size);
    } else {
        if (read_file($file) != $size) {
            file_put_contents($file, $size);
            echo "Remote Conf Change\n";
            echo "Clearing thermals\n";
            $last_gpu = file_get_contents("/var/run/ethos/gpucount.file") - 1;
            for ($i = 0; $i <= $last_gpu; $i++) {
                file_put_contents("/var/run/ethos/throttled.gpu" . $i, "");
            }
            file_put_contents("/var/run/ethos/overheat.file", "");
            file_put_contents("/var/run/ethos/throttled.file", "");
            file_put_contents("/opt/ethos/etc/autorebooted.file", "0");
            shell_exec('sudo /opt/ethos/sbin/ethos-overclock');
            echo "Cleared all overheats and throttles and re-applied overclocks, set autoreboot counter back to 0.\n";
            echo "Execute command putconf && minestop\n";
            shell_exec('putconf && minestop');
            echo "Execute command r\n";
            shell_exec('r');
        }
    }
}


function read_file($file)
{
    $myfile = fopen($file, "r") or die("Unable to open file!");
    return fread($myfile, filesize($file));
    fclose($myfile);
}


?>
