<?php

require_once __DIR__ . '/vendor/autoload.php';

$uri = 'mongodb+srv://localuser_01:OyKbJFFSeGsQpHbI@demo-localdev.l5vs7jo.mongodb.net/?retryWrites=true&w=majority&appName=demo-localdev';

$client = new MongoDB\Client($uri);