<?php

require dirname(__FILE__) . '/vendor/autoload.php';

define("PROJECT_ID", $_SERVER['PROJECT_ID']);
define("REST_API_TOKEN",  $_SERVER['REST_API_TOKEN']);

use Generator as Coroutine;
use SignalWire\Relay\Consumer;

class CustomConsumer extends Consumer {
  public $project = PROJECT_ID;
  public $token = REST_API_TOKEN;
  public $contexts = ['home', 'office'];

  public function ready(): Coroutine {
    yield;
    // Consumer is successfully connected with Relay.
    // You can make calls or send messages here..
  }

  public function onIncomingCall($call): Coroutine {
    $result = yield $call->answer();
    if ($result->isSuccessful()) {
      yield $call->playTTS(['text' => 'Welcome to SignalWire!']);
    }
  }
}

$consumer = new CustomConsumer();
$consumer->run();
