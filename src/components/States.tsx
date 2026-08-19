export function LoadingState({ label = "جارٍ التحميل..." }: { label?: string }) {
  return (
    <div className="flex h-40 items-center justify-center text-sm text-slate-400">
      <span className="animate-pulse">{label}</span>
    </div>
  );
}

export function ErrorState({ message = "حدث خطأ أثناء تحميل البيانات" }: { message?: string }) {
  return (
    <div className="flex h-40 items-center justify-center rounded-xl border border-red-200 bg-red-50 text-sm text-red-600">
      {message}
    </div>
  );
}

export function EmptyState({ message = "لا توجد بيانات لعرضها" }: { message?: string }) {
  return (
    <div className="flex h-40 items-center justify-center rounded-xl border border-dashed border-slate-300 text-sm text-slate-400">
      {message}
    </div>
  );
}
