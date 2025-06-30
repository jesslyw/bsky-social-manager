# Bluesky Social Manager

A social media agent combined with human-in-the-loop interface to engage with and manage mentions of your Bluesky account

The bot uses the [AT Protocol](https://atproto.com/) to communicate with Bluesky and is powered by [@skyware/bot](https://skyware.js.org/guides/bot/introduction/getting-started/).

It listens for mentions and replies to an account you provide. When it receives an incoming post it will trigger a LangGraph graph with the text from the post, and reply using the output from the flow.


## Features

- Auto-detects and replies to mentions using your knowledge base
- Suggests reposts, likes, and highlights feedback for engagement
- Flags negative mentions for quick action
- Human-in-the-loop moderation and reply editing


## Getting Started

### Prerequisites

- Node.js and npm installed
- Python 3.x installed


### Setup

**1. Clone the repository**

```
git clone git@github.com:jesslyw/social-media-agent.git
cd social-media-agent
```

**2. Configure environment variables**

- In the agent-api folder, create a .env file with the following keys:

```
BIL_API_KEY=[your_api_key_here]
BASE_URL=[your_base_url_here]
```

- In the bsky-bot folder, create a .env file with the following keys:

```
BSKY_HANDLE=[your_bluesky_handle]
BSKY_PASSWORD=[your_bluesky_password]
```

**3. Install dependencies and setup**

Run the setup script from the root folder to install and build both parts:

`npm run setup`

**4. Load documents into vector store**

`npm run load-docs`

**5. Start the app**

- Start the agent API server

`npm run start-api`

- Start the Bluesky bot

Open a separate terminal window and run:

`npm run start-bot`

**6. Test the system**

Mention your Bluesky handle in a post and monitor the mention in interface. From there, review, edit, and approve replies.

### Uploading data to Knowledge Base

In `load_documents.py` enter the path of the text file you would like to add to the knowledge base. New files are appended to the existing data.

`loader = TextLoader("[your_text_file_path]")`

For other file types (PDF, etc.) see LangChain's documentation on [document loaders](https://python.langchain.com/api_reference/community/document_loaders.html)

---

Bot based on [langflow-bluesky-bot](https://github.com/philnash/langflow-bluesky-bot), under the MIT License
