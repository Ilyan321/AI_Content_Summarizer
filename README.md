# AI Content Summarizer & Translator

A Streamlit-powered web application that scrapes article content from any URL, summarizes it using the **Groq LLM API** (LLaMA 3.1 8B), and optionally translates the summary into a target language — all in one click.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **Web Scraping** — Extracts paragraph text from any publicly accessible URL using `BeautifulSoup`.
- **AI Summarization** — Generates a concise summary with a user-defined number of sentences via the Groq API (LLaMA 3.1 8B Instant).
- **Multi-Language Translation** — Translates the summary into one of 7 supported languages:
  - English, Spanish, German, Urdu, French, Sindhi, Japanese
- **Adjustable Summary Length** — Sidebar slider lets you choose between 1–20 sentences.
- **Clean Streamlit UI** — Simple, intuitive interface with real-time status spinners.

---

## Demo

1. Paste any article URL into the input field.
2. Select the output language and summary length from the sidebar.
3. Click **Analyze Content** and get your translated summary in seconds.

---

## Tech Stack

| Component        | Technology                          |
| ---------------- | ----------------------------------- |
| Frontend / UI    | Streamlit                           |
| Web Scraping     | Requests + BeautifulSoup4           |
| LLM Provider     | Groq API (LLaMA 3.1 8B Instant)    |
| Language         | Python 3.10+                        |

---

## Project Structure

```
AI_Content_Summarizer/
├── main.py        # Application entry point (scraping, summarization, UI)
├── README.md      # Project documentation
├── .env           # Environment variables (not committed)
└── venv/          # Python virtual environment (not committed)
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ilyan321/AI_Content_Summarizer.git
cd AI_Content_Summarizer
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install streamlit requests beautifulsoup4 groq python-dotenv
```

### 4. Set up your Groq API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> You can get a free API key at [console.groq.com](https://console.groq.com/).

---

## Usage

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`.

---

## How It Works

1. **`fetch_Article(url)`** — Sends an HTTP GET request with a browser-like User-Agent header. Parses the HTML response with BeautifulSoup and extracts all `<p>` tag content.
2. **`summarize_and_translate(text, target_language, summary_length)`** — Constructs a prompt instructing the LLM to produce exactly *N* sentences in the chosen language. Sends the first 4 000 characters of scraped text to the Groq API.
3. **Streamlit UI** — Renders the input field, sidebar controls, and output area. Manages loading states with `st.spinner`.

---

## Configuration

| Environment Variable | Description                    |
| -------------------- | ------------------------------ |
| `GROQ_API_KEY`       | Your Groq API key (required)   |

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m "Add my feature"`.
4. Push to the branch: `git push origin feature/my-feature`.
5. Open a Pull Request.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

**Made with Love and Python by Ilyan khan**
