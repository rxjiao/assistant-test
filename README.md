# assistant-test

This repository contains a Python script for testing OpenAI assistant that can retrieve information from given files.

## Installation

Before running the script, you should set up a virtual environment to isolate the packages required for this project. Here's how you can do it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Next, install the required packages by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

This command will install all the packages listed in the requirements.txt file.

## Configuration

The script requires an API key, which should be stored in an environment variable. You can set this up like this:

```bash
export OPENAI_API_KEY=your_api_key
```

Replace `your_api_key` with your actual API key. Please see the [OpenAI API documentation](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key?context=python) for more information.

## Usage

To run the script, use the following command:

```python
python openai-test.py
```
