"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

const NAV_ITEMS = [
  { href: "/overview", label: "نظرة عامة" },
  { href: "/customers", label: "مخاطر العملاء" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="flex w-64 shrink-0 flex-col border-l border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-5 py-5">
        <p className="text-base font-bold text-slate-900">LTT</p>
        <p className="text-xs text-slate-500">تنبؤ تسرب العملاء</p>
      </div>

      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map((item) => {
          const active = pathname?.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-lg px-3 py-2 text-sm font-medium transition ${
                active ? "bg-sky-50 text-sky-700" : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-slate-200 p-4">
        <p className="text-sm font-medium text-slate-800">{user?.full_name}</p>
        <p className="mb-3 text-xs text-slate-400">{user?.role}</p>
        <button
          onClick={logout}
          className="w-full rounded-lg border border-slate-200 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          تسجيل الخروج
        </button>
      </div>
    </aside>
  );
}
