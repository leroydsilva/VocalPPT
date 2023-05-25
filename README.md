# VocalPPT

Welcome to the VocalPPT! This application is designed to automate the management of PowerPoint presentations using text-to-speech and speech-to-text capabilities. Developed in Python programming language, this virtual assistant provides a convenient solution for regular users, as well as elderly and physically disabled users.

## Tech Stack

**Client:** HTML, CSS, Java Script

**Backend:** Flask, Python

**Database:** PostgreSQL

**API:** Google Image Search API, Speech-to-text Api, Text-to-speech APi


## Features

- Convert text into synthesized speech representation using text-to-speech synthesis.
- Recognize and interpret spoken language using speech recognition system to transcribe speech into text.
- Two-way interaction between the user and the application using speech-to-text and text-to-speech modules.
- Generate PowerPoint presentations using Python's PowerPoint module.
- Recommend templates and layouts based on the content to be presented, such as text, graphs, and images.
- Add desired images by specifying the topic, utilizing the Google Image search API
- Download the completed PowerPoint presentation for further use.

## Getting Started

Clone the project

```bash
  git clone https://github.com/leroydsilva/PhoneMate.git
```

Go to the project directory

```bash
  cd PhoneMate
```

Create a virtual environment for the project:

```bash
  python3 -m venv venv
```
Activate the virtual environment:

On macOS and Linux:
```bash
  source venv/bin/activate 
```
On Windows:
```bash
venv\Scripts\activate
```
Install the project dependencies:
```bash
pip install -r requirements.txt
```
Start the server:
```bash
python app.py
```
