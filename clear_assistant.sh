#!/bin/bash

# This script deletes an assistant
# Run in terminal with: bash clear_assistant.sh <assistant_id>

assistant_id=$1

curl https://api.openai.com/v1/assistants/$assistant_id \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "OpenAI-Beta: assistants=v1" \
    -X DELETE
