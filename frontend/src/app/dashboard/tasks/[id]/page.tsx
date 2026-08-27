"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { formatCurrency } from "@/lib/utils";
import { tasksAPI } from "@/lib/api";

export default function TaskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const taskId = parseInt(params.id as string);
  
  const [task, setTask] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  
  const [coverLetter, setCoverLetter] = useState("");
  const [proposedAmount, setProposedAmount] = useState("");

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const res = await tasksAPI.getTask(taskId);
        setTask(res.data);
        setProposedAmount(res.data.budget.toString());
      } catch (error) {
        console.error("Failed to fetch task:", error);
        router.push("/dashboard/tasks");
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId, router]);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      await tasksAPI.applyToTask(taskId, {
        cover_letter: coverLetter,
        proposed_amount: parseFloat(proposedAmount),
      });
      router.push("/dashboard/tasks?success=true");
    } catch (error) {
      console.error("Failed to apply to task:", error);
      alert("Failed to apply. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-600';
      case 'high': return 'bg-orange-600';
      case 'medium': return 'bg-yellow-600';
      case 'low': return 'bg-green-600';
      default: return 'bg-gray-600';
    }
  };

  if (loading) {
    return <div className="container py-8">Loading task...</div>;
  }

  return (
    <div className="container py-8 max-w-4xl">
      <Button variant="ghost" onClick={() => router.push("/dashboard/tasks")} className="mb-4">
        ← Back to Tasks
      </Button>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <span className={`px-3 py-1 rounded-full text-white text-sm ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
                <span className="px-3 py-1 rounded-full bg-gray-200 text-sm">
                  {task.task_type}
                </span>
              </div>
              <CardTitle className="text-2xl mt-4">{task.title}</CardTitle>
              <CardDescription className="mt-2">{task.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold mb-2">Requirements</h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-600">
                    <li>Minimum Level: {task.min_level_required}</li>
                    {task.required_specializations && task.required_specializations.length > 0 && (
                      <li>Specializations: {task.required_specializations.join(", ")}</li>
                    )}
                    {task.required_skills && task.required_skills.length > 0 && (
                      <li>Skills: {task.required_skills.join(", ")}</li>
                    )}
                  </ul>
                </div>
                
                <div>
                  <h3 className="font-semibold mb-2">Task Details</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Budget:</span>
                      <span className="font-bold text-green-600 ml-2">{formatCurrency(task.budget)}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Duration:</span>
                      <span className="ml-2">{task.estimated_time_hours} hours</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Deadline:</span>
                      <span className="ml-2">{new Date(task.deadline).toLocaleDateString()}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Applications:</span>
                      <span className="ml-2">{task.total_applications}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>Apply for this Task</CardTitle>
              <CardDescription>Submit your application</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="cover-letter">Cover Letter *</Label>
                  <Textarea
                    id="cover-letter"
                    placeholder="Explain why you're the best fit for this task..."
                    value={coverLetter}
                    onChange={(e) => setCoverLetter(e.target.value)}
                    required
                    rows={6}
                  />
                </div>
                
                <div>
                  <Label htmlFor="proposed-amount">Proposed Amount (KES)</Label>
                  <Input
                    id="proposed-amount"
                    type="number"
                    value={proposedAmount}
                    onChange={(e) => setProposedAmount(e.target.value)}
                    placeholder="Your proposed amount"
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    Task budget: {formatCurrency(task.budget)}
                  </p>
                </div>
                
                <Button 
                  onClick={handleSubmit} 
                  disabled={submitting || !coverLetter}
                  className="w-full"
                >
                  {submitting ? "Submitting..." : "Submit Application"}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
