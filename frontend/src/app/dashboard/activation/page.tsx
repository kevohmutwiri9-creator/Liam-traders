"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { getCollectionResults, paymentsAPI, userAPI } from "@/lib/api";

const ACTIVATION_FEE = 200;

export default function ActivationPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [payments, setPayments] = useState<any[]>([]);
  const [reference, setReference] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const [profile, paymentHistory] = await Promise.all([
        userAPI.getProfile(),
        paymentsAPI.getMyPayments(),
      ]);
      setUser(profile.data);
      setPayments(getCollectionResults(paymentHistory.data));
      if (profile.data.is_activated) router.replace("/dashboard/upgrade");
    } catch (requestError) {
      setError("Could not load activation details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setMessage("");
    try {
      await paymentsAPI.submitLevelPayment({
        payment_type: "activation",
        target_level: 1,
        amount: ACTIVATION_FEE,
        transaction_reference: reference,
      });
      setReference("");
      setMessage("Activation payment submitted. An administrator will verify it shortly.");
      await load();
    } catch (requestError: any) {
      setError(requestError.response?.data?.amount?.[0] || requestError.response?.data?.detail || "Activation payment could not be submitted.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="container py-8">Loading activation...</div>;
  if (user?.is_activated) return null;

  return (
    <div className="container py-8">
      <div className="mx-auto max-w-3xl space-y-6">
        <div className="motion-rise rounded-2xl bg-gradient-to-r from-cyan-600 via-blue-700 to-indigo-800 p-8 text-white shadow-xl">
          <Badge className="mb-4 bg-white/20 text-white">Account activation</Badge>
          <h1 className="text-3xl font-bold">Activate your Liam Traders account</h1>
          <p className="mt-3 max-w-xl text-blue-100">Pay the one-time KES 200 activation fee. Once an admin verifies your payment, your account will unlock the platform opportunities.</p>
        </div>

        <Card className="motion-rise motion-glow">
          <CardHeader>
            <CardTitle>Activation payment</CardTitle>
            <CardDescription>Use the details below, then submit your transaction reference.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-xl bg-cyan-50 p-4"><p className="text-sm text-gray-500">Activation fee</p><p className="text-2xl font-bold">KES {ACTIVATION_FEE}</p></div>
              <div className="rounded-xl bg-blue-50 p-4"><p className="text-sm text-gray-500">PayBill</p><p className="text-2xl font-bold">247247</p></div>
              <div className="rounded-xl bg-indigo-50 p-4"><p className="text-sm text-gray-500">Account number</p><p className="text-2xl font-bold">0763613955</p></div>
              <div className="rounded-xl bg-emerald-50 p-4"><p className="text-sm text-gray-500">Account name</p><p className="text-xl font-bold">LIAM TRADERS</p></div>
            </div>
            <form onSubmit={submit} className="space-y-4">
              <Input value={reference} onChange={(event) => setReference(event.target.value)} placeholder="M-Pesa transaction reference" required />
              {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
              {message && <p className="rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">{message}</p>}
              <Button type="submit" disabled={submitting || !reference} className="w-full">{submitting ? "Submitting..." : "Submit KES 200 activation"}</Button>
            </form>
          </CardContent>
        </Card>

        {payments.length > 0 && (
          <Card>
            <CardHeader><CardTitle>Activation history</CardTitle></CardHeader>
            <CardContent className="space-y-3">
              {payments.filter((payment) => payment.payment_type === "activation").map((payment) => (
                <div key={payment.id} className="flex items-center justify-between rounded-lg border p-3">
                  <span className="font-mono text-sm">{payment.transaction_reference}</span>
                  <Badge>{payment.status}</Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
