"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Loader2, GitPullRequest, AlertCircle, Code2 } from "lucide-react";
import { PRSubmissionForm } from "@/components/pr-submission-form";
import { FeedbackDisplay } from "@/components/feedback-display";

interface ReviewFeedback {
  summary: string;
  issues: Array<{
    type: "error" | "warning" | "info";
    file: string;
    line?: number;
    message: string;
    suggestion?: string;
  }>;
  score: number;
  recommendations: string[];
}

export default function HomePage() {
  const [feedback, setFeedback] = useState<ReviewFeedback | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmitPR = async (prUrl: string) => {
    setIsLoading(true);
    setError(null);
    setFeedback(null);

    try {
      // Submit PR URL to Python backend
      const response = await fetch("/api/review-pr", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prUrl }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit PR for review");
      }

      // Poll for feedback.json
      const pollForFeedback = async () => {
        const feedbackResponse = await fetch("/api/feedback");
        if (feedbackResponse.ok) {
          const feedbackData = await feedbackResponse.json();
          setFeedback(feedbackData);
          setIsLoading(false);
        } else {
          // Continue polling if feedback not ready
          setTimeout(pollForFeedback, 2000);
        }
      };

      // Start polling after a short delay
      setTimeout(pollForFeedback, 1000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-lg">
              <Code2 className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">
                PR Review Agent
              </h1>
              <p className="text-muted-foreground">
                AI-powered code review for your pull requests
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Submission Form */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <GitPullRequest className="w-5 h-5" />
                Submit Pull Request for Review
              </CardTitle>
              <CardDescription>
                Enter a GitHub, GitLab, or Bitbucket PR/MR URL to get AI-powered
                code review feedback
              </CardDescription>
            </CardHeader>
            <CardContent>
              <PRSubmissionForm
                onSubmit={handleSubmitPR}
                isLoading={isLoading}
              />
            </CardContent>
          </Card>

          {/* Loading State */}
          {isLoading && (
            <Card>
              <CardContent className="py-8">
                <div className="flex flex-col items-center justify-center space-y-4">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                  <div className="text-center">
                    <h3 className="font-semibold text-foreground">
                      Analyzing Pull Request
                    </h3>
                    <p className="text-muted-foreground">
                      Our AI is reviewing your code...
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Error State */}
          {error && (
            <Card className="border-destructive">
              <CardContent className="py-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertCircle className="w-5 h-5" />
                  <div>
                    <h3 className="font-semibold">Error</h3>
                    <p className="text-sm">{error}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Feedback Display */}
          {feedback && <FeedbackDisplay feedback={feedback} />}

          {/* Instructions */}
          {!feedback && !isLoading && (
            <Card>
              <CardHeader>
                <CardTitle>How it works</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="flex flex-col items-center text-center space-y-2">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                      1
                    </div>
                    <h4 className="font-medium">Submit PR URL</h4>
                    <p className="text-sm text-muted-foreground">
                      Paste your PR/MR URL from any supported platform
                    </p>
                  </div>
                  <div className="flex flex-col items-center text-center space-y-2">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                      2
                    </div>
                    <h4 className="font-medium">AI Analysis</h4>
                    <p className="text-sm text-muted-foreground">
                      Our Python backend analyzes your code
                    </p>
                  </div>
                  <div className="flex flex-col items-center text-center space-y-2">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                      3
                    </div>
                    <h4 className="font-medium">Get Feedback</h4>
                    <p className="text-sm text-muted-foreground">
                      Receive detailed review and suggestions
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
