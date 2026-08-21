"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/store";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="text-xl font-bold text-primary-600">
              Liam Traders
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
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>{children}</main>
    </div>
  );
}
