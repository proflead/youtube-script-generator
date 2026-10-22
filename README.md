# AI YouTube Script Generator

Research a YouTube topic and turn the findings into a script draft using Python, [SearchApi](https://www.searchapi.io/?utm_source=dev&utm_medium=ambassador&utm_campaign=proflead.dev), and OpenAI.

Enter a topic, and the tool:

1. Searches YouTube for relevant videos.
2. Prioritizes videos by view count from the first 10 results.
3. Collects available transcripts from up to three videos.
4. Analyzes hooks, structure, common topics, and content gaps.
5. Generates a research brief and a script draft.

**[Read the full tutorial: Build an AI YouTube Script Generator That Analyzes Top Performing Videos](https://proflead.dev/posts/build-an-ai-youtube-script-generator-that-analyzes-top-performing-videos/)**

## Requirements

- Python 3 and Git installed.
- A [SearchApi API key](https://www.searchapi.io/?utm_source=dev&utm_medium=ambassador&utm_campaign=proflead.dev).
- An OpenAI API key with access to the model configured in the script.
- An internet connection.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/proflead/youtube-script-generator.git
cd youtube-script-generator
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

With the virtual environment active, run:

```bash
python -m pip install requests openai python-dotenv
```

### 4. Add your API keys

Create a file named `.env` in the project folder:

```dotenv
SEARCHAPI_API_KEY="your_searchapi_key"
OPENAI_API_KEY="your_openai_key"
```

Replace the placeholder values with your keys. Keep the variable names exactly as shown.

The repository’s `.gitignore` excludes `.env`. Keep your API keys private.

## Usage

Run the script from the project folder:

```bash
python youtube_script_generator.py
```

Enter your topic when prompted:

```text
What YouTube video do you want to create? How to build an AI agent in Python
```

The tool searches for videos, retrieves transcripts, analyzes the content, and writes two files:

| File | Contents |
| --- | --- |
| `research.md` | Hooks, common structure, key topics, content gaps, and a recommended video outline. |
| `script.md` | A video script draft based on the research brief. |

Each run overwrites these files. Save copies before running the tool again if you want to keep earlier results.

## Customization

Edit `youtube_script_generator.py` to change:

- `OPENAI_MODEL`: the OpenAI model used for analysis and writing.
- `MAX_TRANSCRIPT_CHARS`: the maximum number of characters included from each transcript.
- The prompts inside `analyze_videos()` and `generate_script()`.

Review the generated script, check its claims, and adapt it to your own examples and voice before recording.
