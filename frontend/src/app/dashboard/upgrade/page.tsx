"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getCollectionResults, userAPI, paymentsAPI } from "@/lib/api";

const LEVEL_PRICES = {
  1: 0,
  2: 500,
  3: 1000,
  4: 2000,
  5: 5000,
};

const LEVEL_NAMES = {
  1: "Starter",
  2: "Worker",
  3: "Professional",
  4: "Expert",
  5: "Academy/Master",
};

export default function LevelUpgradePage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [selectedLevel, setSelectedLevel] = useState<number>(2);
  const [transactionRef, setTransactionRef] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [myPayments, setMyPayments] = useState<any[]>([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [profileRes, paymentsRes] = await Promise.all([
        userAPI.getProfile(),
        paymentsAPI.getMyPayments(),
      ]);
      setUser(profileRes.data);
      setMyPayments(getCollectionResults(paymentsRes.data));
      
      // Set default to next level
      const nextLevel = profileRes.data.level + 1;
      if (nextLevel <= 5) {
        setSelectedLevel(nextLevel);
      }
    } catch (err) {
      console.error("Failed to fetch data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await paymentsAPI.submitLevelPayment({
        target_level: selectedLevel,
        amount: LEVEL_PRICES[selectedLevel as keyof typeof LEVEL_PRICES],
        transaction_reference: transactionRef,
      });
      
      setSuccess(true);
      setTransactionRef("");
      fetchData(); // Refresh payments
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to submit payment. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Level Upgrade</h1>
          <p className="text-gray-600">Upgrade your account to unlock more features and earning opportunities</p>
        </div>

        {/* Current Level Info */}
        <Card>
          <CardHeader>
            <CardTitle>Current Level</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <Badge variant="default" className="text-lg px-4 py-2">
                Level {user?.level} - {LEVEL_NAMES[user?.level as keyof typeof LEVEL_NAMES]}
              </Badge>
              <p className="text-gray-600">
                You can upgrade to Level {user?.level + 1} or higher
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Payment Instructions */}
        <Card>
          <CardHeader>
            <CardTitle>Payment Instructions</CardTitle>
            <CardDescription>
              Pay via Equity PayBill to upgrade your level
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-semibold">PayBill Number:</span>
                <span className="font-mono text-lg">247247</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-semibold">Account Number:</span>
                <span className="font-mono text-lg">0763613955</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-semibold">Account Name:</span>
                <span className="font-mono">LIAM TRADERS</span>
              </div>
              <div className="pt-2 border-t border-blue-200 text-sm text-gray-600">
                <p>Use reference: LIAM + your email (e.g., LIAMjohn@example.com)</p>
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="font-semibold">Level Pricing:</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {[2, 3, 4, 5].map((level) => (
                  <div
                    key={level}
                    className={`p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                      selectedLevel === level
                        ? "border-primary-500 bg-primary-50"
                        : "border-gray-200 hover:border-gray-300"
                    }`}
                    onClick={() => setSelectedLevel(level)}
                  >
                    <div className="font-semibold">Level {level}</div>
                    <div className="text-sm text-gray-600">{LEVEL_NAMES[level as keyof typeof LEVEL_NAMES]}</div>
                    <div className="font-bold text-primary-600">KSh {LEVEL_PRICES[level as keyof typeof LEVEL_PRICES]}</div>
                  </div>
                ))}
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Transaction Reference Number
                </label>
                <Input
                  value={transactionRef}
                  onChange={(e) => setTransactionRef(e.target.value)}
                  placeholder="Enter the transaction reference from your M-Pesa message"
                  required
                />
                <p className="text-sm text-gray-500 mt-1">
                  This is the reference number from your M-Pesa confirmation message
                </p>
              </div>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-sm">
                <p className="font-semibold text-yellow-800">Important:</p>
                <ul className="list-disc list-inside text-yellow-700 mt-1 space-y-1">
                  <li>Ensure you've paid the exact amount for your selected level</li>
                  <li>Use the correct PayBill number: 247247</li>
                  <li>Use account number: 0763613955</li>
                  <li>Submit the transaction reference immediately after payment</li>
                  <li>Your level will be upgraded after admin verification</li>
                </ul>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              {success && (
                <div className="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded">
                  Payment submitted successfully! Your level will be upgraded after admin verification.
                </div>
              )}

              <Button
                type="submit"
                className="w-full"
                disabled={submitting || !transactionRef}
              >
                {submitting ? "Submitting..." : `Submit Payment (KSh ${LEVEL_PRICES[selectedLevel as keyof typeof LEVEL_PRICES]})`}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* My Payments History */}
        <Card>
          <CardHeader>
            <CardTitle>My Payment History</CardTitle>
          </CardHeader>
          <CardContent>
            {myPayments.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No payment history</p>
            ) : (
              <div className="space-y-3">
                {myPayments.map((payment) => (
                  <div
                    key={payment.id}
                    className="border rounded-lg p-4 flex justify-between items-start"
                  >
                    <div>
                      <div className="font-semibold">
                        Level {payment.target_level} - {LEVEL_NAMES[payment.target_level as keyof typeof LEVEL_NAMES]}
                      </div>
                      <div className="text-sm text-gray-600">
                        Amount: KSh {payment.amount}
                      </div>
                      <div className="text-sm text-gray-600">
                        Reference: {payment.transaction_reference}
                      </div>
                      <div className="text-sm text-gray-500">
                        {new Date(payment.created_at).toLocaleString()}
                      </div>
                    </div>
                    <Badge
                      variant={
                        payment.status === "approved"
                          ? "success"
                          : payment.status === "rejected"
                          ? "danger"
                          : "default"
                      }
                    >
                      {payment.status}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
