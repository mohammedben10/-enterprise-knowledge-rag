"""
Enterprise Knowledge Copilot — Interactive CLI
----------------------------------------------
Interactive command-line assistant for querying corporate policies,
benefits, travel limits, security standards, and customer SLAs.
"""

import sys
import textwrap
from rag_engine import EnterpriseRAGEngine


def print_banner():
    """Display welcome screen and usage instructions."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║      🏢 APEX GLOBAL TECHNOLOGIES — ENTERPRISE KNOWLEDGE COPILOT   ║
    ║   AI-Powered Policy, HR, Travel, Procurement & SLA Assistant     ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(textwrap.dedent(banner))
    print("💡 Quick tips:")
    print("   • Ask questions about PTO, flight policies, spending limits, SLAs, or security.")
    print("   • Type 'clear' to reset conversation memory.")
    print("   • Type 'exit', 'quit', or 'q' to close the assistant.\n")
    print("-" * 70)


def main():
    try:
        engine = EnterpriseRAGEngine()
    except Exception as err:
        print(f"\n❌ Startup Error: {err}")
        print("Please ensure your GOOGLE_API_KEY is set in .env and you have run 'python load_docs.py'.")
        sys.exit(1)

    print_banner()

    chat_history = []

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            # Handle empty prompts
            if not user_input:
                continue

            # Handle exit commands
            if user_input.lower() in ["exit", "quit", "q", "quitter"]:
                print("\n👋 Goodbye! Have a productive day at Apex Global.\n")
                break

            # Handle reset command
            if user_input.lower() in ["clear", "reset"]:
                chat_history.clear()
                print("🔄 Conversation memory cleared. Ready for a new topic!")
                continue

            print("\n🔍 Searching policy documents & formulating response...")
            result = engine.query(user_input, chat_history=chat_history)

            # Display answer
            print("\n🤖 Copilot:")
            print(result["answer"])

            # Display consulted sources
            if result.get("sources"):
                print("\n📚 Sources Consulted:")
                for src in result["sources"]:
                    print(f"   • {src['title']} ({src['file']})")

            print("-" * 70)

            # Save to conversation memory
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": result["answer"]})

        except KeyboardInterrupt:
            print("\n\nSession terminated by user. Goodbye!")
            break
        except Exception as err:
            print(f"\n⚠️ An unexpected error occurred: {err}")


if __name__ == "__main__":
    main()
