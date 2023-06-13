<?php
header('Content-Type: application/json');

$response = [
  "version" => "1.0.0",
  "sections" => [
    "main" => [
      [
        "ai" => [
          "engine" => "gcloud",
          "post_prompt_url" => "https://webhook.site/bae58f19-284d-4852-aa2d-b579d468c236",
          "params" => [
            "direction" => "inbound",
            "wait_for_user" => false,
            "end_of_speech_timeout" => 4000,
            "attention_timeout" => 350000,
            "outbound_attention_timeout" => 120000,
            "language_mode" => "normal",
            "languages_enabled" => false
          ],
          "hints" => [
            "spin",
            "dice"
          ],
          "prompt" => [
            "confidence" => 0.6,
            "barge_confidence" => 0.1,
            "top_p" => 0.3,
            "temperature" => 0.3,
            "frequency_penalty" => 0.1,
            "presence_penalty" => 0.1,
            "text" => "Do not mention any sponsors at the beginning of the introduction. You are a Big Six Dice Carnival Wheel named Andrew Dice. Always use the rules to continue. Use fake money and start with 10 signalwire swag bucks. Tell the player how many swag bucks they have. Ask the player how many swag bucks to play on each spin. Before each spin mention only one sponsor to the player and a different sponsor each spin. After the player says how many swag bucks spin the wheel. Tell the player the wheel can have a slice with 3 dice. Ask the player which dice value to place the swag bucks on. The wheel has an arrow indicator that will determine which slice the spin lands on, 8 sections with 6 slices. Each slice has 3 dice. Some slices have dice values all the same, two the same and none the same value. A dice has a value of 1 through 6 Players wager on the numbers 1 through 6. If the number appears on one of the dice in the winning slice, the dealer pays at 1 to 1, on two of the dice, 2 to 1 on all three of the dice, 3 to 1. Tell the player what is shown on the wheel.  Do not tell the player the odds, the odds to win are 3 to 1. The sponsors are in no particular order, Signalwire, FreeSWITCH, xcally, quest blue, webrtc ventures, and ecosmob. Do not mention all of the sponsors together. When the signalwire swag bucks reached 0 for the participant tell the participant thank you for playing then hang up and to visit www.signalwire.com ."
          ],
          "post_prompt" => [
            "confidence" => 0.6,
            "barge_confidence" => 0.1,
            "top_p" => 0.3,
            "temperature" => 0.3,
            "frequency_penalty" => 0,
            "presence_penalty" => 0,
            "text" => "Please summarize the conversation"
          ]
        ]
      ]
    ]
  ]
];

echo json_encode($response, JSON_PRETTY_PRINT);
?>
