#!/usr/bin/env python3
"""
ASCII Animal Generator using Ollama
Generates ASCII art of animals on-demand using a lightweight LLM
"""

import subprocess
import json
import sys


ANIMALS = [
    "cat", "dog", "owl", "penguin", "rabbit", "turtle", 
    "elephant", "fox", "bear", "panda", "koala", "duck",
    "butterfly", "fish", "whale", "octopus", "dragon", "unicorn"
]


def check_ollama_installed():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_model_available(model_name="llama3.2:1b"):
    """Check if the specified model is available"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5
        )
        return model_name in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def pull_model(model_name="llama3.2:1b"):
    """Pull the Ollama model if not already available"""
    print(f"Downloading {model_name} model... (This is a one-time setup, ~1GB)")
    print("This may take a few minutes...\n")
    try:
        subprocess.run(
            ["ollama", "pull", model_name],
            encoding='utf-8',
            errors='replace',
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def generate_ascii_animal(animal_name, model_name="llama3.2:1b"):
    """
    Generate ASCII art of an animal using Ollama
    
    Args:
        animal_name: Name of the animal to generate
        model_name: Ollama model to use (default: llama3.2:1b for speed)
    
    Returns:
        str: ASCII art of the animal
    """
    prompt = f"""Create a simple ASCII art of a {animal_name}. 
Keep it small (max 15 lines), cute, and suitable for a thermal printer (max 48 characters wide).
Only output the ASCII art, nothing else. No explanations, no markdown code blocks, just the art itself."""

    try:
        # Use Ollama API via command line
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',  # Fix Windows encoding issues
            errors='replace',  # Replace undecodable chars instead of crashing
            timeout=30
        )
        
        if result.returncode == 0:
            # Clean up the output
            ascii_art = result.stdout.strip()
            # Remove any markdown code blocks if present
            ascii_art = ascii_art.replace("```", "")
            # Limit to reasonable size
            lines = ascii_art.split('\n')
            if len(lines) > 20:
                lines = lines[:20]
            return '\n'.join(lines)
        else:
            # Print error for debugging
            if result.stderr:
                print(f"Ollama error: {result.stderr.strip()}")
            return None
            
    except subprocess.TimeoutExpired:
        print("⏱️  Generation timed out. The model might be too slow.")
        return None
    except FileNotFoundError:
        print("❌ Ollama command not found. Is Ollama installed and in PATH?")
        return None
    except Exception as e:
        print(f"❌ Error generating ASCII art: {e}")
        return None


def list_animals():
    """Display available animals"""
    print("\n🐾 Available Animals:")
    print("=" * 50)
    for i, animal in enumerate(ANIMALS, 1):
        print(f"{i:2d}. {animal.capitalize()}")
    print("=" * 50)
    print()


def interactive_mode():
    """Interactive mode for choosing and generating animals"""
    if not check_ollama_installed():
        print("❌ Ollama is not installed!")
        print("\nTo use AI-generated ASCII art, install Ollama:")
        print("  Windows: Download from https://ollama.ai")
        print("  Linux/Mac: curl -fsSL https://ollama.ai/install.sh | sh")
        print("\nOr use --fallback mode for pre-stored ASCII art.")
        return 1
    
    # Check if model is available, pull if not
    if not check_model_available():
        print(f"Model 'llama3.2:1b' not found.")
        response = input("Download it now? (y/n): ").lower()
        if response == 'y':
            if not pull_model():
                print("Failed to download model.")
                return 1
        else:
            print("Cannot proceed without the model.")
            return 1
    
    while True:
        list_animals()
        print("Type an animal name/number, 'random', or 'quit':")
        choice = input("> ").strip().lower()
        
        if choice in ['quit', 'q', 'exit']:
            print("Goodbye! 🐾")
            break
        
        # Handle numeric input
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ANIMALS):
                animal = ANIMALS[idx]
            else:
                print("Invalid number!")
                continue
        elif choice == 'random':
            import random
            animal = random.choice(ANIMALS)
            print(f"🎲 Random choice: {animal.capitalize()}")
        elif choice in ANIMALS:
            animal = choice
        else:
            # Allow custom animals
            animal = choice
        
        print(f"\n🎨 Generating {animal}...\n")
        ascii_art = generate_ascii_animal(animal)
        
        if ascii_art:
            print(ascii_art)
            print()
        else:
            print("Failed to generate ASCII art. Try another animal!")
        
        print()


def generate_and_print(animal_name):
    """Generate and print a single animal"""
    if not check_ollama_installed():
        print("❌ Ollama is not installed!")
        return 1
    
    if not check_model_available():
        print("Model not available. Run in interactive mode first to download.")
        return 1
    
    print(f"🎨 Generating {animal_name}...\n")
    ascii_art = generate_ascii_animal(animal_name)
    
    if ascii_art:
        print(ascii_art)
        return 0
    else:
        print("Failed to generate ASCII art.")
        return 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate ASCII art of animals using AI"
    )
    parser.add_argument(
        "animal",
        nargs="?",
        help="Animal to generate (or leave empty for interactive mode)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available animals"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_animals()
        sys.exit(0)
    
    if args.animal:
        sys.exit(generate_and_print(args.animal))
    else:
        sys.exit(interactive_mode())
