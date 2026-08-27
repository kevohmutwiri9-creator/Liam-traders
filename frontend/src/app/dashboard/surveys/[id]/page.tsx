"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { surveysAPI } from "@/lib/api";

export default function SurveyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const surveyId = parseInt(params.id as string);
  
  const [survey, setSurvey] = useState<any>(null);
  const [questions, setQuestions] = useState<any>([]);
  const [answers, setAnswers] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [surveyRes, questionsRes] = await Promise.all([
          surveysAPI.getSurvey(surveyId),
          surveysAPI.getSurveyQuestions(surveyId),
        ]);
        setSurvey(surveyRes.data);
        setQuestions(questionsRes.data);
      } catch (error) {
        console.error("Failed to fetch survey:", error);
        router.push("/dashboard/surveys");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [surveyId, router]);

  const handleAnswerChange = (questionId: number, value: any) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      await surveysAPI.submitSurvey(surveyId, { answers });
      router.push("/dashboard/surveys?success=true");
    } catch (error) {
      console.error("Failed to submit survey:", error);
      alert("Failed to submit survey. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const renderQuestion = (question: any) => {
    switch (question.question_type) {
      case 'text':
        return (
          <Textarea
            placeholder="Your answer..."
            value={answers[question.id] || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            required={question.is_required}
          />
        );
      case 'number':
        return (
          <Input
            type="number"
            placeholder="Your answer..."
            value={answers[question.id] || ''}
            onChange={(e) => handleAnswerChange(question.id, parseFloat(e.target.value))}
            required={question.is_required}
          />
        );
      case 'multiple_choice':
        return (
          <RadioGroup
            value={answers[question.id] || ''}
            onValueChange={(value) => handleAnswerChange(question.id, value)}
          >
            {question.options.map((option: string, idx: number) => (
              <div key={idx} className="flex items-center space-x-2">
                <RadioGroupItem value={option} id={`q${question.id}-opt${idx}`} />
                <Label htmlFor={`q${question.id}-opt${idx}`}>{option}</Label>
              </div>
            ))}
          </RadioGroup>
        );
      case 'checkbox':
        return (
          <div className="space-y-2">
            {question.options.map((option: string, idx: number) => (
              <div key={idx} className="flex items-center space-x-2">
                <Checkbox
                  id={`q${question.id}-opt${idx}`}
                  checked={(answers[question.id] || []).includes(option)}
                  onCheckedChange={(checked) => {
                    const current = answers[question.id] || [];
                    if (checked) {
                      handleAnswerChange(question.id, [...current, option]);
                    } else {
                      handleAnswerChange(question.id, current.filter((v: string) => v !== option));
                    }
                  }}
                />
                <Label htmlFor={`q${question.id}-opt${idx}`}>{option}</Label>
              </div>
            ))}
          </div>
        );
      case 'rating':
        return (
          <div className="flex items-center space-x-2">
            <Input
              type="number"
              min={question.min_value}
              max={question.max_value}
              value={answers[question.id] || ''}
              onChange={(e) => handleAnswerChange(question.id, parseInt(e.target.value))}
              required={question.is_required}
              className="w-20"
            />
            <span className="text-sm text-gray-600">
              ({question.min_value} - {question.max_value})
            </span>
          </div>
        );
      case 'dropdown':
        return (
          <select
            className="w-full p-2 border rounded-md"
            value={answers[question.id] || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            required={question.is_required}
          >
            <option value="">Select an option...</option>
            {question.options.map((option: string, idx: number) => (
              <option key={idx} value={option}>{option}</option>
            ))}
          </select>
        );
      case 'date':
        return (
          <Input
            type="date"
            value={answers[question.id] || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            required={question.is_required}
          />
        );
      default:
        return <p className="text-gray-500">Unsupported question type</p>;
    }
  };

  if (loading) {
    return <div className="container py-8">Loading survey...</div>;
  }

  return (
    <div className="container py-8 max-w-3xl">
      <Button variant="ghost" onClick={() => router.push("/dashboard/surveys")} className="mb-4">
        ← Back to Surveys
      </Button>
      
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{survey.title}</CardTitle>
          <CardDescription>{survey.description}</CardDescription>
          <div className="flex gap-4 mt-4 text-sm text-gray-600">
            <span>⏱ {survey.estimated_time_minutes} min</span>
            <span>💰 {survey.reward_amount} KES</span>
            <span>❓ {survey.number_of_questions} questions</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-8">
            {questions.map((question: any, idx: number) => (
              <div key={question.id}>
                <div className="mb-3">
                  <span className="font-medium">Q{idx + 1}.</span>
                  <span className="ml-2">{question.question_text}</span>
                  {question.is_required && <span className="text-red-500 ml-1">*</span>}
                </div>
                {renderQuestion(question)}
              </div>
            ))}
          </div>
          
          <div className="mt-8 flex justify-end gap-4">
            <Button variant="outline" onClick={() => router.push("/dashboard/surveys")}>
              Cancel
            </Button>
            <Button onClick={handleSubmit} disabled={submitting}>
              {submitting ? "Submitting..." : "Submit Survey"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
