"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2, Send, Github, GitBranch } from "lucide-react";

interface PRSubmissionFormProps {
  onSubmit: (prUrl: string) => void;
  isLoading: boolean;
}

export function PRSubmissionForm({
  onSubmit,
  isLoading,
}: PRSubmissionFormProps) {
  const [prUrl, setPrUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prUrl.trim()) {
      // Add protocol if missing
      let url = prUrl.trim();
      if (!url.startsWith("http://") && !url.startsWith("https://")) {
        url = `https://${url}`;
      }
      onSubmit(url);
    }
  };

  const isValidPR = (url: string) => {
    const githubPRRegex =
      /^(https?:\/\/)?github\.com\/[\w.-]+\/[\w.-]+\/pull\/\d+$/;
    const gitlabMRRegex =
      /^(https?:\/\/)?gitlab\.com\/[\w.-]+\/[\w.-]+\/-\/merge_requests\/\d+$/;
    const bitbucketPRRegex =
      /^(https?:\/\/)?bitbucket\.org\/[\w.-]+\/[\w.-]+\/pull-requests\/\d+$/;

    return (
      githubPRRegex.test(url) ||
      gitlabMRRegex.test(url) ||
      bitbucketPRRegex.test(url)
    );
  };

  const getProviderInfo = (url: string) => {
    if (url.includes("github.com")) return { name: "GitHub", icon: Github };
    if (url.includes("gitlab.com")) return { name: "GitLab", icon: GitBranch };
    if (url.includes("bitbucket.org"))
      return { name: "Bitbucket", icon: GitBranch };
    return null;
  };

  const provider = prUrl ? getProviderInfo(prUrl) : null;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="pr-url">Pull Request / Merge Request URL</Label>
        <Input
          id="pr-url"
          type="url"
          placeholder="https://github.com/owner/repo/pull/123 or GitLab/Bitbucket URL"
          value={prUrl}
          onChange={(e) => setPrUrl(e.target.value)}
          disabled={isLoading}
          className="font-mono text-sm"
        />
        {prUrl && provider && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <provider.icon className="w-4 h-4" />
            <span>Detected: {provider.name}</span>
          </div>
        )}
        {prUrl && !isValidPR(prUrl) && (
          <p className="text-sm text-destructive">
            Please enter a valid GitHub, GitLab, or Bitbucket PR/MR URL
          </p>
        )}
      </div>

      <div className="text-xs text-muted-foreground space-y-1">
        <p>Supported formats:</p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>GitHub: https://github.com/owner/repo/pull/123</li>
          <li>GitLab: https://gitlab.com/owner/repo/-/merge_requests/123</li>
          <li>Bitbucket: https://bitbucket.org/owner/repo/pull-requests/123</li>
        </ul>
      </div>

      <Button
        type="submit"
        disabled={!prUrl.trim() || !isValidPR(prUrl) || isLoading}
        className="w-full"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Send className="w-4 h-4 mr-2" />
            Review Pull Request
          </>
        )}
      </Button>
    </form>
  );
}
