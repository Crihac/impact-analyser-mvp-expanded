import { useState } from "react";

export default function DiffInput({ onAnalyze, loading }) {
  const [diff, setDiff] = useState("");

  return (
    <div className="max-w-3xl mx-auto">
      <textarea
        className="w-full h-60 p-4 bg-gray-800 rounded-lg text-sm"
        placeholder="Paste your git diff here..."
        value={diff}
        onChange={(e) => setDiff(e.target.value)}
      />

      <button
        onClick={() => onAnalyze(diff)}
        disabled={loading}
        className="mt-4 px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-700"
      >
        {loading ? "Analyzing..." : "Analyze Impact"}
      </button>
    </div>
  );
}
