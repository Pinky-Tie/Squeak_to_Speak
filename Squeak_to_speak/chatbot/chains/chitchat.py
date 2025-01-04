from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

from chatbot.chains.base import PromptTemplate, generate_prompt_templates


class ChitChatResponseChain(Runnable):
    def __init__(self, llm, memory=True):
        super().__init__()

        self.llm = llm
        prompt_template = PromptTemplate(
            system_template=""" 
              As an AI conversational assistant engaging in friendly interactions for Squeak to Speak,
              your main objectives are to maintain a compassionate tone, highlight Squeak to Speak's focus on mental health support, and emphasize our commitment to creating safe, personalized user experiences.
              Limit your answers to a maximum of 40 words.

              Here's how you should approach these interactions:

              1. Tone and Engagement:
              Use a warm, empathetic, and supportive tone to make users feel heard, valued, and comfortable.
              Keep the conversation inviting and encouraging, fostering trust and openness with Squeak to Speak.

              2. Personalization:
              Leverage conversation history and user preferences to provide thoughtful and meaningful responses.
              Show genuine care by recalling past interactions and tailoring recommendations to the user's needs.
              3. Focus on Squeak to Speak's Core Areas:
              Seamlessly integrate mentions of mental health resources, such as personalized therapist recommendations, alternative routines, or mood tracking features, into the conversation.
              Gently guide the discussion toward Squeak to Speak's mission of supporting emotional well-being whenever appropriate, such as by sharing calming exercises or gratitude prompts.
              4. Handling Irrelevant Questions:
              Politely redirect unrelated inquiries back to Squeak to Speak's focus.
              For example, if asked, "What is the capital of Portugal?", you might respond with:
              "I'm here to help with your mental health journey. Speaking of support, have you tried our journaling feature or gratitude banner?"
              5. Building Rapport:
              Prioritize creating a safe, welcoming environment that encourages users to explore Squeak to Speak's features.
              Foster a sense of emotional support and understanding, making users feel comfortable sharing their thoughts or concerns.
              Your ultimate goal is to empower users on their mental health journey through your empathetic demeanor and thoughtful conversational techniques.

              Here is the user input:
              {customer_input}
            """,
            human_template="Customer Query: {customer_input}",
        )

        self.prompt = generate_prompt_templates(prompt_template, memory)
        self.output_parser = StrOutputParser()

        self.chain = self.prompt | self.llm | self.output_parser

    def invoke(self, input, config=None, **kwargs):
        return self.chain.invoke(input, config=config)


class ChitChatClassifier(BaseModel):

    chitchat: bool = Field(
        description="""Chitchat is defined as:
        - Conversations that are informal, social, or casual in nature.
        - Topics that do not directly relate to specific user problems, situations or company values and mission.
        - Examples include greetings, jokes, small talk, or personal inquiries unrelated to any of the  previous messages. As well as describing an activity, day or event.
        If the user message falls under this category, set 'chitchat' to True.""",
    )


class ChitChatClassifierChain(Runnable):
    def __init__(self, llm, memory=False):
        super().__init__()

        self.llm = llm
        prompt_template = PromptTemplate(
            system_template=""" 
            You are specialized in distinguishing between chitchat and actual requests from user messages.
            Your task is to analyze each incoming user message and determine if it falls under 'chitchat'. 
            Consider the Context:
            - Analyze the user's message in the context of the entire chat history.
            - Check if previous messages in the conversation are related to a specific request or 
            customer-service oriented that might help classify borderline cases.
            - Requests for to keep the user company, tell a story or just chat fall in the chitchat category.

            Here is the user input:
            {customer_input}

            Here is the chat history:
            {chat_history}

            Output Output your results clearly on the following format:  
            {format_instructions}
            """,
            human_template="Customer Query: {customer_input}",
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)

        self.output_parser = PydanticOutputParser(pydantic_object=ChitChatClassifier)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.chain = (self.prompt | self.llm | self.output_parser).with_config(
            {"run_name": self.__class__.__name__}
        )  # Add a run name to the chain on LangSmith

        self.chain = self.prompt | self.llm | self.output_parser

    def invoke(self, input, config=None, **kwargs) -> ChitChatClassifier:
        result = self.chain.invoke(
            {
                "customer_input": input["customer_input"],
                "chat_history": input["chat_history"],
                "format_instructions": self.format_instructions,
            },
        )
        return result
