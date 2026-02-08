"""
Entry point for the Jarvis Multi-Agent System
Run this script to analyze client documents and generate outreach emails.
"""
import sys
from pathlib import Path

# Add the current directory to sys.path to allow imports
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

try:
    from agentic_system import run_overnight_analysis
except ImportError as e:
    print(f"❌ Error: Could not import agentic_system. {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Jarvis Autonomous Multi-Agent Analysis...")
    try:
        results = run_overnight_analysis()
        print("\n✅ Analysis complete!")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
