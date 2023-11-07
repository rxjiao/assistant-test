from openai import OpenAI
import time
client = OpenAI()

# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("assets/test.docx", "rb"),
  purpose='assistants'
)

# Add the file to the assistant
assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=[file.id]
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "what is sepcial about AABBCC city.",
      "file_ids": [file.id]
    }
  ]
)

# Run the assistant on the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

# Retrieve the run status
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

# Keep retrieving the run until its status is 'completed'
while run.status != 'completed':
  time.sleep(1)  # Wait for a short period of time to avoid excessive requests
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.data[0].content[0].text.value)

# Delete the assistant
client.beta.assistants.delete(assistant.id)