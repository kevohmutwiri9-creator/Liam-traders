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
      <header className="bg-white border-b">
        <div className="container">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="flex items-center gap-2">
              <img src="/logo.png" alt="Liam Traders" className="w-8 h-8" />
              <span className="text-xl font-bold text-primary-600">Liam Traders</span>
            </Link>
            <nav className="flex items-center gap-6">
              <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
                Dashboard
              </Link>
              <Link href="/dashboard/tasks" className="text-gray-600 hover:text-gray-900">
                Tasks
              </Link>
              <Link href="/dashboard/surveys" className="text-gray-600 hover:text-gray-900">
                Surveys
              </Link>
              <Link href="/dashboard/courses" className="text-gray-600 hover:text-gray-900">
                Courses
              </Link>
              <Link href="/dashboard/wallet" className="text-gray-600 hover:text-gray-900">
                Wallet
              </Link>
              <Link href="/dashboard/notifications" className="text-gray-600 hover:text-gray-900 relative">
                Notifications
                {unreadCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </Link>
              <Link href="/dashboard/settings" className="text-gray-600 hover:text-gray-900">
                Settings
              </Link>
              {user?.is_staff && (
                <Link href="/admin/users" className="text-gray-600 hover:text-gray-900">
                  Admin
                </Link>
              )}
              <button
                onClick={() => {
                  useAuthStore.getState().logout();
                  router.push("/auth/login");
                }}
                className="text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>{children}</main>
    </div>
  );
}
