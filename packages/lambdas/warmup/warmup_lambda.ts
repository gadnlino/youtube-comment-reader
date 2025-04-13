import axios from "axios";

export const handler = async () => {
  try {
    const url = process.env.SENTIMENT_ANALYSIS_API_URL!;
    const apiKey = process.env.SENTIMENT_ANALYSIS_API_KEY!;

    await axios.post(url, {
      comments: ["ping"]
    }, {
      headers: {
        "x-api-key": apiKey,
        "Content-Type": "application/json"
      }
    });

    console.log("Sentiment function pinged with success.");
  } catch (err) {
    console.error("Failed to ping sentiment function", err);
  }
};
