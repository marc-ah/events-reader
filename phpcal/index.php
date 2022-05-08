<?php

$host        = "host = localhost";
$port        = "port = 5432";
$dbname      = "dbname = cdn_events";
$credentials = "user = cdn_events password=***********";

$db = pg_connect( "$host $port $dbname $credentials"  );

if(!$db) {
	echo "Error : Unable to open database\n";
}

$today = date("Y-m-d");

echo "<h1>Veranstaltungskalender</h1>";

$query = "SELECT * FROM events WHERE event_date >='" . $today . "' ORDER BY event_date ASC";
$result = pg_query($db,$query);

while($row=pg_fetch_assoc($result)) {
	echo "<br><b>" . $row["event_date"] . "</b>";
	echo "<br><h3>" . $row["title"] . "</h3>";
	echo "<br>" . $row["description"];
	echo "<br><img src='" . $row["img_url"] . "' width='200px'>"; 
	echo "<hr>";

}

pg_close($db);

?>
