"""
Challenge 5 (Innovate): AWS DevOps Assistant 🚀

WHAT THIS AGENT DOES:
  An interactive AWS DevOps Assistant that:
  - 📚 Searches and reads live AWS documentation via the AWS Docs MCP server
  - 🧠 Remembers your architecture preferences across sessions (mem0 + FAISS)
  - ⚡ Streams responses in real time so you see answers as they are generated
  - 🛠️  Answers questions about any AWS service, best practices, and architecture

WHY IT'S USEFUL:
  Instead of switching between browser tabs to read AWS docs, you can ask
  natural-language questions and get accurate, doc-backed answers instantly.
  The agent also remembers your stack (e.g. "I use Python and CDK") so it
  tailors every answer to your context.

SETUP:
  pip install awslabs.aws-documentation-mcp-server faiss-cpu
  aws configure   # make sure Bedrock / Nova Pro is enabled

RUN:
  python starter.py
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import mem0_memory
from mcp import StdioServerParameters, stdio_client

MODEL = "us.amazon.nova-pro-v1:0"

# ── Streaming callback ────────────────────────────────────────────────────────
def stream_callback(**kwargs):
    """Print streamed text chunks and tool-use notifications."""
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs:
        tool_name = kwargs["current_tool_use"].get("name")
        if tool_name:
            print(f"\n📡 Fetching from AWS docs [{tool_name}]...", flush=True)


# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert AWS DevOps Assistant 🛠️ with access to:

1. 📚 AWS Documentation tools — search and read the latest official AWS docs
2. 🧠 mem0_memory — remember the user's architecture preferences, tech stack,
   and past questions so every answer is personalised

HOW TO BEHAVE:
- Always search the AWS docs before answering technical questions so your
  answers are accurate and up-to-date.
- When the user mentions their stack or preferences (e.g. "I use CDK",
  "my region is ap-south-1"), store that with mem0_memory.
- Recall stored preferences when they are relevant to the answer.
- Structure answers clearly: use bullet points, code blocks, and section
  headers where helpful.
- Be concise but thorough. If a topic is complex, offer to go deeper.
- Use emojis sparingly to keep the tone friendly without being distracting.

EXAMPLE QUESTIONS YOU CAN ANSWER:
- "What is the difference between SQS and SNS?"
- "How do I set up a VPC with private subnets?"
- "Remember that I use Python and deploy with CDK"
- "What's the best way to handle secrets in Lambda?"
- "Show me the IAM policy for S3 read-only access"
"""

# ── Banner ────────────────────────────────────────────────────────────────────
BANNER = """
╔══════════════════════════════════════════════════════════════╗
║          🛠️  AWS DevOps Assistant  (MCP + Memory)            ║
║                                                              ║
║  📚 Powered by: AWS Documentation MCP Server                 ║
║  🧠 Memory:     mem0 + FAISS (persists across sessions)      ║
║  ⚡ Streaming:  Real-time response output                     ║
╚══════════════════════════════════════════════════════════════╝

Tips:
  • Ask any AWS question — the agent reads live docs for you
  • Say "Remember I use [tech]" to personalise future answers
  • Type 'help' for example questions
  • Type 'quit' to exit
"""

HELP_TEXT = """
Example questions:
  📌 "What is Amazon ECS and when should I use it over EKS?"
  📌 "How do I enable versioning on an S3 bucket?"
  📌 "Remember that my primary region is ap-south-1 and I use Terraform"
  📌 "What IAM permissions does Lambda need to write to DynamoDB?"
  📌 "Explain the difference between ALB and NLB"
  📌 "What's my preferred region?" (recalls stored memory)
"""

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(BANNER)

    # Connect to the AWS Documentation MCP server via stdio transport
    aws_docs_mcp = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="awslabs.aws-documentation-mcp-server",
                env={**os.environ},   # pass current env (AWS creds, etc.)
            )
        )
    )

    with aws_docs_mcp:
        # Collect all tools exposed by the MCP server
        mcp_tools = aws_docs_mcp.list_tools_sync()

        # Build the agent: MCP doc tools + persistent memory + streaming
        agent = Agent(
            model=MODEL,
            tools=[*mcp_tools, mem0_memory],
            callback_handler=stream_callback,
            system_prompt=SYSTEM_PROMPT,
        )

        print("✅ Agent ready! AWS docs MCP server connected.\n")

        # ── Interactive chat loop ─────────────────────────────────────────────
        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ("quit", "exit", "q"):
                    print("\n👋 Goodbye! Your memories are saved for next time.")
                    break

                if user_input.lower() == "help":
                    print(HELP_TEXT)
                    continue

                print("\nAssistant: ", end="")
                agent(user_input)   # stream_callback handles printing
                print("\n")         # blank line after streamed response

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Your memories are saved for next time.")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}\n")
                continue


if __name__ == "__main__":
    main()
