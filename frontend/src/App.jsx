import { useState } from "react";
import DiffInput from "./components/DiffInput";
import ImpactResults from "./components/ImpactResults";
import { analyzeDiff } from "./api";

export default function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (diff) => {
    setLoading(true);
    const data = await analyzeDiff(diff);
    setResults(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 p-8 text-white">
      <h1 className="text-4xl font-bold mb-6 text-center">
        Impact Analyzer Dashboard
      </h1>

      <DiffInput onAnalyze={handleAnalyze} loading={loading} />

      {results && <ImpactResults data={results} />}
    </div>
  );
}
