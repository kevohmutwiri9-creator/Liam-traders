"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { authAPI } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: "",
    full_name: "",
    password: "",
    re_password: "",
  });
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const fieldClass = (field: string) => fieldErrors[field] ? "border-red-500 bg-red-50 focus-visible:ring-red-500" : "";

  const updateField = (field: string, value: string) => {
    setFormData((current) => ({ ...current, [field]: value }));
    setFieldErrors((current) => ({ ...current, [field]: "" }));
    setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({});

    if (formData.password !== formData.re_password) {
      setError("Passwords do not match");
      setFieldErrors({ password: "Passwords do not match", re_password: "Passwords do not match" });
      return;
    }
    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters long");
      setFieldErrors({ password: "Use at least 6 characters" });
      return;
    }

    setLoading(true);

    try {
      await authAPI.register({
        email: formData.email,
        full_name: formData.full_name,
        password: formData.password,
        re_password: formData.re_password,
      });
      
      // Sign in first, then continue directly to activation.
      localStorage.setItem("activation_required", "true");
      router.push("/auth/login?registered=true&next=%2Fdashboard%2Factivation");
    } catch (err: any) {
      const data = err.response?.data || {};
      const nextErrors: Record<string, string> = {};
      Object.entries(data).forEach(([field, value]) => {
        if (field !== "detail") nextErrors[field] = Array.isArray(value) ? String(value[0]) : String(value);
      });
      setFieldErrors(nextErrors);
      setError(data.detail || Object.values(nextErrors)[0] || "Registration failed. Please correct the highlighted fields.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-500 via-cyan-600 to-blue-700 flex items-center justify-center py-12 px-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.1)_0%,transparent_50%)] animate-pulse"></div>
        <div className="absolute top-0 right-0 w-full h-full bg-[radial-gradient(circle_at_70%_50%,rgba(255,255,255,0.08)_0%,transparent_50%)] animate-pulse" style={{ animationDelay: '1.5s' }}></div>
      </div>

      <Card className="w-full max-w-md relative z-10">
        <CardHeader>
          <div className="flex items-center justify-center gap-3 mb-4">
            <img src="/logo.png" alt="Liam Traders" className="w-12 h-12" />
            <CardTitle className="text-2xl">Create Account</CardTitle>
          </div>
          <CardDescription>
            Join Liam Traders and start earning today
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
                {error}
              </div>
            )}
            
            <div className="space-y-2">
              <label htmlFor="full_name" className="text-sm font-medium">
                Full Name
              </label>
              <Input
                id="full_name"
                type="text"
                placeholder="John Doe"
                value={formData.full_name}
                onChange={(e) => updateField("full_name", e.target.value)}
                className={fieldClass("full_name")}
                required
              />
              {fieldErrors.full_name && <p className="text-sm text-red-600">{fieldErrors.full_name}</p>}
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={(e) => updateField("email", e.target.value)}
                className={fieldClass("email")}
                required
              />
              {fieldErrors.email && <p className="text-sm text-red-600">{fieldErrors.email}</p>}
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => updateField("password", e.target.value)}
                minLength={6}
                className={fieldClass("password")}
                required
              />
              <p className="text-xs text-gray-500">Use at least 6 characters.</p>
              {fieldErrors.password && <p className="text-sm text-red-600">{fieldErrors.password}</p>}
            </div>

            <div className="space-y-2">
              <label htmlFor="re_password" className="text-sm font-medium">
                Confirm Password
              </label>
              <Input
                id="re_password"
                type="password"
                placeholder="••••••••"
                value={formData.re_password}
                onChange={(e) => updateField("re_password", e.target.value)}
                className={fieldClass("re_password")}
                required
              />
              {fieldErrors.re_password && <p className="text-sm text-red-600">{fieldErrors.re_password}</p>}
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Creating account..." : "Create Account"}
            </Button>

            <p className="text-center text-sm text-gray-600">
              Already have an account?{" "}
              <Link href="/auth/login" className="text-primary-600 hover:underline">
                Sign in
              </Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
