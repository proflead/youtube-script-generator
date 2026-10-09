import os

import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

SEARCHAPI_API_KEY = os.getenv("SEARCHAPI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not SEARCHAPI_API_KEY:
    raise ValueError("SEARCHAPI_API_KEY is missing")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

SEARCHAPI_URL = "https://www.searchapi.io/api/v1/search"
OPENAI_MODEL = "gpt-5.5"

openai_client = OpenAI(api_key=OPENAI_API_KEY)

MAX_TRANSCRIPT_CHARS = 30000


def searchapi_request(params):
    response = requests.get(
        SEARCHAPI_URL,
        params=params,
        headers={
            "Authorization": f"Bearer {SEARCHAPI_API_KEY}"
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])

    return data


def search_youtube(topic):
    data = searchapi_request({
        "engine": "youtube",
        "q": topic,
    })

    return data.get("videos", [])


def pick_top_videos(videos, limit=6):
    candidates = [
        video
        for video in videos[:10]
        if video.get("id") and not video.get("live")
    ]

    candidates.sort(
        key=lambda video: video.get("extracted_views", 0),
        reverse=True,
    )

    return candidates[:limit]


def get_transcript(video_id):
    data = searchapi_request({
        "engine": "youtube_transcripts",
        "video_id": video_id,
        "lang": "en",
        "only_available": "true",
    })

    segments = data.get("transcripts", [])

    if not segments:
        return ""

    lines = []

    for segment in segments:
        start = int(segment.get("start", 0))
        text = segment.get("text", "").strip()

        if text:
            lines.append(f"[{start}s] {text}")

    return "\n".join(lines)


def collect_videos_with_transcripts(candidates, limit=3):
    results = []

    for video in candidates:
        try:
            transcript = get_transcript(video["id"])
        except Exception as error:
            print(f"Skipping {video['title']}: {error}")
            continue

        if not transcript:
            continue

        video["transcript"] = transcript
        results.append(video)

        if len(results) == limit:
            break

    return results


def ask_ai(prompt):
    response = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text


def analyze_videos(topic, videos):
    video_blocks = []

    for index, video in enumerate(videos, start=1):
        transcript = video["transcript"][:MAX_TRANSCRIPT_CHARS]

        video_blocks.append(
            f"""
VIDEO {index}

Title: {video.get("title")}
Views: {video.get("extracted_views", 0)}
Published: {video.get("published_time", "Unknown")}

Transcript:
{transcript}
"""
        )

    research_data = "\n\n".join(video_blocks)

    prompt = f"""
You are helping me research successful YouTube videos
before I write my own video.

My topic:
{topic}

Below are transcripts from relevant, strong-performing
videos about this topic.

{research_data}

Analyze them as a group.

I do NOT want you to rewrite or copy these videos.

Create a concise content research brief with these sections:

1. HOOKS
Explain how the videos get attention in the first
30-60 seconds. Find common patterns.

2. COMMON STRUCTURE
Show the common way these videos organize the topic.

3. KEY TOPICS
List the important ideas that appear across multiple
videos.

4. WHAT WORKS
Identify useful patterns in examples, explanations,
demos, pacing, or presentation.

5. CONTENT GAPS
Find useful questions, problems, or angles that the
videos do not explain well.

6. RECOMMENDED VIDEO
Create a short brief for my new original video:
- recommended hook
- must-cover topics
- differentiating angle
- suggested section order

Keep the analysis practical and specific.
Do not copy sentences from the transcripts.
"""

    return ask_ai(prompt)


def generate_script(topic, research):
    prompt = f"""
Write an original YouTube script for me about:

{topic}

Use this competitor research as planning input:

{research}

Requirements:

- Write an original script. Do not copy wording from competitors.
- Start with a strong, short hook.
- Get to the useful content quickly.
- Use simple, natural language.
- Cover the important topics found in the research.
- Use relevant content gaps to make the video more useful.
- Keep the structure easy to follow.
- Avoid generic filler and unnecessary hype.
- Target roughly 1,200 to 1,500 words.
- Finish with a short natural conclusion and CTA.

Return only the finished script.
"""

    return ask_ai(prompt)


def main():
    topic = input(
        "What YouTube video do you want to create? "
    ).strip()

    if not topic:
        print("Please enter a topic.")
        return

    print("\nSearching YouTube...")

    search_results = search_youtube(topic)

    if not search_results:
        print("No YouTube videos found.")
        return

    candidates = pick_top_videos(search_results)

    print("\nGetting transcripts...")

    videos = collect_videos_with_transcripts(
        candidates,
        limit=3,
    )

    if not videos:
        print("Could not find usable transcripts.")
        return

    print("\nVideos selected for research:")

    for video in videos:
        print(
            f"- {video['title']} "
            f"({video.get('extracted_views', 0):,} views)"
        )

    print("\nAnalyzing videos...")

    research = analyze_videos(topic, videos)

    with open(
        "research.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(research)

    print("\nGenerating script...")

    script = generate_script(topic, research)

    with open(
        "script.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(script)

    print("\nDone.")
    print("Research saved to research.md")
    print("Script saved to script.md")


if __name__ == "__main__":
    main()