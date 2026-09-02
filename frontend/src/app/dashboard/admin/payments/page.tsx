"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { paymentsAPI } from "@/lib/api";

export default function AdminPaymentsPage() {
  const [pendingPayments, setPendingPayments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState<number | null>(null);
  const [notes, setNotes] = useState<{ [key: number]: string }>({});
  const [error, setError] = useState("");

  useEffect(() => {
    fetchPendingPayments();
  }, []);

  const fetchPendingPayments = async () => {
    try {
      setLoading(true);
      const response = await paymentsAPI.getPendingPayments();
      setPendingPayments(response.data.payments || []);
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError("You don't have permission to access this page");
      } else {
        console.error("Failed to fetch pending payments:", err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (paymentId: number) => {
    setProcessing(paymentId);
    try {
      await paymentsAPI.approvePayment(paymentId, { action: "approve" });
      // Remove from list
      setPendingPayments(pendingPayments.filter(p => p.id !== paymentId));
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to approve payment");
    } finally {
      setProcessing(null);
    }
  };

  const handleReject = async (paymentId: number) => {
    const paymentNotes = notes[paymentId] || "";
    setProcessing(paymentId);
    try {
      await paymentsAPI.approvePayment(paymentId, { 
        action: "reject",
        notes: paymentNotes
      });
      // Remove from list
      setPendingPayments(pendingPayments.filter(p => p.id !== paymentId));
      delete notes[paymentId];
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to reject payment");
    } finally {
      setProcessing(null);
    }
  };

  if (error === "You don't have permission to access this page") {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardContent className="py-8">
              <p className="text-center text-red-600">{error}</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Payment Approvals</h1>
          <p className="text-gray-600">Review and approve level upgrade payments</p>
        </div>

        {/* Payment Instructions Card */}
        <Card>
          <CardHeader>
            <CardTitle>Payment Verification Instructions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-1">
              <p><strong>PayBill Number:</strong> 247247</p>
              <p><strong>Account Number:</strong> 0763613955</p>
              <p><strong>Account Name:</strong> LIAM TRADERS</p>
            </div>
            <p className="text-sm text-gray-600">
              Verify payments by checking the transaction reference against your Equity bank records or M-Pesa statements.
            </p>
          </CardContent>
        </Card>

        {loading ? (
          <div className="flex items-center justify-center py-8">Loading...</div>
        ) : pendingPayments.length === 0 ? (
          <Card>
            <CardContent className="py-8">
              <p className="text-center text-gray-500">No pending payments to review</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {pendingPayments.map((payment) => (
              <Card key={payment.id}>
                <CardHeader>
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <CardTitle>
                        {payment.user.full_name}
                      </CardTitle>
                      <CardDescription>{payment.user.email}</CardDescription>
                    </div>
                    <Badge variant="default">Pending</Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 gap-4 min-[400px]:grid-cols-2 md:grid-cols-4">
                    <div>
                      <p className="text-sm text-gray-600">Current Level</p>
                      <p className="font-semibold">Level {payment.user.current_level}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Target Level</p>
                      <p className="font-semibold">{payment.target_level_name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Amount</p>
                      <p className="font-semibold text-primary-600">KSh {payment.amount}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Submitted</p>
                      <p className="font-semibold">
                        {new Date(payment.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-600 mb-1">Transaction Reference:</p>
                    <p className="font-mono font-semibold">{payment.transaction_reference}</p>
                  </div>

                  <div className="space-y-2">
                    <label className="block text-sm font-medium">
                      Admin Notes (for rejection)
                    </label>
                    <Input
                      value={notes[payment.id] || ""}
                      onChange={(e) => setNotes({ ...notes, [payment.id]: e.target.value })}
                      placeholder="Add notes if rejecting this payment..."
                    />
                  </div>

                  <div className="flex gap-2">
                    <Button
                      onClick={() => handleApprove(payment.id)}
                      disabled={processing === payment.id}
                      className="flex-1 bg-green-600 hover:bg-green-700"
                    >
                      {processing === payment.id ? "Processing..." : "Approve"}
                    </Button>
                    <Button
                      onClick={() => handleReject(payment.id)}
                      disabled={processing === payment.id}
                      variant="destructive"
                      className="flex-1"
                    >
                      {processing === payment.id ? "Processing..." : "Reject"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {error && error !== "You don't have permission to access this page" && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
