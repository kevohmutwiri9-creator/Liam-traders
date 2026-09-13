"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { coursesAPI, getCollectionResults } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function CourseDetailPage() {
  const params = useParams();
  const router = useRouter();
  const courseId = Number(params.id);
  const [course, setCourse] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [message, setMessage] = useState("");
  const [lessons, setLessons] = useState<any[]>([]);
  const [enrollment, setEnrollment] = useState<any>(null);
  const [completingLesson, setCompletingLesson] = useState<number | null>(null);
  const [notes, setNotes] = useState<Record<number, string>>({});
  const [savingNote, setSavingNote] = useState<number | null>(null);

  const loadCourse = async () => {
    try {
      const [courseResponse, lessonsResponse, enrollmentsResponse, notesResponse] = await Promise.all([
        coursesAPI.getCourse(courseId),
        coursesAPI.getCourseLessons(courseId),
        coursesAPI.getMyEnrollments(),
        coursesAPI.getLessonNotes(courseId),
      ]);
      setCourse(courseResponse.data);
      setLessons(getCollectionResults(lessonsResponse.data));
      const enrollments = getCollectionResults(enrollmentsResponse.data);
      setEnrollment(enrollments.find((item: any) => item.course === courseId) || null);
      const noteMap: Record<number, string> = {};
      getCollectionResults(notesResponse.data).forEach((note: any) => {
        noteMap[note.lesson] = note.content;
      });
      setNotes(noteMap);
    } catch (error) {
      router.push("/dashboard/courses");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourse();
  }, [courseId, router]);

  const handleEnroll = async () => {
    setEnrolling(true);
    setMessage("");
    try {
      await coursesAPI.enrollInCourse(courseId);
      setMessage("Enrollment successful. Your course is ready to start.");
      await loadCourse();
    } catch (error: any) {
      const detail = error.response?.data?.non_field_errors?.[0] || error.response?.data?.detail;
      if (detail?.toLowerCase().includes("already enrolled")) {
        setMessage("You are already enrolled. Continue with your lessons below.");
        await loadCourse();
      } else {
        setMessage(detail || "Unable to enroll in this course.");
      }
    } finally {
      setEnrolling(false);
    }
  };

  const completeLesson = async (lessonId: number) => {
    if (!enrollment) return;
    setCompletingLesson(lessonId);
    try {
      await coursesAPI.updateProgress(enrollment.id, {
        lesson_id: lessonId,
        is_completed: true,
        time_spent_seconds: 0,
      });
      await loadCourse();
      setMessage("Lesson completed. Your progress has been saved.");
    } catch (error: any) {
      setMessage(error.response?.data?.detail || "Unable to save lesson progress.");
    } finally {
      setCompletingLesson(null);
    }
  };

  const saveNote = async (lessonId: number) => {
    if (!notes[lessonId]?.trim()) return;
    setSavingNote(lessonId);
    try {
      await coursesAPI.saveLessonNote(lessonId, notes[lessonId]);
      setMessage("Note saved to your course library.");
    } catch (error: any) {
      setMessage(error.response?.data?.detail || "Unable to save note.");
    } finally {
      setSavingNote(null);
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
          {!enrollment ? (
            <Button onClick={handleEnroll} disabled={enrolling} className="w-full sm:w-auto">
              {enrolling ? "Enrolling..." : course.is_free ? "Enroll now" : "Enroll and continue"}
            </Button>
          ) : (
            <div className="space-y-4">
              <div className="rounded-xl bg-blue-50 p-4">
                <div className="flex items-center justify-between text-sm font-medium">
                  <span>Course progress</span><span>{enrollment.progress_percentage}%</span>
                </div>
                <div className="mt-2 h-2 overflow-hidden rounded-full bg-blue-100">
                  <div className="h-full bg-blue-600 transition-all" style={{ width: `${enrollment.progress_percentage}%` }} />
                </div>
              </div>
              <div className="space-y-3">
                {lessons.map((lesson) => {
                  const completed = enrollment.lessons_completed?.includes(lesson.id);
                  return (
                    <div key={lesson.id} className="space-y-3">
                      <div className="flex items-center justify-between rounded-xl border p-4">
                        <div className="min-w-0 flex-1"><p className="font-medium">{lesson.title}</p><p className="text-sm text-gray-500">{lesson.lesson_type}</p></div>
                        <Button variant={completed ? "outline" : "default"} disabled={completed || completingLesson === lesson.id} onClick={() => completeLesson(lesson.id)}>
                          {completed ? "Completed" : completingLesson === lesson.id ? "Saving..." : "Complete lesson"}
                        </Button>
                      </div>
                      <div className="space-y-3 rounded-xl bg-slate-50 p-4">
                        <p className="whitespace-pre-line text-sm leading-6 text-slate-700">{lesson.content || lesson.description}</p>
                        {lesson.video_url && <a href={lesson.video_url} target="_blank" rel="noreferrer" className="inline-flex rounded-lg bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700">Watch related video lessons</a>}
                        {lesson.resources?.length > 0 && <div className="flex flex-wrap gap-2">{lesson.resources.map((resource: any) => (
                          <a key={resource.url || resource.label} href={resource.url || "#"} target={resource.url ? "_blank" : undefined} rel="noreferrer" className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-blue-700 hover:border-blue-400">{resource.label}</a>
                        ))}</div>}
                      </div>
                      <div className="rounded-xl bg-amber-50 p-4">
                      <textarea
                        value={notes[lesson.id] || ""}
                        onChange={(event) => setNotes({ ...notes, [lesson.id]: event.target.value })}
                        placeholder="Write a note for this lesson..."
                        className="min-h-20 w-full resize-y rounded-lg border border-amber-200 bg-white p-3 text-sm outline-none focus:ring-2 focus:ring-amber-400"
                      />
                      <Button variant="outline" className="mt-2" disabled={savingNote === lesson.id || !notes[lesson.id]?.trim()} onClick={() => saveNote(lesson.id)}>
                        {savingNote === lesson.id ? "Saving note..." : "Save note"}
                      </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}