export default function RiskBadge({ risk }) {
  const color =
    risk > 70 ? "bg-red-600" : risk > 40 ? "bg-yellow-500" : "bg-green-600";

  return (
    <span className={`px-3 py-1 rounded text-white ${color}`}>
      {risk}%
    </span>
  );
}
