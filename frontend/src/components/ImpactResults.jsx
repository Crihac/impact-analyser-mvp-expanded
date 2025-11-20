import RiskBadge from "./RiskBadge";

export default function ImpactResults({ data }) {
  return (
    <div className="mt-10 bg-gray-800 rounded-lg p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>

      <p className="mb-4 text-gray-300">
        Overall Risk: <RiskBadge risk={data.overall_risk} />
      </p>

      <h3 className="text-xl font-semibold mb-2">Impacted Modules:</h3>
      <ul className="space-y-3">
        {data.impacted_modules.map((m, idx) => (
          <li
            key={idx}
            className="p-3 rounded bg-gray-700 flex justify-between"
          >
            <span>{m.module}</span>
            <RiskBadge risk={m.risk} />
          </li>
        ))}
      </ul>
    </div>
  );
}
