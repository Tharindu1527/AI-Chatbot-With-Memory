---
title: Langchain_with_Mongodb
app_file: Chatbot.py
sdk: gradio
sdk_version: 5.12.0
---
# Chatbot with Memory

Welcome to the **Chatbot with Memory** project! This AI-powered chatbot leverages state-of-the-art frameworks and tools to deliver a coherent and contextual conversational experience. With multi-language support and persistent memory, this chatbot is designed to engage users effectively across sessions.

## Key Features

1. **LangChain**: A robust framework for building applications powered by language models, allowing seamless integration of prompts, memory, and custom workflows.
2. **LangGraph**: Enhances LangChain by enabling graph-based stateful workflows, ensuring systematic management of conversation states.
3. **Memory Integration**: Provides the chatbot with the ability to recall previous interactions, offering a consistent and context-aware experience.
4. **MongoDB**: A NoSQL database for storing chat history persistently, enabling long-term memory even across multiple sessions.
5. **Multi-language Support**: Allows users to interact with the chatbot in various languages.
6. **Gradio Interface**: Provides an intuitive and user-friendly interface for seamless interaction.

## How It Works

1. **User Input**: The chatbot captures and processes user queries from multiple users.
2. **Chat History**: Retrieves and updates conversation logs stored in MongoDB.
3. **AI Interaction**: Leverages Gemini AI to process queries and provide meaningful responses.
4. **Memory Management**: Ensures conversational continuity by recalling past interactions.

## Resources

For a detailed explanation of how to build a chatbot with memory capabilities, check out this [comprehensive tutorial](https://cckeh.hashnode.dev/building-chatbots-with-memory-capabilities-a-comprehensive-tutorial-with-langchain-langgraph-gemini-ai-and-mongodb).

## Live Demo

Experience the chatbot live on Hugging Face Spaces: [Chatbot With Memory](https://huggingface.co/spaces/Tharindu1527/Chatbot_With_Memory)

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Tharindu1527/Chatbot_With_Memory.git
   cd Chatbot_With_Memory
   ```

2. **Install Dependencies**
   Ensure you have Python 3.8 or later installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MongoDB**
   - Install and configure MongoDB.
   - Create a database and collection to store chat history.
   - Update the MongoDB connection details in the configuration file.

4. **Run the Application**
   ```bash
   python Chatbot.py
   ```

5. **Access the Gradio Interface**
   Open your browser and navigate to `http://localhost:7860` to interact with the chatbot.

## Usage

- Enter your query in the Gradio interface.
- Choose your preferred language for interaction.
- View responses that consider the chat context and memory.
- Switch between languages as needed for multi-lingual support.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

Special thanks to the authors of the following resources and tools:
- [LangChain](https://langchain.readthedocs.io/)
- [LangGraph](https://github.com/langgraph/langgraph)
- [Gemini AI](https://gemini.ai/)
- [Gradio](https://gradio.app/)
- [MongoDB](https://www.mongodb.com/)

---

We hope you enjoy exploring and using the Chatbot with Memory! If you have any feedback or feature requests, please let us know.
