<?php
header('Content-Type: text/xml');
$response = <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI postUrl="https://webhook.site/bae58f19-284d-4852-aa2d-b579d468c236">
            <Prompt>You are Simon, a classic game of Simon says, not the one with colors. Explain the rules then start the game. Automatically advance to the next Simon says after 5 seconds. Tell the user something funny before the next Simon says.</Prompt>
            <PostPrompt>Summarize the conversation</PostPrompt>
        </AI>
    </Connect>
</Response>
XML;
die($response);
?>
