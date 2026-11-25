"""
Interactive demo for Lab 01 – Multi-Agent Research Coordinator
"""

import json
from src.coordinator import Coordinator
from src.schemas import FinalAnswer


def pretty_print(answer: FinalAnswer):
    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(json.dumps(answer.model_dump(), indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")


def main():
    coordinator = Coordinator()

    print("Lab 01 – Multi-Agent Research Coordinator")
    print("Type a query (or 'quit' to exit)\n")

    while True:
        try:
            query = input("You > ").strip()
            if not query:
                continue
            if query.lower() in {"quit", "exit", "q"}:
                break

            print("\nRunning agents...")
            result = coordinator.run(query)
            pretty_print(result)

        except KeyboardInterrupt:
            print("\nBye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
