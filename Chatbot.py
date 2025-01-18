import os
import getpass
import gradio as gr
from typing import Sequence
from typing_extensions import Annotated, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    trim_messages,
    BaseMessage,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langgraph.graph.message import add_messages

# Define the State Schema
"""
A state schema is like a blueprint that defines how we organize and store 
information in our chatbot. It helps the chatbot keep track of important details, 
such as the messages exchanged and other constraints.

Messages: This is a list holding all messages that have been sent and received 
          during the conversation. One can think of each message as a piece of the chat history.

Language: This is a simple text field that stores the user's preferred language 
          for communication. This is to ensure that the chatbot answers back in the correct language.
"""
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

# Configure the AI Model
"""
initialize chatbot's core functionalities
"""
class Model:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            google_api_key = os.getenv("GOOGLE_API_KEY")
        )

        # Define Prompt Template
        """
        The chatbot uses a prompt template to define its behavior
        """
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        # Implement the Workflow
        """
        1. self.workflow = StateGraph(state_schema=State)
            This line creates a new workflow called workflow using a `StateGraph`. A StateGraph is a structure that helps in 
            managing the flow of data and actions in a program. The `state_schema=State` part means that the workflow will use a 
            specific format or structure for the data it will handle, defined by `State`.

        2. self.workflow.add_edge(START, "model")
            Here, an "edge" which is similar to a connection or a path is added to the workflow.

        3. self.workflow.add_node("model", self.call_model)
            This line introduces a new "node" (which is a specific task or function) into the workflow.

        4. self.memory = MemorySaver()
            This line establishes a memory storage system called memory with the MemorySaver.

        5. self.app = self.workflow.compile(checkpointer=self.memory)
            this line compiles the workflow into a runnable application called app.
            checkpointer=self.memory part means that the workflow will use the MemorySaver to keep track of its state while it runs.
        """

        self.workflow = StateGraph(state_schema=State)
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)

        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

        # Setup Trimmer
        """
        `self.trimmer` to handle message histories
        """
        self.trimmer = trim_messages(
            max_tokens=65,
            strategy="last",
            token_counter=self.model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )

    #Call the AI Model
    """
    `call_model` function processes inputs, generates responses, and updates memory
    """
    def call_model(self, state: State):
        if not state["messages"] or len(state["messages"]) == 1:
            state["messages"] = self.chat_message_history.messages + state["messages"]
        print(state["messages"])
        trimmed_messages = self.trimmer.invoke(state["messages"])
        prompt = self.prompt_template.invoke(
            {"messages": trimmed_messages, "language": state["language"]}
        )
        response = self.model.invoke(prompt)

        self.chat_message_history.add_user_message(prompt.messages[-1].content)
        self.chat_message_history.add_ai_message(response.content)

        return {"messages": [response]}

    def invoke(self, query, config, chat_message_history):
        self.chat_message_history = chat_message_history
        input_messages = [HumanMessage(query)]
        response = self.app.invoke(
                {"messages": input_messages, "language": "en"}, config
        )
        return response["messages"][-1].content

# Create Chat Interface Class
class ChatInterface:
    def __init__(self):
        self.model = Model()
        self.active_users = {}

    def get_chat_history(self, user_id):
        return MongoDBChatMessageHistory(
            session_id=user_id,
            connection_string=os.getenv("Mongo_URI"),
            database_name="Chatbot",
            collection_name="chat_histories",
        )

    def chat(self, message, history, user_id, language="English"):
        try:
            if not user_id:
                return "", history, "Please enter a user ID first."
            
            config = {"configurable": {"thread_id": user_id}}
            chat_history = self.get_chat_history(user_id)
            
            response = self.model.invoke(message, config, chat_history)
            return "", history + [(message, response)], ""
        except Exception as e:
            return "", history, f"Error: {str(e)}"

    def reset_chat(self, user_id):
        try:
            if not user_id:
                return None, "Please enter a user ID first"
            chat_history = self.get_chat_history(user_id)
            chat_history.clear()
            return None, f"Chat history cleared for user {user_id}"
        except Exception as e:
            return None, f"Error clearing chat: {str(e)}"
    
# Create the Gradio Interface
def create_gradio_interface():
    chat_interface = ChatInterface()

    custom_css = """
        .gradio-container {
            max-width: 800px !important;
            margin: auto !important;
            padding: 20px !important;
            background-color: #f7f7f7 !important;
        }
        .chat-message {
            padding: 15px !important;
            border-radius: 10px !important;
            margin: 5px !important;
        }
        .message-wrap {
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
        }
    """

    with gr.Blocks(css="footer {visibility: hidden}") as demo:
        with gr.Column(elem_id="chat-container"):
            gr.Markdown(
                """
                # 🤖 AI Chatbot with Memory
                Welcome to your personal AI assistant! Enter your ID and start chatting.
                """
            )
            
            with gr.Row():
                with gr.Column(scale=3):
                    user_id = gr.Textbox(
                        label="🆔 User ID",
                        placeholder="Enter Your User ID",
                        elem_id="user-id"
                    )
                with gr.Column(scale=1):
                    language = gr.Dropdown(
                        choices=["English", "Spanish", "French", "German", "Chinese"],
                        value="English",
                        label="🌐 Language",
                        elem_id="language"
                    )

            chatbot = gr.Chatbot(
                label="💬 Chat History",
                height=500,
                bubble_full_width=False,
                show_label=True,
                elem_id="chatbot"
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="✍️ Message",
                    placeholder="Type your message here...",
                    show_label=True,
                    elem_id="message"
                )
                submit = gr.Button("🚀 Send", variant="primary")

            clear = gr.Button("🗑️ Clear Chat", variant="secondary")
            status_msg = gr.Markdown("")

            # Event handlers
            submit.click(
                fn=chat_interface.chat,
                inputs=[msg, chatbot, user_id, language],
                outputs=[msg, chatbot, status_msg]
            )

            msg.submit(
                fn=chat_interface.chat,
                inputs=[msg, chatbot, user_id, language],
                outputs=[msg, chatbot, status_msg]
            )

            clear.click(
                fn=chat_interface.reset_chat,
                inputs=[user_id],
                outputs=[chatbot, status_msg]
            )
  
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=True)