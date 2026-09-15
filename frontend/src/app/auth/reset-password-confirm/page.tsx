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
    <div className="min-h-screen bg-gradient-to-br from-emerald-500 via-teal-600 to-cyan-700 flex items-center justify-center px-4 py-12 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-emerald-400 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-teal-400 rounded-full opacity-20 animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-cyan-500 rounded-full opacity-10 animate-pulse" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-20 left-20 w-32 h-32 bg-emerald-400 rounded-full opacity-15 animate-bounce" style={{ animationDuration: '3s' }}></div>
        <div className="absolute bottom-20 right-20 w-40 h-40 bg-teal-300 rounded-full opacity-15 animate-bounce" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
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