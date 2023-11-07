from openai import OpenAI
import time
import subprocess

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

# Retrieve the assistant ID
print("\nThe assistant ID is:\n", assistant.id, "\n")

# Initialize a thread
thread = client.beta.threads.create(
    messages=[]
)

while True:
    # Get user input
    user_input = input("\nUser: ")
    if user_input.lower() == 'exit':
        break

    # Add user message to the thread
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=user_input
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

    # Get the latest messages from the thread
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Print the latest assistant message
    print("Assistant:", messages.data[0].content[0].text.value, "\n")


# Delete the assistant
del_status = client.beta.assistants.delete(assistant.id)

if del_status.deleted:
    print("\nThe assistant was successfully deleted.\n")
else:
    print("\nThe assistant was not deleted. ID:", assistant.id, "\n")

    # Call the shell script
    subprocess.call(['bash', 'clear_assistant.sh', assistant.id])
