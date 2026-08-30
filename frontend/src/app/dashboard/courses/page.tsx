"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/utils";
import { coursesAPI } from "@/lib/api";

export default function CoursesPage() {
  const [courses, setCourses] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const res = await coursesAPI.getCourses({ status: 'published' });
        console.log('Courses API response:', res.data);
        setCourses(res.data);
      } catch (error: any) {
        console.error("Failed to fetch courses:", error);
        console.error("Error response:", error.response?.data);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return <div className="container py-8">Loading courses...</div>;
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-600';
      case 'intermediate': return 'bg-yellow-600';
      case 'advanced': return 'bg-red-600';
      default: return 'bg-gray-600';
    }
  };

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Courses</h1>
        <p className="text-gray-600 mt-2">Improve your skills with our courses</p>
      </div>

      {courses?.results && courses.results.length > 0 ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.results.map((course: any) => (
            <Card key={course.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <Badge className={getDifficultyColor(course.difficulty)}>{course.difficulty}</Badge>
                  <Badge variant="outline">{course.category}</Badge>
                </div>
                <CardTitle className="text-lg">{course.title}</CardTitle>
                <CardDescription className="line-clamp-2">{course.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Price:</span>
                    <span className={`font-bold ${course.is_free ? 'text-green-600' : 'text-blue-600'}`}>
                      {course.is_free ? 'Free' : formatCurrency(course.price)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Duration:</span>
                    <span>{course.duration_hours} hours</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Lessons:</span>
                    <span>{course.number_of_lessons}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Level Required:</span>
                    <span>{course.min_level_required}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Enrolled:</span>
                    <span>{course.number_of_enrollments}</span>
                  </div>
                  {course.average_rating > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Rating:</span>
                      <span className="text-yellow-600">⭐ {course.average_rating.toFixed(1)}</span>
                    </div>
                  )}
                  <Button className="w-full mt-4">
                    {course.is_free ? 'Enroll Now' : 'View Course'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12">
            <p className="text-gray-600 text-center">No courses available at the moment. Check back later!</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
