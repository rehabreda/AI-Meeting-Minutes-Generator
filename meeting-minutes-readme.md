# AI Meeting Minutes Generator

An automated meeting minutes generation system that combines OpenAI's Whisper for speech-to-text transcription and Deepseek LLM for summarization. This tool records meetings and generates structured meeting minutes with key points, takeaways, and action items.

## Features

- Real-time audio recording through a user-friendly Gradio interface
- Speech-to-text transcription using Whisper Medium model
- Automated meeting minutes generation using Deepseek LLM
- Structured output with key discussion points, takeaways, and action items
- Easy-to-use web interface
- Local processing capabilities

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (for Whisper transcription)
- Ollama installed locally (for Deepseek LLM)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rehabreda/ai-meeting-minutes-generator.git
cd ai-meeting-minutes-generator
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is installed and the Deepseek model is downloaded:
```bash
ollama pull deepseek-r1
```

## Project Structure

- `main_huggingface.py`: Main application with Gradio interface
- `audio_module.py`: Handles speech-to-text conversion using Whisper
- `llm_module.py`: Manages meeting minutes generation using Deepseek LLM
- `requirements.txt`: List of Python dependencies

## Usage

1. Start the application:
```bash
python main_huggingface.py
```

2. Access the web interface through your browser (default: http://localhost:7860)

3. Use the interface to:
   - Start/stop recording your meeting
   - Generate meeting minutes from the recorded audio
   - View the generated minutes

## Output Format

The generated meeting minutes include:

1. Key Discussion Points
   - Main topics discussed
   - Important insights
   - Significant conversations

2. Takeaways
   - Core learnings
   - Critical insights
   - Strategic implications

3. Action Items
   - Specific tasks or next steps
   - Prioritized actionable items
   - Assigned responsibilities (if mentioned)

## Technical Details

- Audio Recording: Uses PyAudio for real-time audio capture
- Speech-to-Text: Implements Whisper Medium model with CUDA acceleration
- Text Processing: Utilizes Deepseek LLM through Ollama for generating structured minutes
- Interface: Built with Gradio for easy interaction

## Limitations

- Requires CUDA-compatible GPU for optimal performance
- Audio quality affects transcription accuracy
- Meeting minutes quality depends on transcription clarity
- Local processing required for both transcription and summarization

