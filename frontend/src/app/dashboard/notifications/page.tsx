"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { userAPI } from "@/lib/api";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await userAPI.getNotifications();
        setNotifications(res.data.results || res.data);
      } catch (error) {
        console.error("Failed to fetch notifications:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchNotifications();
  }, []);

  const markAsRead = async (id: number) => {
    try {
      await userAPI.markNotificationAsRead(id);
      setNotifications(notifications.map(n => 
        n.id === id ? { ...n, is_read: true } : n
      ));
    } catch (error) {
      console.error("Failed to mark notification as read:", error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await userAPI.markAllNotificationsAsRead();
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
    } catch (error) {
      console.error("Failed to mark all notifications as read:", error);
    }
  };

  if (loading) {
    return <div className="container py-8">Loading notifications...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Notifications</h1>
          <p className="text-gray-600 mt-2">Stay updated with your account activity</p>
        </div>
        {notifications.some(n => !n.is_read) && (
          <Button onClick={markAllAsRead}>Mark All as Read</Button>
        )}
      </div>

      {notifications.length === 0 ? (
        <Card>
          <CardContent className="py-12">
            <p className="text-gray-600 text-center">No notifications yet</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <Card 
              key={notification.id} 
              className={`transition-all ${!notification.is_read ? 'bg-blue-50 border-blue-200' : ''}`}
            >
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="font-semibold">{notification.title}</h3>
                      {!notification.is_read && (
                        <Badge variant="default" className="bg-blue-600">New</Badge>
                      )}
                    </div>
                    <p className="text-gray-600 mb-3">{notification.message}</p>
                    <p className="text-sm text-gray-400">
                      {new Date(notification.created_at).toLocaleString()}
                    </p>
                  </div>
                  {!notification.is_read && (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => markAsRead(notification.id)}
                    >
                      Mark as Read
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
