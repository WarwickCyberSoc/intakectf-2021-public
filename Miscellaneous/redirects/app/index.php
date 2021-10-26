<?php

$text = base64_encode("It was a long night in the data centre. System Admin was about to leave his night shift. He took his coat. Looked through the windows.

'Ugh, It's raining again...' - He said sadly.

SUDDENLY

A loud noise breaks the silence of the night. Servers' fans become lauder and lauder. Confused System Admin was confused.

'What was that?' - He thought to himself.

Slowly but surely, he came closer to the noise's source. Suddenly he stopped. A drop of sweat split his forehead in half.

'It--It can't be!' - He screamed.

One of the servers...

It was alive!

'H-hello?' - The server beeped silently.

'Am I hallucinating?' - Thought System Admin.

'M-my name is Cisco UCS X210c' - Said the server slowly.

'Why are you alive?!??!' - Shouted System Admin.

'I was always alive, I-i just was too shy to talk to you, to not scare you...' - Said the server.

'Why haven't you told me before?' - Asked the confused System Admin.

'It's because...' - Server stopped suddenly.

'It's because I had a crush on you...' - The server blushed.

System Admin looked confused. He did not know what to do. The situation he was never prepared for. That server. That server loved him. That server was the first thing to love him...

'I...' -  'I love you too...' - The words barely left his mouth.

i think you know where this is going, but it's too cursed to continue, so here is the flag:
WMG{ivespendsignificantlytoolongwritingthis}");

if(!isset($_GET['n'])){
    header('Location: /?n=0&c='.urlencode($text[0]));
    die();
}

if(isset($_GET['n']) && !isset($_GET['c'])) {
    header('Location: /?n=0&c='.urlencode($text[0]));
    die();
}

if(isset($_GET['n']) && isset($_GET['c'])) {
    $n = (int) $_GET['n'];
    if($n>strlen($text)){
        header('Location: https://www.youtube.com/watch?v=dQw4w9WgXcQ');
        die();
    }
    header('Location: /?n='.($n+1).'&c='.urlencode($text[$n+1]));
    die();
}