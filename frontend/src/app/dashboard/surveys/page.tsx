"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/utils";
import { surveysAPI } from "@/lib/api";

export default function SurveysPage() {
  const router = useRouter();
  const [surveys, setSurveys] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSurveys = async () => {
      try {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        console.info('[SurveysPage] token present:', Boolean(token));
        console.info('[SurveysPage] API base URL:', process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api');

        const res = await surveysAPI.getSurveys({ status: 'active' });
        console.log('Surveys API response:', res.data);
        setSurveys(res.data);
      } catch (error: any) {
        console.error("Failed to fetch surveys:", error);
        console.error("Error response:", error.response?.data);
        setSurveys({ count: 0, next: null, previous: null, results: [] });
      } finally {
        setLoading(false);
      }
    };

    fetchSurveys();
  }, []);

  if (loading) {
    return <div className="container py-8">Loading surveys...</div>;
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Surveys</h1>
        <p className="text-gray-600 mt-2">Complete surveys and earn rewards</p>
      </div>

      {surveys?.results && surveys.results.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {surveys.results.map((survey: any) => (
            <Card key={survey.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <Badge className="mb-2">{survey.category}</Badge>
                  <Badge variant="outline">{survey.current_participants}/{survey.max_participants}</Badge>
                </div>
                <CardTitle className="text-lg">{survey.title}</CardTitle>
                <CardDescription>{survey.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Reward:</span>
                    <span className="font-bold text-green-600">{formatCurrency(survey.reward_amount)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Duration:</span>
                    <span>{survey.estimated_time_minutes} min</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Questions:</span>
                    <span>{survey.number_of_questions}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Level Required:</span>
                    <span>{survey.min_level_required}</span>
                  </div>
                  <Button className="w-full mt-4" onClick={() => router.push(`/dashboard/surveys/${survey.id}`)}>Start Survey</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12">
            <p className="text-gray-600 text-center">No surveys available at the moment. Check back later!</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
