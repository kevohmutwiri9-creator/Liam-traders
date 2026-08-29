"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/lib/store";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { formatCurrency, getLevelName, getLevelColor } from "@/lib/utils";
import { userAPI, walletAPI } from "@/lib/api";

export default function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const updateUser = useAuthStore((state) => state.updateUser);
  const [walletStats, setWalletStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [copySuccess, setCopySuccess] = useState(false);

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
            <CardTitle className="text-2xl">{typeof user?.quality_score === 'number' ? user.quality_score.toFixed(1) : '0.0'}%</CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Referral Section */}
      <Card className="mb-8 bg-gradient-to-r from-primary-50 to-primary-100">
        <CardHeader>
          <CardTitle className="text-xl">Refer & Earn</CardTitle>
          <CardDescription>Share your referral link and earn up to KES 200 for each friend who signs up!</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Referral Code Display */}
            <div className="bg-white p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Your Referral Code</p>
              <p className="text-2xl font-bold text-primary-600">{user?.referral_code || 'Loading...'}</p>
            </div>
            
            <div className="flex items-center gap-2">
              <Input
                readOnly
                value={`${typeof window !== 'undefined' ? window.location.origin : ''}/?ref=${user?.referral_code || ''}`}
                className="flex-1"
              />
              <Button
                onClick={async () => {
                  const link = `${typeof window !== 'undefined' ? window.location.origin : ''}/?ref=${user?.referral_code || ''}`;
                  try {
                    await navigator.clipboard.writeText(link);
                    setCopySuccess(true);
                    setTimeout(() => setCopySuccess(false), 2000);
                  } catch (err) {
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = link;
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {
                      document.execCommand('copy');
                      setCopySuccess(true);
                      setTimeout(() => setCopySuccess(false), 2000);
                    } catch (e) {
                      console.error('Failed to copy:', e);
                      alert('Failed to copy link. Please select and copy manually.');
                    }
                    document.body.removeChild(textArea);
                  }
                }}
              >
                {copySuccess ? 'Copied!' : 'Copy Link'}
              </Button>
            </div>
            
            {/* Social Sharing Buttons */}
            <div className="flex gap-2 flex-wrap">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const link = `${typeof window !== 'undefined' ? window.location.origin : ''}/?ref=${user?.referral_code || ''}`;
                  const text = 'Join Liam Traders and start earning today!';
                  window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(link)}`, '_blank');
                }}
              >
                Share on Twitter
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const link = `${typeof window !== 'undefined' ? window.location.origin : ''}/?ref=${user?.referral_code || ''}`;
                  window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(link)}`, '_blank');
                }}
              >
                Share on Facebook
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const link = `${typeof window !== 'undefined' ? window.location.origin : ''}/?ref=${user?.referral_code || ''}`;
                  window.open(`https://wa.me/?text=${encodeURIComponent('Join Liam Traders and start earning today! ' + link)}`, '_blank');
                }}
              >
                Share on WhatsApp
              </Button>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded-lg">
                <p className="text-sm text-gray-600">Total Referrals</p>
                <p className="text-2xl font-bold">{user?.total_referrals || 0}</p>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <p className="text-sm text-gray-600">Referral Earnings</p>
                <p className="text-2xl font-bold">{formatCurrency(user?.referral_earnings || 0)}</p>
              </div>
            </div>
            
            <a href="/dashboard/referrals" className="text-primary-600 hover:underline text-sm">
              View detailed referral statistics →
            </a>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-4 gap-4">
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
            <a href="/dashboard/upgrade" className="p-4 border rounded-lg hover:bg-gray-50 transition">
              <h3 className="font-semibold">Upgrade Level</h3>
              <p className="text-sm text-gray-600">Pay to unlock higher levels</p>
            </a>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
