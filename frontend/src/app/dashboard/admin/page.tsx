"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import api from "@/lib/api";

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/admin-dashboard/stats/');
        setStats(res.data);
      } catch (error: any) {
        console.error("Failed to fetch stats:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    // Poll for stats updates every 10 seconds
    const interval = setInterval(fetchStats, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="container py-8">Loading admin dashboard...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <p className="text-gray-600 mt-2">Real-time platform statistics</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardDescription>Total Users</CardDescription>
            <CardTitle className="text-3xl">{stats?.total_users || 0}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-green-600">+{stats?.new_users_today || 0} today</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Total Earnings</CardDescription>
            <CardTitle className="text-3xl">${stats?.total_earnings?.toFixed(2) || '0.00'}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">Platform-wide</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Active Tasks</CardDescription>
            <CardTitle className="text-3xl">{stats?.active_tasks || 0}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">Open for applications</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Pending Withdrawals</CardDescription>
            <CardTitle className="text-3xl">{stats?.pending_withdrawals || 0}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-yellow-600">Awaiting approval</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest user registrations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats?.recent_users?.map((user: any) => (
                <div key={user.id} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{user.full_name || user.email}</p>
                    <p className="text-sm text-gray-600">{user.email}</p>
                  </div>
                  <span className="text-sm text-gray-500">
                    {new Date(user.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Level Distribution</CardTitle>
            <CardDescription>Users by level</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats?.level_distribution?.map((level: any) => (
                <div key={level.level} className="flex items-center justify-between">
                  <span className="font-medium">{level.level}</span>
                  <span className="text-sm text-gray-600">{level.count} users</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
