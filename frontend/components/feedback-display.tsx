"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { CheckCircle, AlertCircle, Info, AlertTriangle, FileText, Star } from "lucide-react"

interface ReviewFeedback {
  summary: string
  issues: Array<{
    type: "error" | "warning" | "info"
    file: string
    line?: number
    message: string
    suggestion?: string
  }>
  score: number
  recommendations: string[]
}

interface FeedbackDisplayProps {
  feedback: ReviewFeedback
}

export function FeedbackDisplay({ feedback }: FeedbackDisplayProps) {
  const getIssueIcon = (type: string) => {
    switch (type) {
      case "error":
        return <AlertCircle className="w-4 h-4 text-destructive" />
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-warning" />
      case "info":
        return <Info className="w-4 h-4 text-primary" />
      default:
        return <Info className="w-4 h-4 text-muted-foreground" />
    }
  }

  const getIssueColor = (type: string) => {
    switch (type) {
      case "error":
        return "destructive"
      case "warning":
        return "secondary"
      case "info":
        return "outline"
      default:
        return "outline"
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-success"
    if (score >= 60) return "text-warning"
    return "text-destructive"
  }

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-success" />
            Review Complete
          </CardTitle>
          <CardDescription>AI analysis of your pull request</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Code Quality Score</span>
            <span className={`text-2xl font-bold ${getScoreColor(feedback.score)}`}>{feedback.score}/100</span>
          </div>
          <Progress value={feedback.score} className="h-2" />
          <p className="text-muted-foreground">{feedback.summary}</p>
        </CardContent>
      </Card>

      {/* Issues */}
      {feedback.issues.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Issues Found ({feedback.issues.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {feedback.issues.map((issue, index) => (
                <div key={index} className="border border-border rounded-lg p-4 space-y-3">
                  <div className="flex items-start gap-3">
                    {getIssueIcon(issue.type)}
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-2">
                        <Badge variant={getIssueColor(issue.type) as any}>{issue.type}</Badge>
                        <span className="text-sm font-mono text-muted-foreground">
                          {issue.file}
                          {issue.line && `:${issue.line}`}
                        </span>
                      </div>
                      <p className="text-sm text-foreground">{issue.message}</p>
                      {issue.suggestion && (
                        <div className="bg-muted rounded-md p-3">
                          <p className="text-sm text-muted-foreground">
                            <strong>Suggestion:</strong> {issue.suggestion}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      {feedback.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Star className="w-5 h-5" />
              Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {feedback.recommendations.map((recommendation, index) => (
                <li key={index} className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <span className="text-sm text-muted-foreground">{recommendation}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
