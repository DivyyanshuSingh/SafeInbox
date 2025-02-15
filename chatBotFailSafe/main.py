import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");

  const fetchResponse = async (userMessage) => {
    try {
      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": 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,
        },
        body: JSON.stringify({
          model: "gpt-3.5-turbo",
          messages: [{ role: "user", content: userMessage }],
        }),
      });
      const data = await response.json();
      return data.choices[0].message.content;
    } catch (error) {
      console.error("Error fetching response: ", error);
      return "Sorry, something went wrong.";
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const newMessage = { text: input, sender: "user" };
    setMessages([...messages, newMessage]);
    setInput("");
    
    const botReply = await fetchResponse(input);
    setMessages((prev) => [...prev, { text: botReply, sender: "bot" }]);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <Card className="w-full max-w-md p-4 bg-white shadow-md rounded-2xl">
        <CardContent className="space-y-4 h-96 overflow-y-auto p-4 border border-gray-200 rounded-lg">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`p-2 rounded-lg w-fit max-w-xs ${
                msg.sender === "user"
                  ? "bg-blue-500 text-white self-end ml-auto"
                  : "bg-gray-200 text-black"
              }`}
            >
              {msg.text}
            </div>
          ))}
        </CardContent>
        <div className="flex items-center gap-2 mt-4">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1"
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <Button onClick={handleSend} className="bg-blue-500 text-white">
            <Send size={16} />
          </Button>
        </div>
      </Card>
    </div>
  );
}