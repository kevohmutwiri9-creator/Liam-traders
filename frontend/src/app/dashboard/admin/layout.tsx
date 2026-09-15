"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/lib/store";
import { userAPI } from "@/lib/api";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isInitialized = useAuthStore((state) => state.isInitialized);
  const user = useAuthStore((state) => state.user);
  const refreshUser = useAuthStore((state) => state.refreshUser);
  const [unreadCount, setUnreadCount] = useState(0);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activationChecked, setActivationChecked] = useState(false);

  useEffect(() => {
    let active = true;
    if (!isAuthenticated) return undefined;

    refreshUser().finally(() => {
      if (active) setActivationChecked(true);
    });

    return () => {
      active = false;
    };
  }, [isAuthenticated, refreshUser]);

  useEffect(() => {
    if (isInitialized && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, isInitialized, router]);

  useEffect(() => {
    if (!activationChecked || !isAuthenticated || !user || !user.is_staff) {
      return;
    }

    if (!user.is_staff) {
      router.replace("/dashboard");
    }
  }, [activationChecked, isAuthenticated, router, user]);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await userAPI.getNotifications();
        const notifications = res.data.results || res.data;
        setUnreadCount(notifications.filter((n: any) => !n.is_read).length);
      } catch (error) {
        console.error("Failed to fetch notifications:", error);
      }
    };

    if (isAuthenticated) {
      fetchNotifications();
      const interval = setInterval(fetchNotifications, 30000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  if (!isInitialized || !isAuthenticated || !activationChecked) {
    return null;
  }

  if (!user?.is_staff) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900 relative overflow-hidden">
      {/* Animated Background Elements - Dark Theme */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-red-500 rounded-full opacity-10 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-orange-500 rounded-full opacity-10 animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-amber-500 rounded-full opacity-5 animate-pulse" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-20 left-20 w-32 h-32 bg-red-600 rounded-full opacity-8 animate-bounce" style={{ animationDuration: '3s' }}></div>
        <div className="absolute bottom-20 right-20 w-40 h-40 bg-orange-600 rounded-full opacity-8 animate-bounce" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
      </div>

      {/* Header */}
      <header className="bg-gray-800/90 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-20">
        <div className="container">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard/admin" className="flex items-center gap-2 min-w-0">
              <img src="/logo.png" alt="Liam Traders" className="w-8 h-8 shrink-0" />
              <span className="text-lg font-bold text-red-500 truncate sm:text-xl">Admin Panel</span>
            </Link>

            <button
              type="button"
              className="inline-flex items-center justify-center rounded-md p-2 text-gray-300 md:hidden"
              onClick={() => setMobileMenuOpen((open) => !open)}
              aria-label="Toggle navigation"
            >
              <span className="text-xl">☰</span>
            </button>

            <nav className={`${mobileMenuOpen ? 'flex' : 'hidden'} absolute left-4 right-4 top-16 z-30 flex-col gap-2 rounded-lg border border-gray-700 bg-gray-800 p-4 shadow-lg md:static md:flex md:flex-row md:items-center md:gap-6 md:p-0 md:shadow-none md:border-0`}>
              <Link href="/dashboard/admin" className="text-gray-300 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
                Dashboard
              </Link>
              <Link href="/dashboard/admin/users" className="text-gray-300 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
                Users
              </Link>
              <Link href="/dashboard/admin/payments" className="text-gray-300 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
                Payments
              </Link>
              <Link href="/dashboard/admin/logs" className="text-gray-300 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
                Logs
              </Link>
              <Link href="/dashboard" className="text-gray-300 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
                Back to App
              </Link>
              <button
                onClick={() => {
                  useAuthStore.getState().logout();
                  router.push("/auth/login");
                }}
                className="text-left text-red-400 hover:text-red-300"
              >
                Logout
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-3 pb-8 pt-4 sm:px-4 md:px-6 relative z-10">{children}</main>
    </div>
  );
}
