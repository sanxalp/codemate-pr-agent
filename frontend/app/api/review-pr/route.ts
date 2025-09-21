import { type NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";

export async function POST(request: NextRequest) {
  try {
    const { prUrl } = await request.json();

    if (!prUrl) {
      return NextResponse.json(
        { error: "PR URL is required" },
        { status: 400 }
      );
    }

    // Validate PR URL format for supported providers
    const githubPRRegex =
      /^(https?:\/\/)?github\.com\/[\w.-]+\/[\w.-]+\/pull\/\d+$/;
    const gitlabMRRegex =
      /^(https?:\/\/)?gitlab\.com\/[\w.-]+\/[\w.-]+\/-\/merge_requests\/\d+$/;
    const bitbucketPRRegex =
      /^(https?:\/\/)?bitbucket\.org\/[\w.-]+\/[\w.-]+\/pull-requests\/\d+$/;

    // Add protocol if missing
    let normalizedPrUrl = prUrl.trim();
    if (
      !normalizedPrUrl.startsWith("http://") &&
      !normalizedPrUrl.startsWith("https://")
    ) {
      normalizedPrUrl = `https://${normalizedPrUrl}`;
    }

    const isValidUrl =
      githubPRRegex.test(normalizedPrUrl) ||
      gitlabMRRegex.test(normalizedPrUrl) ||
      bitbucketPRRegex.test(normalizedPrUrl);

    if (!isValidUrl) {
      return NextResponse.json(
        {
          error: "Invalid PR URL format. Supported: GitHub, GitLab, Bitbucket",
        },
        { status: 400 }
      );
    }

    console.log(`Submitting PR for review: ${normalizedPrUrl}`);

    // First try to call the Python backend
    try {
      const response = await fetch(`${BACKEND_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prUrl: normalizedPrUrl }),
      });

      if (response.ok) {
        const result = await response.json();
        return NextResponse.json({
          message: "PR submitted for review",
          result,
        });
      }

      // If backend returns an error, fall back to fake success
      console.log("Backend returned error, using fake data as fallback");
    } catch (backendError) {
      // If backend is unreachable, fall back to fake success
      console.log(
        "Backend unreachable, using fake data as fallback:",
        backendError instanceof Error ? backendError.message : "Unknown error"
      );
    }

    // Return fake success response as fallback
    return NextResponse.json({
      message: "PR submitted for review (fake response)",
      result: {
        prUrl: normalizedPrUrl,
        status: "processing",
      },
    });
  } catch (error) {
    console.error("Error submitting PR:", error);
    return NextResponse.json(
      { error: "Failed to submit PR for review" },
      { status: 500 }
    );
  }
}

// Add a GET method for health check
export async function GET() {
  return NextResponse.json({
    message: "PR Review API is running",
    status: "ok",
  });
}
