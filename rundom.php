<?php

$host = 'localhost';
$database = 'rundom'; 
$user = ''; 
$password = ''; 
$link = mysqli_connect($host, $user, $password, $database);


$data = $_POST['data'];
$chatid = $_POST['chatid'];
$name = $_POST['name'];
$username = $_POST['username'];
$start = $_POST['start'];
$end = $_POST['end'];
$count = $_POST['count'];
$note = $_POST['note'];
$game = $_POST['game'];
$winners = $_POST['winners'];
$users = $_POST['users'];
$luckers = $_POST['luckers'];
$date_luck = $_POST['date_luck'];

mysqli_set_charset($link, "utf8mb4");

if ( $data == "getuser" )
{
	$result = mysqli_query($link, " SELECT * FROM `users` WHERE `chatid`='{$chatid}' " );
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ( $data == "adduser" )
{
	$result = mysqli_query($link, "INSERT INTO `users` (`chatid`, `name`, `username`, `ban`, `luck`, `date_luck`) VALUES ('{$chatid}', '{$name}', '{$username}', '1', '0', '') " );
}
elseif ( $data == "updateuser" )
{
	$result = mysqli_query($link, " UPDATE `users` SET `name`='{$name}',`username`='{$username}' WHERE `chatid`='{$chatid}' " );
}
elseif ( $data == "allusers" )
{
	$result = mysqli_query($link, " SELECT * FROM `users` " );
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ( $data == "addluck" )
{
	$result = mysqli_query($link, " UPDATE `users` SET `luck`='1',`date_luck`='{$date_luck}' WHERE `chatid`='{$chatid}' " );
}
elseif ( $data == "deluser" )
{
	$result = mysqli_query($link, " DELETE FROM `users` WHERE `chatid`='{$chatid}' " );
}
elseif ( $data == "allowuser" )
{
	$result = mysqli_query($link, " UPDATE `users` SET `ban`='0' WHERE `chatid`='{$chatid}' " );
}
elseif ( $data == "delluck" )
{
	$result = mysqli_query($link, " UPDATE `users` SET `luck`='0', `date_luck`='' WHERE `chatid`='{$chatid}' " );
}



elseif ( $data == "addgame" )
{
	$result = mysqli_query($link, " INSERT INTO `games`(`start`, `end`, `count`, `status`, `users`, `luckers`, `winners`, `note`) VALUES ('{$start}','{$end}','{$count}','stop','','','','{$note}') " );
	echo mysqli_insert_id($link);

}
elseif ( $data == "getgame" )
{
	$result = mysqli_query($link, " SELECT * FROM `games` WHERE `id`='{$game}' " );
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ( $data == "stopgame" )
{
	$result = mysqli_query($link, " UPDATE `games` SET `status`='stop' WHERE `id`='{$game}' " );
}
elseif ( $data == "rungame" )
{
	$result = mysqli_query($link, " UPDATE `games` SET `status`='run' WHERE `id`='{$game}' " );
}
elseif ( $data == "winners" )
{
	$result = mysqli_query($link, " UPDATE `games` SET `winners`='{$winners}' WHERE `id`='{$game}' " );
}
elseif ( $data == "delgame" )
{
	$result = mysqli_query($link, " DELETE FROM `games` WHERE `id`='{$game}' " );
}
elseif ( $data == "newusers" )
{
	$result = mysqli_query($link, " UPDATE `games` SET `users`='{$users}' WHERE `id`='{$game}' " );
}
elseif ( $data == "newluckers" )
{
	$result = mysqli_query($link, " UPDATE `games` SET `luckers`='{$luckers}' WHERE `id`='{$game}' " );
}
elseif ( $data == "activegame" )
{
	$result = mysqli_query($link, " SELECT * FROM `games` WHERE `status`='run' " );
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}

