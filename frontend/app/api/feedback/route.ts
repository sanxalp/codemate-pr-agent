import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

// Fake data for fallback
const fakeFeedback = {
  summary:
    "This pull request introduces a new authentication feature with JWT tokens. The implementation looks solid overall with good error handling.",
  score: 85,
  issues: [
    {
      type: "warning",
      file: "src/auth/service.ts",
      line: 42,
      message:
        "Password hashing algorithm could be upgraded from bcrypt to argon2 for better security",
      suggestion:
        "Consider migrating to argon2 for improved resistance against GPU-based attacks",
    },
    {
      type: "info",
      file: "src/auth/controller.ts",
      line: 15,
      message: "Missing input validation for email format",
      suggestion:
        "Add email format validation using a regex pattern or validation library",
    },
    {
      type: "error",
      file: "src/auth/middleware.ts",
      line: 28,
      message: "Missing error handling for expired tokens",
      suggestion:
        "Implement proper error handling for expired JWT tokens with appropriate HTTP status codes",
    },
  ],
  recommendations: [
    "Add unit tests for the authentication service",
    "Implement rate limiting for login endpoints",
    "Add logging for security-related events",
    "Consider adding multi-factor authentication support",
  ],
};

export async function GET() {
  try {
    // First try to call the Python backend
    const response = await fetch(`${BACKEND_URL}/feedback`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    // If backend responds successfully, return its data
    if (response.ok) {
      const feedback = await response.json();
      return NextResponse.json(feedback);
    }

    // If backend responds with 404 (feedback not ready), return that error
    if (response.status === 404) {
      return NextResponse.json(
        { error: "Feedback not ready yet" },
        { status: 404 }
      );
    }

    // For other backend errors, fall back to fake data
    console.log("Backend returned error, using fake data as fallback");
  } catch (error) {
    // If backend is unreachable, fall back to fake data
    console.log(
      "Backend unreachable, using fake data as fallback:",
      error instanceof Error ? error.message : "Unknown error"
    );
  }

  // Return fake feedback data as fallback
  return NextResponse.json(fakeFeedback);
}
