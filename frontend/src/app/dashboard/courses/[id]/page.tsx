"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { coursesAPI } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function CourseDetailPage() {
  const params = useParams();
  const router = useRouter();
  const courseId = Number(params.id);
  const [course, setCourse] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    coursesAPI.getCourse(courseId)
      .then((response) => setCourse(response.data))
      .catch(() => router.push("/dashboard/courses"))
      .finally(() => setLoading(false));
  }, [courseId, router]);

  const handleEnroll = async () => {
    setEnrolling(true);
    setMessage("");
    try {
      await coursesAPI.enrollInCourse(courseId);
      setMessage("Enrollment successful. Your course is ready to start.");
    } catch (error: any) {
      setMessage(error.response?.data?.detail || "Unable to enroll in this course.");
    } finally {
      setEnrolling(false);
    }
  };

  if (loading) return <div className="container py-8">Loading course...</div>;
  if (!course) return null;

  return (
    <div className="container py-8">
      <Button variant="ghost" onClick={() => router.push("/dashboard/courses")} className="mb-6">
        Back to courses
      </Button>
      <Card className="mx-auto max-w-4xl overflow-hidden border-0 shadow-xl">
        <div className="h-3 bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-700" />
        <CardHeader className="space-y-4 p-8">
          <div className="flex flex-wrap gap-2">
            <Badge>{course.category}</Badge>
            <Badge variant="outline">{course.difficulty}</Badge>
          </div>
          <CardTitle className="text-3xl">{course.title}</CardTitle>
          <CardDescription className="text-base leading-7">{course.description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6 p-8 pt-0">
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-xl bg-blue-50 p-4"><p className="text-sm text-gray-500">Duration</p><p className="text-xl font-semibold">{course.duration_hours} hours</p></div>
            <div className="rounded-xl bg-cyan-50 p-4"><p className="text-sm text-gray-500">Lessons</p><p className="text-xl font-semibold">{course.number_of_lessons}</p></div>
            <div className="rounded-xl bg-emerald-50 p-4"><p className="text-sm text-gray-500">Price</p><p className="text-xl font-semibold">{course.is_free ? "Free" : formatCurrency(course.price)}</p></div>
          </div>
          {message && <p className="rounded-lg bg-blue-50 p-3 text-sm text-blue-800">{message}</p>}
          <Button onClick={handleEnroll} disabled={enrolling} className="w-full sm:w-auto">
            {enrolling ? "Enrolling..." : course.is_free ? "Enroll now" : "Enroll and continue"}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}