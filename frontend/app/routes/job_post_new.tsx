import { useParams, useNavigate,redirect } from "react-router";
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
  const [mode, setMode] = useState("review"); // review → submit

  // NEW: 3-output pipeline
  const [summary, setSummary] = useState("");
  const [rewritten, setRewritten] = useState("");
  const [fixed, setFixed] = useState("");

  async function handleSubmit(e: any) {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.target);
    const title = formData.get("title") as string;
    const description = formData.get("description") as string;

    // STEP 1 → AI REVIEW (3 prompts)
    if (mode === "review") {
      const res = await fetch("/api/review-job", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: description }),
      });

      const data = await res.json();

      // store all 3 results
      setSummary(data.summary);
      setRewritten(data.rewritten);
      setFixed(data.fixed);

      setMode("submit");
      setLoading(false);
      return;
    }

    // STEP 2 → SUBMIT JOB
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

  // NEW: Apply the fixed improved JD into the textarea
  function applyFix() {
    const textarea = document.querySelector(
      "textarea[name='description']"
    ) as HTMLTextAreaElement;

    if (textarea) textarea.value = fixed;
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
            ? "Step 1 of 2 — Review Job Description with AI"
            : "Step 2 of 2 — Submit Final Job Post"}
        </div>

        <form
          onSubmit={handleSubmit}
          style={{
            display: "grid",
            gap: "20px",
          }}
        >
          {/* Job Title */}
          <div style={{ display: "grid", gap: "6px" }}>
            <label style={{ fontWeight: "600", fontSize: "14px" }}>
              Job Title
            </label>
            <input
              name="title"
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

          {/* AI Review Section */}
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

          {/* Submit / Review Button */}
          <div style={{ display: "flex", justifyContent: "flex-end" }}>
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
                backgroundColor: mode === "review" ? "#2563eb" : "#10b981",
                transition: "0.2s",
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
