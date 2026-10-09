# YouTube Script Generator

A Python tool that helps you write a YouTube video script. Enter a topic, and it searches YouTube, reads available English transcripts from up to three videos, and uses OpenAI to create a research summary and an original script.

## Setup

You need Python 3, a SearchAPI API key, and an OpenAI API key.

1. Open a terminal in the project folder and install the required packages:

   ```bash
   python3 -m pip install requests python-dotenv openai
   ```

2. Create a file named `.env` in the project folder and add your keys:

   ```dotenv
   SEARCHAPI_API_KEY=your_searchapi_key
   OPENAI_API_KEY=your_openai_key
   ```

   Keep your API keys private. Do not commit the `.env` file to Git.

## Use

Run the tool:

```bash
python3 youtube_script_generator.py
```

Enter your video topic when asked. For example: `How to start a vegetable garden`.

The tool saves two files in the folder where you run it:

- `research.md`: A summary of hooks, common topics, and content gaps.
- `script.md`: Your generated video script.

Each run replaces these files, so save a copy if you want to keep earlier results.
