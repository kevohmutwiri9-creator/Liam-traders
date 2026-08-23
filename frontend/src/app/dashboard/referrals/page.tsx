"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/lib/store";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/utils";
import { userAPI } from "@/lib/api";

export default function ReferralsPage() {
  const user = useAuthStore((state) => state.user);
  const [referralStats, setReferralStats] = useState<any>(null);
  const [referralHistory, setReferralHistory] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, historyRes, leaderboardRes] = await Promise.all([
          userAPI.getReferralStats(),
          userAPI.getReferralHistory(),
          userAPI.getReferralLeaderboard(10),
        ]);
        setReferralStats(statsRes.data);
        setReferralHistory(historyRes.data);
        setLeaderboard(leaderboardRes.data);
      } catch (error) {
        console.error("Failed to fetch referral data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="container py-8">Loading referral statistics...</div>;
  }

  const referralLink = `${typeof window !== 'undefined' ? window.location.origin : ''}/?ref=${user?.referral_code || ''}`;

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Referral Program</h1>
        <p className="text-gray-600 mt-2">Track your referrals and earnings</p>
      </div>

      {/* Referral Link */}
      <Card className="mb-6 bg-gradient-to-r from-primary-50 to-primary-100">
        <CardHeader>
          <CardTitle>Your Referral Link</CardTitle>
          <CardDescription>Share this link to earn referral bonuses</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Input readOnly value={referralLink} className="flex-1" />
              <Button
                onClick={() => {
                  navigator.clipboard.writeText(referralLink);
                }}
              >
                Copy Link
              </Button>
            </div>
            
            {/* Social Sharing */}
            <div className="flex gap-2 flex-wrap">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const text = 'Join Liam Traders and start earning today!';
                  window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(referralLink)}`, '_blank');
                }}
              >
                Share on Twitter
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(referralLink)}`, '_blank');
                }}
              >
                Share on Facebook
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  window.open(`https://wa.me/?text=${encodeURIComponent('Join Liam Traders and start earning today! ' + referralLink)}`, '_blank');
                }}
              >
                Share on WhatsApp
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardDescription>Total Referrals</CardDescription>
            <CardTitle className="text-2xl">{referralStats?.total_referrals || 0}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Referral Earnings</CardDescription>
            <CardTitle className="text-2xl">{formatCurrency(referralStats?.referral_earnings || 0)}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Current Bonus Tier</CardDescription>
            <CardTitle className="text-2xl">{formatCurrency(referralStats?.current_bonus_tier || 50)}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Next Tier</CardDescription>
            <CardTitle className="text-2xl">
              {referralStats?.next_tier ? `${referralStats.next_tier.referrals_needed} more` : 'Max tier'}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Bonus Tiers */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Bonus Tiers</CardTitle>
          <CardDescription>Earn more as you refer more people</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {Object.entries(referralStats?.bonus_tiers || {}).map(([threshold, bonus]: [string, any]) => (
              <div
                key={threshold}
                className={`flex items-center justify-between p-3 rounded-lg ${
                  (referralStats?.total_referrals || 0) >= parseInt(threshold)
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-gray-50 border border-gray-200'
                }`}
              >
                <div>
                  <span className="font-medium">{threshold}+ referrals</span>
                  <span className="text-sm text-gray-600 ml-2">
                    {parseInt(threshold) === 1 ? '(Base tier)' : ''}
                  </span>
                </div>
                <Badge className={referralStats?.current_bonus_tier === bonus ? 'bg-green-600' : 'bg-gray-600'}>
                  {formatCurrency(bonus)}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Referral History */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Referral History</CardTitle>
          <CardDescription>People who signed up with your referral code</CardDescription>
        </CardHeader>
        <CardContent>
          {referralHistory?.referrals && referralHistory.referrals.length > 0 ? (
            <div className="space-y-3">
              {referralHistory.referrals.map((referral: any) => (
                <div key={referral.user_id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <p className="font-medium">{referral.full_name}</p>
                    <p className="text-sm text-gray-600">{referral.email}</p>
                  </div>
                  <div className="text-right">
                    <Badge>{referral.level_name}</Badge>
                    <p className="text-sm text-gray-600 mt-1">
                      {new Date(referral.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">No referrals yet. Start sharing your link!</p>
          )}
        </CardContent>
      </Card>

      {/* Leaderboard */}
      <Card>
        <CardHeader>
          <CardTitle>Top Referrers</CardTitle>
          <CardDescription>See who's earning the most from referrals</CardDescription>
        </CardHeader>
        <CardContent>
          {leaderboard?.leaderboard && leaderboard.leaderboard.length > 0 ? (
            <div className="space-y-3">
              {leaderboard.leaderboard.map((entry: any) => (
                <div
                  key={entry.rank}
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    entry.rank <= 3 ? 'bg-yellow-50 border border-yellow-200' : 'bg-gray-50 border border-gray-200'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                      entry.rank === 1 ? 'bg-yellow-400 text-white' :
                      entry.rank === 2 ? 'bg-gray-400 text-white' :
                      entry.rank === 3 ? 'bg-orange-400 text-white' :
                      'bg-gray-200 text-gray-600'
                    }`}>
                      {entry.rank}
                    </div>
                    <div>
                      <p className="font-medium">{entry.full_name}</p>
                      <p className="text-sm text-gray-600">{entry.email}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold">{formatCurrency(entry.referral_earnings)}</p>
                    <p className="text-sm text-gray-600">{entry.total_referrals} referrals</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">No referrers yet. Be the first!</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
