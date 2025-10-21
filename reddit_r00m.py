import sys
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

Bearer = os.getenv('Bearer')


def _ensure_bearer():
    """Prompt for a Bearer token if it is missing from the environment."""
    global Bearer
    if Bearer:
        return
    Bearer = input("Enter Bearer token: ").strip()
    if not Bearer:
        raise ValueError("Bearer token is required to use the API.")

def get_quota():
    headers = {
        "Authorization": f"Bearer {Bearer}"
    }
    quota = requests.get("https://api.r00m101.com/quota", headers=headers)
    if quota.status_code != 200:
        return f"Error: {quota.status_code} - {quota.text}"
    try:
        return quota.json()
    except requests.exceptions.JSONDecodeError:
        return quota.text

AVAILABLE_MODELS = [
    "x-ai/grok-3-mini",
    "x-ai/grok-4",
    "x-ai/grok-4-fast",
    "google/gemini-2.0-flash-001",
    "google/gemini-2.0-flash-lite-001",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-flash-lite",
    "google/gemini-2.5-pro",
    "deepseek/deepseek-chat-v3-0324",
    "deepseek/deepseek-r1-0528",
    "deepseek/deepseek-r1-0528:free",
    "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
]


def _prompt_boolean(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in {"true", "t", "yes", "y", "1"}:
            return True
        if value in {"false", "f", "no", "n", "0"}:
            return False
        print("Please enter true/false (or y/n).")


def _prompt_model():
    while True:
        print("Available models:")
        for idx, model in enumerate(AVAILABLE_MODELS, start=1):
            print(f"{idx}. {model}")
        value = input("Pick a model by number or provide a model string: ").strip()
        if not value:
            print("Model is required.")
            continue
        if value.isdigit():
            index = int(value) - 1
            if 0 <= index < len(AVAILABLE_MODELS):
                return AVAILABLE_MODELS[index]
            print("Invalid selection, please provide a model string.")
            continue
        if value in AVAILABLE_MODELS:
            return value
        use_custom = _prompt_boolean(
            f"'{value}' is not in the list. Use it anyway? (true/false): "
        )
        if use_custom:
            return value


def _prompt_use_case():
    while True:
        value = input("Use case (leave blank or type 'law_enforcement'): ").strip()
        if value in {"", "law_enforcement"}:
            return value
        print("Only 'law_enforcement' or blank is allowed. Please try again.")


def analyze_username():
    headers = {
        "Authorization": f"Bearer {Bearer}"
    }

    username = input("Enter Reddit username: ").strip()
    if not username:
        return "Error: username is required."

    model = _prompt_model()
    latest = _prompt_boolean("Fetch latest messages? (true/false): ")
    refresh = _prompt_boolean("Force re-processing? (true/false): ")
    sources = _prompt_boolean("Verify sources? (true/false): ")

    use_case = _prompt_use_case()

    params = {
        "model": model,
        "latest": latest,
        "refresh": refresh,
        "sources": sources,
    }

    if use_case:
        params["use_case"] = use_case

    analyze = requests.get(
        f"https://api.r00m101.com/analyze/{username}",
        headers=headers,
        params=params
    )
    if analyze.status_code != 200:
        return f"Error: {analyze.status_code} - {analyze.text}"
    try:
        return json.dumps(analyze.json(), indent=4)
    except requests.exceptions.JSONDecodeError:
        return analyze.text


def get_username():
    headers = {
        "Authorization": f"Bearer {Bearer}",
        "Accept": "text/csv"
    }

    username = input("Enter Reddit username: ").strip()
    if not username:
        return "Error: username is required."

    latest = _prompt_boolean("Fetch latest messages? (true/false): ")

    params = {
        "latest": latest
    }

    user = requests.get(
        f"https://api.r00m101.com/user/{username}",
        headers=headers,
        params=params
    )
    if user.status_code != 200:
        return f"Error: {user.status_code} - {user.text}"
    csv_content = user.text.strip()
    if not csv_content:
        return "No comment history found."

    # API may wrap the CSV in an error message string; strip it out
    lowered = csv_content.lower()
    if lowered.startswith("can't parse json"):
        _, _, remainder = csv_content.partition("Raw result:")
        csv_content = remainder.strip()

    if not csv_content:
        return "No comment history found."

    return csv_content


def get_subscribers():
    headers = {
        "Authorization": f"Bearer {Bearer}",
        "Accept": "application/json"
    }

    subreddit = input("Enter subreddit name: ").strip()
    if not subreddit:
        return "Error: subreddit name is required."

    response = requests.get(
        f"https://api.r00m101.com/subreddit/{subreddit}",
        headers=headers
    )
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    try:
        return json.dumps(response.json(), indent=4)
    except requests.exceptions.JSONDecodeError:
        return response.text


def search():
    headers = {
        "Authorization": f"Bearer {Bearer}",
        "Accept": "application/json"
    }

    raw_terms = input("Enter search terms (comma separated): ").strip()
    if not raw_terms:
        return "Error: at least one search term is required."

    terms = [term.strip() for term in raw_terms.split(",") if term.strip()]
    if not terms:
        return "Error: at least one search term is required."

    from_timestamp = input("From timestamp (unix, leave blank for no lower bound): ").strip()
    to_timestamp = input("To timestamp (unix, leave blank for current time): ").strip()

    params = []
    for term in terms:
        params.append(("terms", term))
    if from_timestamp:
        params.append(("from", from_timestamp))
    if to_timestamp:
        params.append(("to", to_timestamp))

    response = requests.get(
        "https://api.r00m101.com/search",
        headers=headers,
        params=params
    )
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    try:
        return json.dumps(response.json(), indent=4)
    except requests.exceptions.JSONDecodeError:
        return response.text


def _display_menu():
    print("\nChoose an option:")
    print("1. Analyze username")
    print("2. Get username history")
    print("3. Get subreddit subscribers")
    print("4. Search submissions")
    print("5. Check quota")
    print("Q. Quit")

def main():
    # Exit cleanly in non-interactive environments (e.g., Docker Compose, CI/CD)
    if not sys.stdin.isatty():
        print("🔹 Non-interactive environment detected — exiting.")
        sys.exit(0)

    try:
        _ensure_bearer()
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    options = {
        "1": ("Analyze username", analyze_username),
        "2": ("Get username history", get_username),
        "3": ("Get subreddit subscribers", get_subscribers),
        "4": ("Search submissions", search),
        "5": ("Check quota", get_quota),
    }

    while True:
        _display_menu()
        try:
            choice = input("Select an option: ").strip().lower()
        except EOFError:
            print("\n🔹 Input stream closed — exiting.")
            break

        if choice in {"q", "quit", "exit"}:
            print("Goodbye!")
            break

        action = options.get(choice)
        if not action:
            print("Invalid selection. Please try again.")
            continue

        label, func = action
        print(f"\n--- {label} ---")
        try:
            result = func()
            if result is not None:
                print(result)
        except Exception as exc:
            print(f"Unexpected error: {exc}")

        input("\nPress Enter to return to the menu...")



if __name__ == "__main__":
    main()
