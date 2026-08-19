"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { Sidebar } from "@/components/Sidebar";
import { LoadingState } from "@/components/States";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) router.replace("/login");
  }, [isLoading, user, router]);

  if (isLoading || !user) {
    return <LoadingState label="جارٍ التحقق من الجلسة..." />;
  }

  return (
    <div className="flex min-h-screen flex-1">
      <Sidebar />
      <main className="flex-1 overflow-x-hidden p-6">{children}</main>
    </div>
  );
}
