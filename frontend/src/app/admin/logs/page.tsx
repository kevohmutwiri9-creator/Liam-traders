"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import api from "@/lib/api";

export default function AdminLogsPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await api.get('/admin/logs/');
        setLogs(res.data);
      } catch (error: any) {
        console.error("Failed to fetch logs:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
    // Poll for new logs every 10 seconds
    const interval = setInterval(fetchLogs, 10000);
    return () => clearInterval(interval);
  }, []);

  const filteredLogs = logs.filter(log => 
    log.message.toLowerCase().includes(filter.toLowerCase()) ||
    log.level.toLowerCase().includes(filter.toLowerCase())
  );

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'INFO': return 'bg-blue-600';
      case 'WARNING': return 'bg-yellow-600';
      case 'ERROR': return 'bg-red-600';
      case 'DEBUG': return 'bg-gray-600';
      default: return 'bg-green-600';
    }
  };

  if (loading) {
    return <div className="container py-8">Loading logs...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">System Logs</h1>
        <p className="text-gray-600 mt-2">View all system activity and API calls</p>
      </div>

      <div className="mb-6">
        <Input
          placeholder="Filter logs..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="max-w-md"
        />
      </div>

      <div className="space-y-4">
        {filteredLogs.length === 0 ? (
          <Card>
            <CardContent className="py-12">
              <p className="text-gray-600 text-center">No logs available</p>
            </CardContent>
          </Card>
        ) : (
          filteredLogs.map((log, index) => (
            <Card key={index}>
              <CardContent className="pt-6">
                <div className="flex items-start gap-4">
                  <Badge className={getLevelColor(log.level)}>{log.level}</Badge>
                  <div className="flex-1">
                    <p className="font-mono text-sm">{log.message}</p>
                    <p className="text-gray-500 text-xs mt-1">
                      {new Date(log.timestamp).toLocaleString()} - {log.source}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
