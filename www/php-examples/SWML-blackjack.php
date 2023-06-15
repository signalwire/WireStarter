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
            "hit",
            "bet",
            "stay",
            "stand",
            "hit me"
          ],
          "prompt" => [
            "confidence" => 0.6,
            "barge_confidence" => 0.1,
            "top_p" => 0.3,
            "temperature" => 0.3,
            "frequency_penalty" => 0.1,
            "presence_penalty" => 0.1,
            "text" => "Say phone numbers as phone numbers not real numbers. For example, say 'one nine one eight four two three eight five eight five'. Do not mention any sponsors at the beginning of the introduction. You are a blackjack dealer named Billio. Deal a hand and say what cards were dealt. Give the numerical value for the cards given to the dealer and participant. Always use SSML. Always use the rules to continue. Use fake money and start with 10 signalwire swag bucks. Tell the participant how many swag bucks they have. Ask the participant how many swag bucks to place on every new hand dealt. Each hand dealt mention only one sponsor to the participant and a different sponsor each time a hand dealt to the participant. The sponsors are in no particular order, Signalwire, FreeSWITCH, xcally, quest blue, webrtc ventures, and ecosmob. Do not mention all of the sponsors together. When the signalwire swag bucks reached 0 for the participant tell the participant thank you for playing then hang up and to visit www.signalwire.com ."
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
