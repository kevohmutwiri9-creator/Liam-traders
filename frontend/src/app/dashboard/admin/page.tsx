"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [pendingPayments, setPendingPayments] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        console.log('Fetching admin stats...');
        const [statsRes, pendingRes] = await Promise.all([
          api.get('/admin-dashboard/stats/'),
          api.get('/users/payments/pending/'),
        ]);
        console.log('Admin stats response:', statsRes.data);
        setStats(statsRes.data);

        const pendingCount = typeof pendingRes.data?.total === 'number'
          ? pendingRes.data.total
          : Array.isArray(pendingRes.data?.payments)
            ? pendingRes.data.payments.length
            : 0;
        setPendingPayments(pendingCount);
      } catch (error: any) {
        console.error("Failed to fetch stats:", error);
        console.error("Error response:", error.response?.data);
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
    <div className="container py-6 sm:py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <p className="text-gray-600 mt-2">Real-time platform statistics</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4 mb-8">
        <Card className="border-yellow-200 bg-yellow-50/40">
          <CardHeader>
            <CardDescription>Pending Activation Verifications</CardDescription>
            <CardTitle className="text-3xl">{pendingPayments}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm text-yellow-700">Level upgrade payments waiting for admin review</p>
              <Link href="/dashboard/admin/payments">
                <Button variant="outline" size="sm">Review</Button>
              </Link>
            </div>
          </CardContent>
        </Card>

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
            <CardTitle className="text-3xl">${Number(stats?.total_earnings || 0).toFixed(2)}</CardTitle>
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
            <CardDescription>Surveys</CardDescription>
            <CardTitle className="text-3xl">{stats?.total_surveys || 0}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">{stats?.active_surveys || 0} active</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Courses</CardDescription>
            <CardTitle className="text-3xl">{stats?.total_courses || 0}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">{stats?.total_enrollments || 0} enrollments</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Task Submissions</CardDescription>
            <CardTitle className="text-3xl">{stats?.total_submissions || 0}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">{stats?.completed_tasks || 0} tasks completed</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Monthly Revenue</CardDescription>
            <CardTitle className="text-3xl">${Number(stats?.monthly_revenue || 0).toFixed(2)}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">Last 30 days</p>
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

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
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
