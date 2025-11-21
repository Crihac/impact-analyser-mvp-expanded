import axios from "axios";

export async function analyzeDiff(diff) {
  try {
    const res = await axios.post("https://impact-analyser-backend.onrender.com/analyze", { diff });
    return res.data;
  } catch (err) {
    console.error(err);
    return { error: "API call failed" };
  }
}
