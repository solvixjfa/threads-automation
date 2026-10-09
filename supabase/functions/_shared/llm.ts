export async function generateAutoReply(
  promptTone: string,
  knowledgeBase: string,
  userText: string,
  authorUsername: string
): Promise<string> {
  const apiKey = Deno.env.get("GEMINI_API_KEY");
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY environment variable is missing");
  }

  const systemInstruction = `
Kamu adalah asisten balasan otomatis di Threads.
Tone: ${promptTone}
Knowledge Base: ${knowledgeBase}

Aturan Ketat:
1. Jangan pernah mengarang fakta di luar Knowledge Base.
2. Panjang jawaban maksimal 400 karakter (karakter Threads max 500).
3. Jangan pernah memberikan janji, kepastian harga, atau komitmen tanpa data di Knowledge Base.
4. Jangan sertakan tautan URL kecuali ada di Knowledge Base.
`;

  const userMessage = `Pengguna @${authorUsername} bertanya/berkomentar: "${userText}"\nBuatkan balasan yang pas:`;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [
        {
          role: "user",
          parts: [{ text: `${systemInstruction}\n\n${userMessage}` }]
        }
      ]
    })
  });

  const data = await response.json();
  if (data.error) {
    throw new Error(data.error.message || "Failed to generate LLM response");
  }

  const replyText = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || "";
  return replyText;
}
