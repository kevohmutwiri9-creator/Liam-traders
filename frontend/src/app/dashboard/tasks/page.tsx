"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/utils";
import { tasksAPI } from "@/lib/api";

export default function TasksPage() {
  const [tasks, setTasks] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await tasksAPI.getTasks({ status: 'open' });
        console.log('Tasks API response:', res.data);
        setTasks(res.data);
      } catch (error: any) {
        console.error("Failed to fetch tasks:", error);
        console.error("Error response:", error.response?.data);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  if (loading) {
    return <div className="container py-8">Loading tasks...</div>;
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-600';
      case 'high': return 'bg-orange-600';
      case 'medium': return 'bg-yellow-600';
      case 'low': return 'bg-green-600';
      default: return 'bg-gray-600';
    }
  };

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <p className="text-gray-600 mt-2">Browse and apply for available tasks</p>
      </div>

      {tasks?.results && tasks.results.length > 0 ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tasks.results.map((task: any) => (
            <Card key={task.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <Badge className={getPriorityColor(task.priority)}>{task.priority}</Badge>
                  <Badge variant="outline">{task.task_type}</Badge>
                </div>
                <CardTitle className="text-lg">{task.title}</CardTitle>
                <CardDescription className="line-clamp-2">{task.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Budget:</span>
                    <span className="font-bold text-green-600">{formatCurrency(task.budget)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Duration:</span>
                    <span>{task.estimated_time_hours} hrs</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Deadline:</span>
                    <span>{new Date(task.deadline).toLocaleDateString()}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Level Required:</span>
                    <span>{task.min_level_required}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Applications:</span>
                    <span>{task.total_applications}</span>
                  </div>
                  <Button className="w-full mt-4" onClick={() => window.location.href = `/dashboard/tasks/${task.id}`}>Apply Now</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12">
            <p className="text-gray-600 text-center">No tasks available at the moment. Check back later!</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
