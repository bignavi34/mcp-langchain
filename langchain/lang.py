from groq import Groq
API_KEY = "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"
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain.prompts import ChatPromptTemplate
llm = ChatOpenAI(
    openai_api_key=API_KEY,         # Groq API key
    openai_api_base="https://api.groq.com/openai/v1",  # Groq's base URL
    model="llama3-8b-8192",
    temperature=0.0,# or "llama3-70b-8192"
)

class State(TypedDict):
    application:str
    experience:str
    skillmatch:str
    response:str
workflow=StateGraph(State)
def Exxperience(state:State):
    prompt = ChatPromptTemplate.from_template(
    "You are an expert HR assistant. Based only on the following job application:\n\n"
    "{application}\n\n"
    "Categorize the candidate strictly as one of the following: 'senior-level', 'middlelevel', or 'entrylevel'.\n"
    "Respond with **only** one of those exact words. Return an empty response if the input is meaningless or does not allow categorization.\n"
    "Do not add any explanation, punctuation, or extra text. Output must be exactly one word from the list or nothing."
)
    chain=prompt|llm
    experience=chain.invoke({"application":state["application"]}).content
    return {"experience":experience}
def assesedskilled(state:State):
    prompt = ChatPromptTemplate.from_template(
    "Based on the job application for a Python Developer, assess the candidate's skillset. "
    "Strictly Respond with either 'match' or 'nomatch'. Application: {application}"
    )
    chain=prompt|llm
    skillwdmatch=chain.invoke({"application":state["application"]}).content
    return {"skillmatch":skillwdmatch}
def scheduleinterview(state:State):
    return {"response":"candidate has been shortlisted"}
def escalate(state:State):
    return {"response":"candidate has senior-level"}
def reject(state:State):
    return {"response":"candidate is rejected"}
def routeapp(state: State):
    if state["skillmatch"].strip().lower() == "match":
        return "schinterview"

    # Escalate if experience is senior-level, regardless of skillmatch
    if state["experience"].strip().lower() == "senior-level":
        return "escalate"
    else:
        return "reject"

workflow.add_node("experiences", Exxperience)
workflow.add_node("assesskilled", assesedskilled)
workflow.add_node("schinterview", scheduleinterview)
workflow.add_node("escalate", escalate)
workflow.add_node("reject", reject)

# Add missing edge to make sure assesskilled runs
workflow.add_edge(START, "experiences")
workflow.add_edge("experiences", "assesskilled")  # <-- Important!
workflow.add_conditional_edges("assesskilled", routeapp)
workflow.add_edge("assesskilled",END)
workflow.add_edge("schinterview", END)
workflow.add_edge("escalate", END)
workflow.add_edge("reject", END)
inputs=input("enter the applications:")
# Compile and run
m = workflow.compile()
output = m.invoke({"application":inputs})

print({"experiencelevel": output.get("experience")})
print({"skillmatch": output.get("skillmatch")})
print({"response": output.get("response")})



