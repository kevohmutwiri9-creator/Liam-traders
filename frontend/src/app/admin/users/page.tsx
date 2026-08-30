"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import api from "@/lib/api";

export default function AdminUsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await api.get('/admin-dashboard/users/');
        setUsers(res.data);
      } catch (error) {
        console.error("Failed to fetch users:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const handleLevelChange = async (userId: number, newLevel: number) => {
    try {
      await api.patch(`/admin-dashboard/users/${userId}/`, { level: newLevel });
      setUsers(users.map(user => user.id === userId ? { ...user, level: newLevel } : user));
    } catch (error) {
      console.error("Failed to update user level:", error);
    }
  };

  const handleBanUser = async (userId: number) => {
    try {
      await api.post(`/admin-dashboard/users/${userId}/ban/`);
      setUsers(users.map(user => user.id === userId ? { ...user, is_active: false } : user));
    } catch (error) {
      console.error("Failed to ban user:", error);
    }
  };

  const handleUnbanUser = async (userId: number) => {
    try {
      await api.post(`/admin-dashboard/users/${userId}/unban/`);
      setUsers(users.map(user => user.id === userId ? { ...user, is_active: true } : user));
    } catch (error) {
      console.error("Failed to unban user:", error);
    }
  };

  const filteredUsers = users.filter(user =>
    user.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.full_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="container py-8">Loading users...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">User Management</h1>
        <p className="text-gray-600 mt-2">Manage user accounts and permissions</p>
      </div>

      <Card className="mb-6">
        <CardContent className="pt-6">
          <Input
            placeholder="Search users by email or name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </CardContent>
      </Card>

      <div className="space-y-4">
        {filteredUsers.map((user) => (
          <Card key={user.id}>
            <CardContent className="pt-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-gray-900">{user.full_name || 'No name'}</h3>
                    <Badge variant={user.is_staff ? 'default' : 'secondary'}>
                      {user.is_staff ? 'Admin' : 'User'}
                    </Badge>
                    <Badge variant={user.is_active ? 'default' : 'danger'}>
                      {user.is_active ? 'Active' : 'Banned'}
                    </Badge>
                  </div>
                  <p className="text-gray-600 mb-3">{user.email}</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Level:</span>
                      <span className="ml-2 font-medium">{user.level}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Tasks:</span>
                      <span className="ml-2 font-medium">{user.total_tasks_completed}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Quality:</span>
                      <span className="ml-2 font-medium">{typeof user.quality_score === 'number' ? user.quality_score.toFixed(1) : '0.0'}%</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Referrals:</span>
                      <span className="ml-2 font-medium">{user.total_referrals}</span>
                    </div>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <select
                    value={user.level}
                    onChange={(e) => handleLevelChange(user.id, parseInt(e.target.value))}
                    className="px-3 py-2 border rounded-md"
                  >
                    {[1, 2, 3, 4, 5].map(level => (
                      <option key={level} value={level}>Level {level}</option>
                    ))}
                  </select>
                  {user.is_active ? (
                    <Button variant="destructive" size="sm" onClick={() => handleBanUser(user.id)}>
                      Ban User
                    </Button>
                  ) : (
                    <Button variant="outline" size="sm" onClick={() => handleUnbanUser(user.id)}>
                      Unban User
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
