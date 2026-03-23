import requests


# 1. Calculator
def calculator(expr: str) -> str:
    """Evaluate a math expression and return the result as text."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"


# 2. Joke generator
def joke(topic: str) -> str:
    """Tell a quick joke about a given topic."""
    return (
        f"Here’s a {topic}-themed joke: "
        f"Why did the {topic} cross the road? To learn Agentic AI!"
    )


# 3. Weather (demo API call using Open-Meteo geocoding endpoint)
def weather(city: str) -> str:
    """Get demo weather info for a city using Open-Meteo geocoding."""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        r = requests.get(url, timeout=10).json()
    except Exception as e:
        return f"Weather lookup failed: {e}"

    if "results" not in r or not r["results"]:
        return f"No weather info for {city}"

    coords = r["results"][0]
    return (
        f"{city} located at lat {coords['latitude']}, "
        f"lon {coords['longitude']} (demo response)."
    )


tools = [calculator, joke, weather]


if __name__ == "__main__":
    print("Calculator:", calculator("2 + 3 * 4"))
    print("Joke:", joke("python"))
    print("Weather:", weather("Chicago"))
    print("Loaded tools:", [t.name for t in tools])
