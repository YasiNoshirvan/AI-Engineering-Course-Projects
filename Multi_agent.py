
import re
import dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import ToolMessage

dotenv.load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)



fruits = {
    "tomato": "Botanically a fruit, but commonly used as a vegetable in cooking.",
    "apple": "A pome fruit related to roses. Contains fiber and vitamin C.",
    "banana": "A tropical fruit known for potassium and carbohydrates.",
    "orange": "A citrus fruit rich in vitamin C.",
    "strawberry": "An accessory fruit containing vitamin C and antioxidants.",
    "grape": "A small fruit that grows in clusters and contains antioxidants.",
    "mango": "A tropical stone fruit containing vitamins A and C.",
    "pineapple": "A tropical fruit containing vitamin C and bromelain.",
    "watermelon": "A fruit with high water content and lycopene.",
    "peach": "A stone fruit containing fiber and vitamin C.",
    "pear": "A sweet fruit containing dietary fiber.",
    "kiwi": "A small fruit rich in vitamin C and fiber.",
    "lemon": "A sour citrus fruit commonly used for juice and flavoring."}

vegetables = {
    "carrot": "A root vegetable containing beta-carotene, a source of vitamin A.",
    "potato": "A starchy tuber containing carbohydrates and potassium.",
    "broccoli": "A cruciferous vegetable containing fiber and vitamin C.",
    "spinach": "A leafy green vegetable containing iron, folate and vitamin K.",
    "lettuce": "A leafy vegetable commonly used in salads.",
    "onion": "A bulb vegetable used for flavoring many dishes.",
    "garlic": "A bulb vegetable known for its strong flavor.",
    "cabbage": "A leafy cruciferous vegetable containing fiber and vitamin C.",
    "cauliflower": "A cruciferous vegetable related to broccoli.",
    "celery": "A crunchy vegetable with high water content.",
    "radish": "A root vegetable with a peppery taste.",
    "beetroot": "A root vegetable containing folate and natural pigments.",
    "asparagus": "A vegetable containing folate and vitamin K."}


# Find food names in a question, including common plural forms
def find_foods(question: str, database: dict) -> list:
    results = []

    for name, description in database.items():
        if name.endswith("y"):
            plural = name[:-1] + "ies"
        elif name.endswith(("o", "ch", "sh")):
            plural = name + "es"
        else:
            plural = name + "s"

        pattern = rf"\b({re.escape(name)}|{re.escape(plural)})\b"

        if re.search(pattern, question, re.IGNORECASE):
            results.append(f"{name.title()}: {description}")

    return results


# Tools for the specialist agents
def fruit_info(fruit_name: str) -> str:
    """Look up information about one or more fruits mentioned in the input."""
    results = find_foods(fruit_name, fruits)
    if not results:
        return "NOT_FOUND: No matching fruit exists in the fruit database."
    return "\n".join(results)


def veggie_info(veggie_name: str) -> str:
    """Look up information about one or more vegetables mentioned in the input."""
    results = find_foods(veggie_name, vegetables)
    if not results:
        return "NOT_FOUND: No matching vegetable exists in the vegetable database."
    return "\n".join(results)



fruit_agent = create_agent(
    model=llm,
    tools=[fruit_info],
    system_prompt=(
        "You are a fruit expert. Always use fruit_info before answering. "
        "Use only the information returned by the tool. "
        "You can discuss and compare multiple fruits. "
        "If the tool returns NOT_FOUND, explain that the fruit is not "
        "available in the database. Do not invent facts. "
        "Keep your answers short and clear."
    )
)


veggie_agent = create_agent(
    model=llm,
    tools=[veggie_info],
    system_prompt=(
        "You are a vegetable expert. Always use veggie_info before answering. "
        "Use only the information returned by the tool. "
        "You can discuss and compare multiple vegetables. "
        "If the tool returns NOT_FOUND, explain that the vegetable is not "
        "available in the database. Do not invent facts. "
        "Keep your answers short and clear."
    )
)


def ask_fruit_expert(question: str) -> str:
    """Ask the fruit expert about fruits or fruit comparisons."""
    response = fruit_agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return response["messages"][-1].content


def ask_veggie_expert(question: str) -> str:
    """Ask the vegetable expert about vegetables or vegetable comparisons."""
    response = veggie_agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return response["messages"][-1].content



main_agent = create_agent(       # Main supervisor agent
    model=llm,
    tools=[ask_fruit_expert, ask_veggie_expert],
    system_prompt=(
        "You are a food assistant supervising two specialist agents. "
        "Use ask_fruit_expert for fruit questions and ask_veggie_expert "
        "for vegetable questions. "
        "For questions involving both fruits and vegetables, call BOTH experts. "
        "For comparisons within one category, call the corresponding expert. "
        "Use the experts for all food-related questions. "
        "The fruit database contains: " + ", ".join(fruits.keys()) + ". "
        "The vegetable database contains: " + ", ".join(vegetables.keys()) + ". "
        "Tomato is classified as a fruit in this project. "
        "If a food is not listed, ask the relevant expert to check it. "
        "Only use information provided by the experts. "
        "If information is unavailable, say so instead of guessing. "
        "Combine the expert responses into one clear answer. "
        "Keep your answers concise."
    )
)


def ask_question(question: str):    # Run the supervisor and track which experts were called
    response = main_agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    used_experts = set()
    for message in response["messages"]:
        if isinstance(message, ToolMessage):
            if message.name in ["ask_fruit_expert", "ask_veggie_expert"]:
                used_experts.add(message.name)
    answer = response["messages"][-1].content
    return answer, used_experts


def main():   # Interactive chatbot
    print("FoodIQ - Multi-Agent Food Assistant")
    print("Ask me anything about fruits and vegetables!")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            answer, used_experts = ask_question(question)

            print("\nFoodIQ:", answer)

            experts = []
            if "ask_fruit_expert" in used_experts:
                experts.append("Fruit Expert")
            if "ask_veggie_expert" in used_experts:
                experts.append("Vegetable Expert")

            print("Experts used:", ", ".join(experts) or "None")
            print()

        except Exception as error:
            print(f"\nError: {error}")
            print("Check your API key, connection or Groq rate limits.\n")


if __name__ == "__main__":
    main()

