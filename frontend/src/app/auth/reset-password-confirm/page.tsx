"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import api from "@/lib/api";

export default function ResetPasswordConfirmPage() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setMessage("");
    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    const params = new URLSearchParams(window.location.search);
    const uid = params.get("uid");
    const token = params.get("token");
    if (!uid || !token) {
      setError("This reset link is incomplete or invalid.");
      return;
    }
    setLoading(true);
    try {
      await api.post("/auth/users/reset_password_confirm/", {
        uid,
        token,
        new_password: password,
        re_new_password: confirmPassword,
      });
      setMessage("Password reset successfully. Redirecting to login...");
      setTimeout(() => router.push("/auth/login"), 1200);
    } catch (err: any) {
      const data = err.response?.data;
      setError(data?.detail || data?.new_password?.[0] || "This reset link is invalid or expired.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-500 via-orange-600 to-red-700 flex items-center justify-center px-4 py-12 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.1)_0%,transparent_50%)] animate-pulse"></div>
        <div className="absolute top-0 right-0 w-full h-full bg-[radial-gradient(circle_at_70%_50%,rgba(255,255,255,0.08)_0%,transparent_50%)] animate-pulse" style={{ animationDelay: '1.5s' }}></div>
      </div>

      <Card className="w-full max-w-md relative z-10">
        <CardHeader>
          <div className="flex items-center justify-center gap-3 mb-4">
            <img src="/logo.png" alt="Liam Traders" className="w-12 h-12" />
            <CardTitle className="text-2xl">Reset Password</CardTitle>
          </div>
          <CardDescription>Choose a new password with at least 6 characters.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={submit} className="space-y-4">
            <Input type="password" placeholder="New password" value={password} minLength={6} onChange={(event) => setPassword(event.target.value)} required />
            <Input type="password" placeholder="Confirm new password" value={confirmPassword} minLength={6} onChange={(event) => setConfirmPassword(event.target.value)} required />
            {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
            {message && <p className="rounded-lg bg-green-50 p-3 text-sm text-green-700">{message}</p>}
            <Button type="submit" className="w-full" disabled={loading}>{loading ? "Resetting..." : "Reset password"}</Button>
            <p className="text-center text-sm text-gray-600"><Link href="/auth/login" className="text-primary-600 hover:underline">Back to login</Link></p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}