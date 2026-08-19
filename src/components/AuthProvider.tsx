"use client";

import { createContext, useContext, useSyncExternalStore, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { login as loginRequest, setToken } from "@/services/api";
import { AuthUser } from "@/types";

interface AuthContextValue {
  user: AuthUser | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// Hydration flag via useSyncExternalStore (no effect/setState needed): the
// server snapshot is always false, the client snapshot is always true, so
// React re-renders with the real value right after hydration completes.
function subscribeNoop() {
  return () => {};
}
function getClientTrue() {
  return true;
}
function getServerFalse() {
  return false;
}
function useIsClient() {
  return useSyncExternalStore(subscribeNoop, getClientTrue, getServerFalse);
}

function subscribeAuthChange(callback: () => void) {
  window.addEventListener("ltt-auth-change", callback);
  return () => window.removeEventListener("ltt-auth-change", callback);
}

function getUserSnapshot(): string | null {
  return localStorage.getItem("ltt_user");
}

function getServerUserSnapshot(): string | null {
  return null;
}

function notifyAuthChange() {
  window.dispatchEvent(new Event("ltt-auth-change"));
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const isClient = useIsClient();
  const rawUser = useSyncExternalStore(subscribeAuthChange, getUserSnapshot, getServerUserSnapshot);
  const user: AuthUser | null = isClient && rawUser ? JSON.parse(rawUser) : null;
  const isLoading = !isClient;
  const router = useRouter();

  async function login(username: string, password: string) {
    const data = await loginRequest(username, password);
    setToken(data.access_token);
    localStorage.setItem("ltt_user", JSON.stringify({ full_name: data.full_name, role: data.role }));
    notifyAuthChange();
  }

  function logout() {
    setToken(null);
    localStorage.removeItem("ltt_user");
    notifyAuthChange();
    router.push("/login");
  }

  return <AuthContext.Provider value={{ user, isLoading, login, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
