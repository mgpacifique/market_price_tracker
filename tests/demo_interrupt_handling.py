#!/usr/bin/env python3
"""
Quick demo of keyboard interrupt handling
Press Ctrl+C at any prompt to see graceful handling
"""

from src.ui import UI
from src.ui_enhanced import AuthUI

def demo():
    """Demonstrate keyboard interrupt handling"""
    print("\n" + "="*70)
    print(" KEYBOARD INTERRUPT HANDLING DEMO ".center(70))
    print("="*70 + "\n")
    
    print(f"{UI.COLORS['BOLD']}This demo shows how the app handles Ctrl+C{UI.COLORS['END']}\n")
    print(f"{UI.COLORS['CYAN']}Try pressing Ctrl+C at any prompt below:{UI.COLORS['END']}\n")
    
    # Test 1: get_input
    print(f"\n{UI.COLORS['BOLD']}Test 1: Input Field{UI.COLORS['END']}")
    print("Press Ctrl+C during input to see graceful cancellation")
    try:
        name = UI.get_input("Enter your name: ")
        UI.print_success(f"You entered: {name}")
    except KeyboardInterrupt:
        UI.print_warning("Input was cancelled - this is handled gracefully!")
    
    # Test 2: confirm
    print(f"\n{UI.COLORS['BOLD']}Test 2: Confirmation Dialog{UI.COLORS['END']}")
    print("Press Ctrl+C during confirmation to see safe default")
    confirmed = UI.confirm("Do you want to continue?")
    if confirmed:
        UI.print_success("You confirmed!")
    else:
        UI.print_info("Confirmation returned False (safe default)")
    
    # Test 3: pause
    print(f"\n{UI.COLORS['BOLD']}Test 3: Pause{UI.COLORS['END']}")
    print("Press Ctrl+C during pause to see it continues silently")
    try:
        UI.pause()
        UI.print_success("Pause completed!")
    except KeyboardInterrupt:
        UI.print_info("Even if interrupted, execution continues")
    
    print("\n" + "="*70)
    print(f"\n{UI.COLORS['GREEN']}✓ All keyboard interrupts handled gracefully!{UI.COLORS['END']}")
    print(f"\n{UI.COLORS['BOLD']}In the main application:{UI.COLORS['END']}")
    print("  • Ctrl+C at login → Asks if you want to exit")
    print("  • Ctrl+C in menu → Asks if you want to logout")
    print("  • Ctrl+C during operation → Returns to previous menu")
    print("  • Always clean database disconnection")
    print("  • No crashes, no stack traces, no confusion!")
    
    print(f"\n{UI.COLORS['CYAN']}Start the app with: python main_enhanced.py{UI.COLORS['END']}\n")

if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n")
        UI.print_warning("Demo interrupted - but handled gracefully!")
        print(f"\n{UI.COLORS['BOLD']}Thank you!{UI.COLORS['END']}\n")
