import { useParams, useNavigate } from "react-router";
import { useState } from "react";
import { userContext } from "~/context";

export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
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

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.target);

    const payload = {
      title: formData.get("title"),
      description: formData.get("description"),
      job_board_id: parseInt(jobBoardId),
    };

    // Submit as form data (FastAPI expects Form())
    const body = new URLSearchParams(payload);

    await fetch("/api/job-posts", {
      method: "POST",
      body,
    });

    navigate(`/job-boards/${jobBoardId}/job-posts`);
  }

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "50px auto",
        padding: "30px",
        borderRadius: "12px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
        backgroundColor: "#fff",
        fontFamily: "sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "30px", fontSize: "28px" }}>
        Create Job Post
      </h1>

      <form
        onSubmit={handleSubmit}
        style={{
          display: "grid",
          gap: "25px",
        }}
      >
        {/* Job Title */}
        <div style={{ display: "grid", gap: "8px" }}>
          <label style={{ fontWeight: "bold", fontSize: "14px" }}>Job Title</label>
          <input
            name="title"
            required
            placeholder="Enter job title"
            style={{
              padding: "12px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              fontSize: "14px",
            }}
          />
        </div>

        {/* Job Description */}
        <div style={{ display: "grid", gap: "8px" }}>
          <label style={{ fontWeight: "bold", fontSize: "14px" }}>Job Description</label>
          <textarea
            name="description"
            rows={6}
            placeholder="Enter job description"
            style={{
              padding: "12px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              fontSize: "14px",
              resize: "vertical",
            }}
          />
        </div>

        {/* Submit Button */}
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: "12px 25px",
              fontSize: "16px",
              fontWeight: "bold",
              color: "#fff",
              backgroundColor: "#007bff",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              transition: "background 0.3s",
            }}
          >
            {loading ? "Submitting..." : "Submit Job"}
          </button>
        </div>
      </form>
    </div>
  );
}
