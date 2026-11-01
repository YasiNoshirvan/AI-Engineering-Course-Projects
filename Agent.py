import dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain.agents import create_agent
import requests
from langchain_tavily import TavilySearch

dotenv.load_dotenv()

# with Agent : HumanMessage('where is the capital of France?')
#  == 
# with Chat Bot : {'role' : 'user' , 'content' : 'what is the capital of France?'}

TavilySearch(max_results=1)

def get_weather(city: str):
    ''' get weather of a city.
        Args: 
          city: city name
    '''
    try:
        # Step 1: Find the city's coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={"name": city, "count": 1},
            timeout=10
        )
        geo_response.raise_for_status()

        locations = geo_response.json().get("results", [])

        if not locations:
            return {"error": f"City '{city}' not found."}

        location = locations[0]

        # Step 2: Get real weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()

        current = weather_response.json()["current"]

        # Step 3: Convert weather codes into descriptions
        code = current["weather_code"]

        if code == 0:
            condition = "Clear sky"
        elif code in [1, 2, 3]:
            condition = "Cloudy or partly cloudy"
        elif code in [45, 48]:
            condition = "Foggy"
        elif code in [51, 53, 55, 56, 57]:
            condition = "Drizzle"
        elif code in [61, 63, 65, 66, 67, 80, 81, 82]:
            condition = "Rainy"
        elif code in [71, 73, 75, 77, 85, 86]:
            condition = "Snowy"
        elif code in [95, 96, 99]:
            condition = "Thunderstorm"
        else:
            condition = "Unknown"

        # Step 4: Return the weather information
        return {
            "city": location["name"],
            "country": location["country"],
            "temperature": current["temperature_2m"],
            "unit": "Celsius",
            "weather": condition,
            "humidity": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "time": current["time"],
            "source": "Open-Meteo"
        }

    except (requests.RequestException, ValueError, KeyError) as e:
        return {"error": f"Unable to fetch weather: {e}"}


class Agent:
    def __init__ (self):
        self.llm = ChatGroq(model = 'openai/gpt-oss-20b' , temperature=0.5)
        self.messages = [
            SystemMessage('answer the given questions and use the provided tools whenever needed!')
        ]

        self.agent = create_agent(
            model = self.llm,
            tools = [get_weather]
        )

    def chat_loop (self):
        while True:
            user_input = input(
                'Ask something (type "q" to terminate):' ).strip().lower()
        
            if user_input == 'q':
                print('Good Luck')
                break
            self.messages.append(HumanMessage(user_input))
            # response = self.llm.invoke(self.messages)
            # self.messages.append(response)

            # print(response.content)

            response = self.agent.invoke({'messages' : self.messages})
            self.messages.append(response ['messages'][-1])
            print (response ['messages'][-1].content)


def main():
   #response = llm.invoke('what is the capita of France?')
   #print (response.content)
   #print(response.response_metadata)
   #print (response.usage_metadata)
   #print(response.tool_calls)

   agent = Agent()
   agent.chat_loop()


if __name__ == '__main__':
    main()