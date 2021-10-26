<?php
require_once "secret.php";

function loadNotesFromCookie() {
    if(!isset($_COOKIE["auth"]))
    {
        return array();
    }

    $cookie = explode(":", $_COOKIE["auth"]);

    if(count($cookie) != 2)
    {
        return array();
    }

    $json = base64_decode($cookie[0], true);
    $hmac = $cookie[1];

    if($json === false)
    {
        return array();
    }

    if(!password_verify($SECRET_KEY . $json, $hmac))
    {
        return array();
    }

    $decoded = json_decode($json, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        return array();
    }

    if(!is_array($decoded) || !isset($decoded["notes"]) || !isset($decoded["notes"]))
    {
        return array();
    }

    return $decoded["notes"];
}

function saveNotesToCookie($notes) {
    $encoded = json_encode(array("notes" => $notes));

    $hmac = password_hash($SECRET_KEY . $encoded, PASSWORD_BCRYPT);

    $encoded = base64_encode($encoded);

    setcookie("auth", $encoded . ":" . $hmac);
}
?>