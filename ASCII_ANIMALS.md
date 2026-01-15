# ASCII Animals Feature 🐾

A fun CLI feature that generates ASCII art of animals using AI! Instead of storing pre-made ASCII art, this feature uses **Ollama** with a lightweight 1B parameter model to generate unique ASCII art on-demand.

## Why Use an LLM?

✅ **No storage needed** - No large files of pre-made ASCII art  
✅ **Infinite variety** - Different art each time you run it  
✅ **Lightweight** - Uses llama3.2:1b (only 1GB, runs on CPU)  
✅ **Offline** - Works without internet after initial setup  
✅ **Fun** - AI-generated means every render is unique!  

## Installation

### 1. Install Ollama

**Windows:**
```powershell
# Download and install from: https://ollama.ai
```

**Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull the Model (One-time setup)

```bash
ollama pull llama3.2:1b
```

This downloads ~1GB - it's a one-time operation.

## Usage

### Interactive Mode (Recommended)

From the main menu:
```bash
python main.py
# Select option 7: ASCII Animals 🐾
```

Or directly:
```bash
python main.py animals
```

This gives you an interactive selection menu where you can choose animals by number or name!

### Command Line

Generate a specific animal:
```bash
python main.py animals cat
python main.py animals dragon
python main.py animals penguin
```

List available animals:
```bash
python main.py animals --list
```

Generate a random animal:
```bash
python ascii_animals.py
# Then type: random
```

### Direct Script Usage

```bash
# Interactive mode
python ascii_animals.py

# Specific animal
python ascii_animals.py dog

# List animals
python ascii_animals.py --list
```

## Available Animals

🐱 cat | 🐶 dog | 🦉 owl | 🐧 penguin | 🐰 rabbit | 🐢 turtle  
🐘 elephant | 🦊 fox | 🐻 bear | 🐼 panda | 🐨 koala | 🦆 duck  
🦋 butterfly | 🐟 fish | 🐋 whale | 🐙 octopus | 🐉 dragon | 🦄 unicorn

You can also request custom animals - just type any animal name!

## Example Output

```
🎨 Generating cat...

  /\_/\  
 ( o.o ) 
  > ^ <  
 /|   |\
(_|   |_)
```

Each generation is unique because it's AI-created!

## Technical Details

- **Model**: llama3.2:1b (1 billion parameters)
- **Prompt**: Optimized for small, cute ASCII art (max 15 lines, 48 chars wide)
- **Generation time**: ~2-5 seconds on modern CPUs
- **Size**: Model is ~1GB on disk
- **Requirements**: Ollama installed and running

## Troubleshooting

**"Ollama is not installed"**
- Install Ollama from https://ollama.ai

**"Model not found"**
- Run: `ollama pull llama3.2:1b`
- Or let the interactive mode download it for you

**Generation is slow**
- The 1B model should be fast. If slow, check:
  - CPU usage (should use ~100% of 1 core)
  - Try a newer version of Ollama
  - Check if other processes are using resources

**Output has markdown code blocks**
- The tool automatically strips these, but if you see them, it's a parsing issue
- Try regenerating the animal

## Why Not Just Use a Library?

Traditional ASCII art libraries like `art` or `pyfiglet`:
- Only do text banners (not animal drawings)
- Have limited pre-made art
- Require storage of art files

Using an LLM:
- Generates any animal you can imagine
- Creates unique variations each time
- More fun and surprising!
- Demonstrates practical AI usage in CLI tools

## Future Enhancements

Potential ideas:
- Add `--print` flag to send output directly to thermal printer
- Save favorite generations
- Add more art styles (pixel art, detailed, minimal, etc.)
- Support custom prompts for specific styles

Enjoy your AI-powered ASCII animals! 🎨🐾
