"use client";

import { useState, useEffect } from "react";
import { useAuthStore } from "@/lib/store";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { formatCurrency } from "@/lib/utils";
import { walletAPI } from "@/lib/api";

export default function WalletPage() {
  const user = useAuthStore((state) => state.user);
  const [walletStats, setWalletStats] = useState<any>(null);
  const [transactions, setTransactions] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, transactionsRes] = await Promise.all([
          walletAPI.getStatistics(),
          walletAPI.getTransactions(),
        ]);
        setWalletStats(statsRes.data);
        setTransactions(transactionsRes.data);
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="container py-8">Loading wallet...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Wallet</h1>
        <p className="text-gray-600 mt-2">Manage your earnings and withdrawals</p>
      </div>

      {/* Balance Cards */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardDescription>Available Balance</CardDescription>
            <CardTitle className="text-3xl">{formatCurrency(walletStats?.available_balance || 0)}</CardTitle>
          </CardHeader>
          <CardContent>
            <Button className="w-full">Withdraw</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Pending Balance</CardDescription>
            <CardTitle className="text-3xl">{formatCurrency(walletStats?.pending_balance || 0)}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">Earnings awaiting approval</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Total Earnings</CardDescription>
            <CardTitle className="text-3xl">{formatCurrency(walletStats?.total_earnings || 0)}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">Lifetime earnings</p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Transactions */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Transactions</CardTitle>
          <CardDescription>Your latest earnings and withdrawals</CardDescription>
        </CardHeader>
        <CardContent>
          {transactions?.results && transactions.results.length > 0 ? (
            <div className="space-y-3">
              {transactions.results.map((transaction: any) => (
                <div key={transaction.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <p className="font-medium">{transaction.description}</p>
                    <p className="text-sm text-gray-600">{new Date(transaction.created_at).toLocaleDateString()}</p>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${transaction.transaction_type === 'earning' ? 'text-green-600' : 'text-red-600'}`}>
                      {transaction.transaction_type === 'earning' ? '+' : '-'}{formatCurrency(transaction.amount)}
                    </p>
                    <p className="text-sm text-gray-600 capitalize">{transaction.status}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">No transactions yet</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
