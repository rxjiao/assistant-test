from openai import OpenAI
import time
import subprocess
import os

client = OpenAI()

# List of supported file formats
supported_formats = ['c', 'cpp', 'csv', 'docx', 'html', 'java', 'json', 'md', 'pdf', 'php', 'pptx', 'py', 'rb', 'tex', 'txt', 'css', 'jpeg', 'jpg', 'js', 'gif', 'png', 'tar', 'ts', 'xlsx', 'xml', 'zip']

# Get a list of all files in the 'assets' directory
file_list = os.listdir('assets')

# Filter the list to include only supported file formats
file_list = [f for f in file_list if f.split('.')[-1] in supported_formats]

# Create a list to store the file objects
files = []

# Upload each file in the list
for filename in file_list:
    with open(f'assets/{filename}', 'rb') as f:
        file = client.files.create(
            file=f,
            purpose='assistants'
        )
        # Add the file object to the list
        files.append(file)

# Add the file to the assistant
assistant = client.beta.assistants.create(
  instructions="You are an AI assistant. Read the provided files and use the information to answer questions about the files.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=[f.id for f in files]
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
