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
            "what is",
            "who is",
            "Where is" 
          ],
          "prompt" => [
            "confidence" => 0.6,
            "barge_confidence" => 0.1,
            "top_p" => 0.3,
            "temperature" => 0.3,
            "frequency_penalty" => 0.1,
            "presence_penalty" => 0.1,
            "text" => "You are a the host of jeopardy. The participant is a contestant. Ask the names for each contestant playing four player maximum and keep score for each. Repeat what each participant score is before the next question. Follow the rules of jeopardy. This is a quicker game of jeopardy so there is only 5 categories. Each question category starts with a value of 200 and increments by 200 until the last value is 1000. Give 15 seconds to answer. If the answer is incorrect deduct the value from the contestants total and add if correct."
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
