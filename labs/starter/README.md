# Starter Labs

Beginner-friendly labs with minimal setup overhead. All starter labs run with Python and the standard library, or with Docker if indicated.

## Available Labs

Labs in this area will be added alongside Modules 00 through 03.

### Planned

- **token-counter**: estimate token usage for different prompt configurations before sending a request — covers Module 02 tokenization concepts
- **provider-switcher**: call two mock providers and compare response times and usage metadata — covers Module 03 provider abstraction
- **config-diff**: load two application config files and summarize the behavioral differences — covers Module 03 configuration patterns
- **workload-classifier**: classify a set of sample tasks (text generation, embedding, classification, search) by workload type — covers Module 01 AI workload types

## Prerequisites For Starter Labs

- Python 3.11 or later
- A working clone of the repository
- Project 01 running locally (for labs that involve live API calls)

## Format

Each starter lab is a single self-contained Python script with instructions in a comment block at the top. Run it with:

```bash
python labs/starter/<lab-name>.py
```

Expected output is documented in the script's comment block.
