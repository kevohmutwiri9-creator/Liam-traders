"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/lib/store";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, getLevelName, getLevelColor } from "@/lib/utils";
import { userAPI, walletAPI } from "@/lib/api";

export default function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const updateUser = useAuthStore((state) => state.updateUser);
  const [walletStats, setWalletStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileRes, walletRes] = await Promise.all([
          userAPI.getProfile(),
          walletAPI.getStatistics(),
        ]);
        updateUser(profileRes.data);
        setWalletStats(walletRes.data);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [updateUser]);

  if (loading) {
    return <div className="container py-8">Loading...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Welcome back, {user?.full_name}!</h1>
        <p className="text-gray-600 mt-2">Here's what's happening with your account</p>
      </div>

      {/* Level Badge */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold">Current Level</h3>
              <div className="flex items-center gap-3 mt-2">
                <Badge className={`${getLevelColor(user?.level || 1)} text-white px-4 py-2`}>
                  Level {user?.level} - {getLevelName(user?.level || 1)}
                </Badge>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Tasks Completed</p>
              <p className="text-2xl font-bold">{user?.total_tasks_completed}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardDescription>Available Balance</CardDescription>
            <CardTitle className="text-2xl">
              {formatCurrency(walletStats?.available_balance || 0)}
            </CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Pending Balance</CardDescription>
            <CardTitle className="text-2xl">
              {formatCurrency(walletStats?.pending_balance || 0)}
            </CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Total Earnings</CardDescription>
            <CardTitle className="text-2xl">
              {formatCurrency(walletStats?.total_earnings || 0)}
            </CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Quality Score</CardDescription>
            <CardTitle className="text-2xl">{user?.quality_score.toFixed(1)}%</CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-4">
            <a href="/dashboard/tasks" className="p-4 border rounded-lg hover:bg-gray-50 transition">
              <h3 className="font-semibold">Browse Tasks</h3>
              <p className="text-sm text-gray-600">Find work that matches your skills</p>
            </a>
            <a href="/dashboard/surveys" className="p-4 border rounded-lg hover:bg-gray-50 transition">
              <h3 className="font-semibold">Take Surveys</h3>
              <p className="text-sm text-gray-600">Complete surveys for quick earnings</p>
            </a>
            <a href="/dashboard/courses" className="p-4 border rounded-lg hover:bg-gray-50 transition">
              <h3 className="font-semibold">Learn Skills</h3>
              <p className="text-sm text-gray-600">Improve your skills to earn more</p>
            </a>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
