"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/lib/store";
import { userAPI } from "@/lib/api";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const user = useAuthStore((state) => state.user);
  const [unreadCount, setUnreadCount] = useState(0);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await userAPI.getNotifications();
        const notifications = res.data.results || res.data;
        setUnreadCount(notifications.filter((n: any) => !n.is_read).length);
      } catch (error) {
        console.error("Failed to fetch notifications:", error);
        // Don't logout on notification fetch failure
      }
    };

    if (isAuthenticated) {
      fetchNotifications();
      // Poll for notifications every 30 seconds
      const interval = setInterval(fetchNotifications, 30000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-20">
        <div className="container">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="flex items-center gap-2 min-w-0">
              <img src="/logo.png" alt="Liam Traders" className="w-8 h-8 shrink-0" />
              <span className="text-lg font-bold text-primary-600 truncate sm:text-xl">Liam Traders</span>
            </Link>

            <button
              type="button"
              className="inline-flex items-center justify-center rounded-md p-2 text-gray-600 md:hidden"
              onClick={() => setMobileMenuOpen((open) => !open)}
              aria-label="Toggle navigation"
            >
              <span className="text-xl">☰</span>
            </button>

            <nav className={`${mobileMenuOpen ? 'flex' : 'hidden'} absolute left-4 right-4 top-16 z-30 flex-col gap-2 rounded-lg border bg-white p-4 shadow-lg md:static md:flex md:flex-row md:items-center md:gap-6 md:p-0 md:shadow-none md:border-0`}>
              <Link href="/dashboard" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Dashboard
              </Link>
              <Link href="/dashboard/tasks" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Tasks
              </Link>
              <Link href="/dashboard/surveys" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Surveys
              </Link>
              <Link href="/dashboard/courses" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Courses
              </Link>
              <Link href="/dashboard/wallet" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Wallet
              </Link>
              <Link href="/dashboard/notifications" className="relative text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Notifications
                {unreadCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </Link>
              <Link href="/dashboard/settings" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                Settings
              </Link>
              {user?.is_staff && (
                <>
                  <Link href="/dashboard/admin" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                    Admin
                  </Link>
                  <Link href="/dashboard/admin/users" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                    Users
                  </Link>
                  <Link href="/dashboard/admin/logs" className="text-gray-600 hover:text-gray-900" onClick={() => setMobileMenuOpen(false)}>
                    Logs
                  </Link>
                </>
              )}
              <button
                onClick={() => {
                  useAuthStore.getState().logout();
                  router.push("/auth/login");
                }}
                className="text-left text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-3 pb-8 pt-4 sm:px-4 md:px-6">{children}</main>
    </div>
  );
}
