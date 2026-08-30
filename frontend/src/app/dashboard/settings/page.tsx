"use client";

import { useState, useEffect } from "react";
import { useAuthStore } from "@/lib/store";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { userAPI } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function SettingsPage() {
  const user = useAuthStore((state) => state.user);
  const updateUser = useAuthStore((state) => state.updateUser);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  const [profileData, setProfileData] = useState({
    full_name: '',
    email: '',
    phone_number: '',
    bio: '',
    location: '',
    date_of_birth: '',
  });

  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        full_name: user.full_name || '',
        email: user.email || '',
        phone_number: user.phone_number || '',
        bio: user.bio || '',
        location: user.location || '',
        date_of_birth: user.date_of_birth ? user.date_of_birth.split('T')[0] : '',
      });
      setLoading(false);
    }
  }, [user]);

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      const res = await userAPI.updateProfile(profileData);
      updateUser(res.data);
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
    } catch (error: any) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to update profile' });
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    if (passwordData.new_password !== passwordData.confirm_password) {
      setMessage({ type: 'error', text: 'Passwords do not match' });
      setSaving(false);
      return;
    }

    try {
      await userAPI.changePassword(passwordData);
      setMessage({ type: 'success', text: 'Password changed successfully!' });
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
    } catch (error: any) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to change password' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="container py-8">Loading settings...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-gray-600 mt-2">Manage your account settings and preferences</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${message.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
          {message.text}
        </div>
      )}

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="account">Account</TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <CardDescription>Update your personal information</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileUpdate} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="full_name">Full Name</Label>
                    <Input
                      id="full_name"
                      value={profileData.full_name}
                      onChange={(e) => setProfileData({ ...profileData, full_name: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={profileData.email}
                      onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                      required
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="phone_number">Phone Number</Label>
                  <Input
                    id="phone_number"
                    type="tel"
                    value={profileData.phone_number}
                    onChange={(e) => setProfileData({ ...profileData, phone_number: e.target.value })}
                  />
                </div>

                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    value={profileData.location}
                    onChange={(e) => setProfileData({ ...profileData, location: e.target.value })}
                  />
                </div>

                <div>
                  <Label htmlFor="date_of_birth">Date of Birth</Label>
                  <Input
                    id="date_of_birth"
                    type="date"
                    value={profileData.date_of_birth}
                    onChange={(e) => setProfileData({ ...profileData, date_of_birth: e.target.value })}
                  />
                </div>

                <div>
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea
                    id="bio"
                    value={profileData.bio}
                    onChange={(e) => setProfileData({ ...profileData, bio: e.target.value })}
                    rows={4}
                  />
                </div>

                <Button type="submit" disabled={saving}>
                  {saving ? 'Saving...' : 'Save Changes'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security">
          <Card>
            <CardHeader>
              <CardTitle>Change Password</CardTitle>
              <CardDescription>Update your password to keep your account secure</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handlePasswordChange} className="space-y-4">
                <div>
                  <Label htmlFor="current_password">Current Password</Label>
                  <Input
                    id="current_password"
                    type="password"
                    value={passwordData.current_password}
                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="new_password">New Password</Label>
                  <Input
                    id="new_password"
                    type="password"
                    value={passwordData.new_password}
                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="confirm_password">Confirm New Password</Label>
                  <Input
                    id="confirm_password"
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                    required
                  />
                </div>

                <Button type="submit" disabled={saving}>
                  {saving ? 'Changing Password...' : 'Change Password'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>Manage how you receive notifications</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Email Notifications</h3>
                    <p className="text-sm text-gray-600">Receive notifications via email</p>
                  </div>
                  <input type="checkbox" defaultChecked className="w-5 h-5" />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Task Updates</h3>
                    <p className="text-sm text-gray-600">Get notified about task status changes</p>
                  </div>
                  <input type="checkbox" defaultChecked className="w-5 h-5" />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Payment Notifications</h3>
                    <p className="text-sm text-gray-600">Receive payment confirmations</p>
                  </div>
                  <input type="checkbox" defaultChecked className="w-5 h-5" />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Level Updates</h3>
                    <p className="text-sm text-gray-600">Get notified when you level up</p>
                  </div>
                  <input type="checkbox" defaultChecked className="w-5 h-5" />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="account">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Account Information</CardTitle>
                <CardDescription>Your account details and statistics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Label>Current Level</Label>
                    <Badge className="mt-1">Level {user?.level}</Badge>
                  </div>
                  <div>
                    <Label>Tasks Completed</Label>
                    <p className="font-semibold">{user?.total_tasks_completed}</p>
                  </div>
                  <div>
                    <Label>Quality Score</Label>
                    <p className="font-semibold">{typeof user?.quality_score === 'number' ? user.quality_score.toFixed(1) : '0.0'}%</p>
                  </div>
                  <div>
                    <Label>Referral Code</Label>
                    <p className="font-semibold">{user?.referral_code}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Danger Zone</CardTitle>
                <CardDescription>Irreversible account actions</CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="destructive">Delete Account</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
