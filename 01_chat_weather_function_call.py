import os
import json
import urllib.parse
import urllib.request
from typing import Any, Dict

# pip install openai (v1+)
from openai import OpenAI


def _http_get_json(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    req = urllib.request.Request(full_url, headers={"User-Agent": "weather-tool/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    return json.loads(data.decode("utf-8"))


def get_current_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """
    Fetch real-time weather for a city using OpenWeather API.

    Returns a JSON-serializable dict the model can use to produce a final answer.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENWEATHER_API_KEY in environment")

    unit = unit.lower().strip()
    ow_units = "metric" if unit == "celsius" else "imperial"

    payload = {
        "q": location,
        "appid": api_key,
        "units": ow_units,
    }

    data = _http_get_json("https://api.openweathermap.org/data/2.5/weather", payload)

    # Normalize response
    weather_list = data.get("weather", [])
    description = weather_list[0]["description"] if weather_list else "unknown"
    main = data.get("main", {})
    wind = data.get("wind", {})
    sys_info = data.get("sys", {})

    result = {
        "resolved_location": {
            "city": data.get("name"),
            "country": sys_info.get("country"),
        },
        "conditions": description,
        "temperature": main.get("temp"),
        "temperature_unit": "C" if ow_units == "metric" else "F",
        "humidity_percent": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "wind_speed_unit": "m/s" if ow_units == "metric" else "mph",
        "source": "OpenWeather",
    }
    return result


def main() -> None:
    # Configure OpenAI client
    client = OpenAI()

    # Ask for weather in "Pairis" on purpose; the model should infer Paris
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. When asked about weather, use the provided function "
                "to retrieve real-time data and then summarize it clearly for the user."
            ),
        },
        {
            "role": "user",
            "content": "What is the real-time weather in Pairis right now?",
        },
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get current weather for a city using OpenWeather.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name, optionally with country code (e.g., 'Paris, FR').",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Temperature unit preference.",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    first = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        # temperature=0.2,
    )

    msg = first.choices[0].message
    tool_calls = getattr(msg, "tool_calls", None) or []

    if tool_calls:
        # Handle the first tool call (typical for a single-function example)
        for call in tool_calls:
            if call.type == "function" and call.function and call.function.name == "get_current_weather":
                args = json.loads(call.function.arguments or "{}")
                location = args.get("location")
                unit = args.get("unit", "celsius")
                result = get_current_weather(location=location, unit=unit)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": "get_current_weather",
                        "content": json.dumps(result),
                    }
                )

        final = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
            # temperature=0.2,
        )
        print(final.choices[0].message.content)
    else:
        # Model chose to answer without a tool call (unlikely for weather)
        print(msg.content)


if __name__ == "__main__":
    # Required environment variables:
    # - OPENAI_API_KEY
    # - OPENWEATHER_API_KEY
    main()


