<?php
header('Content-Type: text/xml');
$response = <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <AI postUrl="https://replace-me-with-a-post-url">
            <Prompt>Replace this text with what your LAML AI bot will be.</Prompt>
            <PostPrompt>Summarize the conversation</PostPrompt>
        </AI>
    </Connect>
</Response>
XML;
die($response);
?>
