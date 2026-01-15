#!/usr/bin/env python3
"""
Demo/Test script for ASCII Animals
Includes fallback ASCII art for testing without Ollama
"""

import sys


# Fallback ASCII art (in case Ollama is not installed)
FALLBACK_ANIMALS = {
    "cat": """
  /\\_/\\  
 ( o.o ) 
  > ^ <  
 /|   |\\
(_|   |_)
""",
    "dog": """
  / \\__
 (    @\\___
 /         O
/   (_____/
/_____/   U
""",
    "owl": """
  (o,o)
  {`"'}
  -"-"-
""",
    "penguin": """
  _~_
 (o o)
/  V  \\
/|    |\\
 ^    ^
""",
    "rabbit": """
(\\___/)
(='.'=)
(")_(")
""",
    "dragon": """
    ^___^
   (O   O)
   (  >  )
  __) (__
~(_______)-
""",
}


def demo_fallback():
    """Demo the fallback ASCII art"""
    print("\n" + "=" * 50)
    print("ASCII Animals - Fallback Demo")
    print("(Pre-stored art - works without Ollama)")
    print("=" * 50 + "\n")
    
    for name, art in FALLBACK_ANIMALS.items():
        print(f"🐾 {name.capitalize()}:")
        print(art)
        input("Press Enter for next animal...")


def demo_with_ollama():
    """Demo with actual Ollama if available"""
    try:
        from ascii_animals import (
            check_ollama_installed,
            check_model_available,
            generate_ascii_animal,
            ANIMALS
        )
        
        if not check_ollama_installed():
            print("❌ Ollama not installed. Showing fallback demo instead.\n")
            demo_fallback()
            return
        
        if not check_model_available():
            print("❌ Model not available. Showing fallback demo instead.\n")
            demo_fallback()
            return
        
        print("\n" + "=" * 50)
        print("ASCII Animals - AI-Generated Demo")
        print("(Using Ollama with llama3.2:1b)")
        print("=" * 50 + "\n")
        
        demo_animals = ["cat", "dog", "dragon", "penguin"]
        
        for animal in demo_animals:
            print(f"🎨 Generating {animal}...")
            art = generate_ascii_animal(animal)
            if art:
                print(f"\n{art}\n")
            else:
                print(f"Failed to generate {animal}\n")
            
            cont = input("Continue to next animal? (y/n): ").lower()
            if cont != 'y':
                break
        
        print("\n✨ Demo complete!")
        
    except ImportError:
        print("❌ Could not import ascii_animals.py")
        print("Showing fallback demo instead.\n")
        demo_fallback()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fallback":
        demo_fallback()
    else:
        print("ASCII Animals Demo")
        print("-" * 50)
        print("This demo will test the ASCII animal generator.")
        print()
        print("Options:")
        print("1. Try with Ollama (if installed)")
        print("2. Show fallback pre-stored animals")
        print()
        
        choice = input("Select (1/2): ").strip()
        
        if choice == "2":
            demo_fallback()
        else:
            demo_with_ollama()
