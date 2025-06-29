import { Bot, Post } from "@skyware/bot";
import {
  StateGraph,
  START,
  END,
  Annotation,
  Command,
} from "@langchain/langgraph";
import * as readline from "node:readline/promises";
import { stdin, stdout } from "node:process";
import { MyGraphState } from "../graphStateType.js";

const State = Annotation.Root({
  user_input: Annotation<string>(),
  graph_output: Annotation<string>(),
});

class HilNodeQueue {
  private queue: (() => Promise<void>)[] = [];
  private running = false;

  async enqueue(task: () => Promise<void>) {
    this.queue.push(task);
    if (!this.running) {
      this.running = true;
      await this.runNext();
    }
  }

  private async runNext() {
    const next = this.queue.shift();
    if (next) {
      await next();
      await this.runNext();
    } else {
      this.running = false;
    }
  }
}

const hilQueue = new HilNodeQueue();

async function hilNode(
    state: typeof State.State
): Promise<typeof State.State | Command> {
  const rl = readline.createInterface({ input: stdin, output: stdout });

  try {
    const action = JSON.parse(state.graph_output);
    const output = action.data.graph_output;

    console.log("Vorgeschlagene Aktion:");
    console.log(`  Ausgangskommentar: ${output.comment}`);
    console.log(`  Reply: ${output.reply}`);
    console.log(`  Like: ${output.like}`);
    console.log(`  Repost: ${output.repost}`);
    console.log(`  Reply-Text: ${output.reply_text ?? "(leer)"}`);

    while (true) {
      const approval = await rl.question("Genehmigen? (y/n/e = edit): ");

      if (approval.toLowerCase() === "y") {
        console.log("Aktion angenommen. Alle Interaktionen werden ausgeführt.");
        return {
          ...state,
          graph_output: JSON.stringify({
            reply: output.reply,
            like: output.like,
            repost: output.repost,
            reply_text: output.reply_text,
          }),
        };
      } else if (approval.toLowerCase() === "n") {
        console.log("Aktion abgelehnt. Alle Interaktionen deaktiviert.");
        return {
          ...state,
          graph_output: JSON.stringify({
            reply: false,
            like: false,
            repost: false,
            reply_text: "",
          }),
        };
      } else if (approval.toLowerCase() === "e") {
        const editedText = await rl.question(
            "Bitte neuen Antworttext eingeben/Antworttext korrigieren:\n"
        );
        action.data.graph_output.reply_text = editedText;
        action.data.graph_output.reply = true;

        const likeInput = await rl.question("Like setzen? (y/n): ");
        const repostInput = await rl.question("Reposten? (y/n): ");

        const like = likeInput.toLowerCase() === "y";
        const repost = repostInput.toLowerCase() === "y";

        action.data.graph_output.like = like;
        action.data.graph_output.repost = repost;

        console.log("Antworttext aktualisiert:\n", editedText);
        console.log(`Like: ${like ? "Ja" : "Nein"}, Repost: ${repost ? "Ja" : "Nein"}`);
      }
      else {
        console.log("Ungültige Eingabe. Bitte y (ja), n (nein) oder e (editieren) eingeben.");
      }
    }
  } finally {
    rl.close();
  }
}

const graph = new StateGraph(State)
    .addNode("hil", hilNode)
    .addEdge(START, "hil")
    .addEdge("hil", END)
    .compile();

const bot = new Bot();
await bot.login({
  identifier: process.env.BSKY_HANDLE!,
  password: process.env.BSKY_PASSWORD!,
});

bot.on("reply", respondToIncoming);
bot.on("mention", respondToIncoming);
console.log(`[✓] @${process.env.BSKY_HANDLE} lauscht auf Erwähnungen und Antworten... 🤖`);


async function respondToIncoming(post: Post) {
  await hilQueue.enqueue(async () => {
    try {
      const response = await getLanggraphResponse(post.text);
      if (!response) return;

      if (response.reply && response.reply_text) {
        await post.reply({ text: response.reply_text });
      }
      if (response.like) {
        await post.like();
      }
      if (response.repost) {
        await post.repost();
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(`[✗] ${error.name}: ${error.message}`);
      }
    }
  });

  // console.log(`[✓] Antwort von @${post.author.handle} verarbeitet.`);
}

async function getLanggraphResponse(text: string) {
  const incoming_data = JSON.stringify({ input_data: text });

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze-comment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: incoming_data,
    });


    const data = await response.json();
    const graphData = data as MyGraphState;
    const graphOutputString = JSON.stringify(graphData);

    const result = await graph.invoke({
      user_input: text,
      graph_output: graphOutputString,
    });

    return JSON.parse(result.graph_output);
  } catch (error) {
    console.error("Error at getLanggraphResponse:", error);
    return null;
  }
}
