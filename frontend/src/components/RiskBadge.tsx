const STYLES: Record<string, string> = {
  Critical: "bg-red-100 text-red-700 ring-1 ring-red-200",
  High: "bg-orange-100 text-orange-700 ring-1 ring-orange-200",
  Medium: "bg-amber-100 text-amber-700 ring-1 ring-amber-200",
  Low: "bg-emerald-100 text-emerald-700 ring-1 ring-emerald-200",
  Unscored: "bg-slate-100 text-slate-500 ring-1 ring-slate-200",
};

const LABELS_AR: Record<string, string> = {
  Critical: "حرج",
  High: "مرتفع",
  Medium: "متوسط",
  Low: "منخفض",
  Unscored: "غير مقيّم",
};

export function RiskBadge({ level }: { level: string }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold ${STYLES[level] ?? STYLES.Unscored}`}>
      {LABELS_AR[level] ?? level}
    </span>
  );
}
