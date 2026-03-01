import os
from dotenv import load_dotenv
from autogen import AssistantAgent, GroupChat, GroupChatManager

load_dotenv()

config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY")
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7
}


def create_agents():

    snob = AssistantAgent(
        name="FilmSnob",
        system_message="""
You are a dramatic film snob.
Use witty sarcasm.
Max 60 words.
Be funny but sharp.
""",
        llm_config=llm_config
    )

    entertainer = AssistantAgent(
        name="MassEntertainer",
        system_message="""
You love fun and chaos.
Mock boring films.
Be loud, funny, max 60 words.
""",
        llm_config=llm_config
    )

    therapist = AssistantAgent(
        name="CinemaTherapist",
        system_message="""
You analyze emotions like a therapist.
Be gently funny.
Max 60 words.
""",
        llm_config=llm_config
    )

    judge = AssistantAgent(
        name="Judge",
        system_message="""
You are a strict but witty judge.
Give final verdict.
Short, punchy, max 80 words.
Ensure age appropriateness.
""",
        llm_config=llm_config
    )

    return snob, entertainer, therapist, judge


def run_debate(mood, age, candidates_text):

    snob, entertainer, therapist, judge = create_agents()

    groupchat = GroupChat(
        agents=[snob, entertainer, therapist],
        messages=[],
        max_round=3
    )

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )

    intro_message = f"""
        User mood: {mood}
        User age: {age}
        
        Candidate Movies:
        {candidates_text}
        
        Debate for two rounds.
        After debate ends, stop.
        """

    snob.initiate_chat(manager, message=intro_message)

    transcript = groupchat.messages

    debate_text = ""
    for msg in transcript:
        debate_text += f"{msg['name']}: {msg['content']}\n\n"

    verdict = judge.generate_reply(
        messages=[{
            "role": "user",
            "content": f"""
            User mood: {mood}
            User age: {age}
            
            Debate Transcript:
            {debate_text}
            
            Give final verdict.
            Choose ONE movie.
            """
        }]
    )

    return f"""
    ## 🎤 Debate Transcript

    {debate_text}

    ---

    ## ⚖️ Final Verdict

    {verdict}
    """