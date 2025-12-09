import { useParams, useNavigate, redirect } from "react-router";
import { useState } from "react";
import { userContext } from "~/context";

export async function clientLoader({ context }) {
  const me = context.get(userContext);
  const isAdmin = me?.is_admin ?? false;

  if (!isAdmin) {
    throw redirect("/admin-login");
  }

  return {};
}

export default function JobPostForm() {
  const { jobBoardId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<"review" | "submit">("review");

  // Controlled Inputs
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  // AI Outputs
  const [summary, setSummary] = useState("");
  const [rewritten, setRewritten] = useState("");
  const [fixed, setFixed] = useState("");

  // Resume Recommendations
  const [recommendations, setRecommendations] = useState<any[]>([]);

  async function handleSubmit(e: any) {
    e.preventDefault();
    setLoading(true);

    // STEP 1 → AI REVIEW (with 3-step prompt pipeline)
    if (mode === "review") {
      const res = await fetch("/api/review-job", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: description }),
      });

      const data = await res.json();

      setSummary(data.summary || "");
      setRewritten(data.rewritten || "");
      setFixed(data.fixed || "");

      setMode("submit");
      setLoading(false);
      return;
    }

    // STEP 2 → SUBMIT FINAL JOB POST
    const payload = new URLSearchParams({
      job_board_id: jobBoardId!,
      title,
      description,
    });

    await fetch("/api/job-posts", {
      method: "POST",
      body: payload,
    });

    navigate(`/job-boards/${jobBoardId}/job-posts`);
  }

  // Apply FIXED job description
  function applyFix() {
    setDescription(fixed);
  }

  // NEW → Candidate Recommendations from Vector DB
  async function recommendCandidates() {
    if (!description.trim()) {
      alert("Please enter a job description first.");
      return;
    }

    setLoading(true);

    const res = await fetch("/api/recommend-resumes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        job_description: description,
        top_k: 5,
      }),
    });

    const data = await res.json();
    setRecommendations(data.recommendations || []); // safe fallback
    setLoading(false);
  }

  return (
    <div
      style={{
        maxWidth: "750px",
        margin: "40px auto",
        padding: "20px",
        fontFamily: "sans-serif",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "25px",
          fontSize: "28px",
          fontWeight: "600",
        }}
      >
        Create Job Post
      </h1>

      <div
        style={{
          background: "#ffffff",
          padding: "25px",
          borderRadius: "12px",
          boxShadow: "0 4px 14px rgba(0,0,0,0.08)",
        }}
      >
        {/* Step Indicator */}
        <div
          style={{
            marginBottom: "20px",
            padding: "12px 15px",
            background: "#eef2ff",
            borderRadius: "8px",
            fontWeight: "600",
            color: "#4338ca",
            fontSize: "14px",
          }}
        >
          {mode === "review"
            ? "Step 1 — AI Review + Candidate Recommendations"
            : "Step 2 — Submit Final Job Post"}
        </div>

        <form
          onSubmit={handleSubmit}
          style={{ display: "grid", gap: "20px" }}
        >
          {/* Job Title */}
          <div style={{ display: "grid", gap: "6px" }}>
            <label style={{ fontWeight: "600", fontSize: "14px" }}>
              Job Title
            </label>
            <input
              name="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Enter job title"
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "15px",
              }}
            />
          </div>

          {/* Job Description */}
          <div style={{ display: "grid", gap: "6px" }}>
            <label style={{ fontWeight: "600", fontSize: "14px" }}>
              Job Description
            </label>
            <textarea
              name="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={6}
              placeholder="Enter job description..."
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "15px",
                resize: "vertical",
              }}
            />
          </div>

          {/* AI Review Output */}
          {(summary || rewritten) && (
            <div
              style={{
                marginTop: "10px",
                padding: "18px",
                background: "#f9fafb",
                borderRadius: "10px",
                border: "1px solid #e5e7eb",
                color: "#374151",
                whiteSpace: "pre-wrap",
              }}
            >
              <h3 style={{ marginBottom: "10px", fontSize: "18px" }}>
                AI Summary of Issues
              </h3>
              <div style={{ fontSize: "14px", lineHeight: "1.6" }}>
                {summary}
              </div>

              <h3 style={{ margin: "20px 0 10px", fontSize: "18px" }}>
                Rewritten Problem Areas
              </h3>
              <div style={{ fontSize: "14px", lineHeight: "1.6" }}>
                {rewritten}
              </div>

              <button
                type="button"
                onClick={applyFix}
                style={{
                  marginTop: "16px",
                  padding: "10px 20px",
                  background: "#10b981",
                  borderRadius: "8px",
                  color: "white",
                  border: "none",
                  cursor: "pointer",
                  fontWeight: "600",
                }}
              >
                Fix for Me
              </button>
            </div>
          )}

          {/* Resume Recommendations */}
          {recommendations?.length > 0 && (
            <div
              style={{
                marginTop: "20px",
                padding: "18px",
                background: "#f0fdf4",
                borderRadius: "10px",
                border: "1px solid #86efac",
              }}
            >
              <h3
                style={{
                  marginBottom: "12px",
                  fontSize: "18px",
                  color: "#166534",
                }}
              >
                Recommended Candidates
              </h3>

              {recommendations.map((r, i) => (
                <div
                  key={i}
                  style={{
                    padding: "10px 0",
                    borderBottom:
                      i < recommendations.length - 1
                        ? "1px solid #d1fae5"
                        : "none",
                  }}
                >
                  <strong>{r.metadata?.applicant_name}</strong>
                  <br />
                  <span>{r.metadata?.email}</span>
                  <br />
                  <span>
                    Match Score: {(r.score * 100).toFixed(1)}%
                  </span>

                  {r.metadata?.filename && (
                    <div>
                      <a
                        href={`/uploads/resumes/${r.metadata.filename}`}
                        target="_blank"
                        style={{ color: "#2563eb", fontSize: "14px" }}
                      >
                        View Resume
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Buttons */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: "10px",
            }}
          >
            {/* Recommend Button */}
            {mode === "review" && (
              <button
                type="button"
                onClick={recommendCandidates}
                style={{
                  padding: "10px 20px",
                  background: "#9333ea",
                  color: "white",
                  borderRadius: "8px",
                  border: "none",
                  cursor: "pointer",
                }}
              >
                Recommend Candidates
              </button>
            )}

            {/* Review / Submit */}
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: "12px 30px",
                fontSize: "16px",
                fontWeight: "700",
                borderRadius: "8px",
                border: "none",
                cursor: "pointer",
                color: "#fff",
                backgroundColor:
                  mode === "review" ? "#2563eb" : "#10b981",
              }}
            >
              {loading
                ? "Processing..."
                : mode === "review"
                ? "Review with AI"
                : "Submit Job"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
