export function KpiCard({
  label,
  value,
  sublabel,
  tone = "default",
}: {
  label: string;
  value: string;
  sublabel?: string;
  tone?: "default" | "danger" | "warning" | "success";
}) {
  const toneClasses: Record<string, string> = {
    default: "text-slate-900",
    danger: "text-red-600",
    warning: "text-amber-600",
    success: "text-emerald-600",
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className={`mt-1 text-2xl font-bold ${toneClasses[tone]}`}>{value}</p>
      {sublabel && <p className="mt-1 text-xs text-slate-400">{sublabel}</p>}
    </div>
  );
}
