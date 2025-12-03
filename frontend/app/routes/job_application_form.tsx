import { useParams } from "react-router";
import { useState } from "react";

export default function JobApplicationForm() {
  const { postId } = useParams();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [resume, setResume] = useState<File | null>(null);

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!resume) {
      setError("Please upload your resume (PDF).");
      return;
    }

    const formData = new FormData();
    formData.append("job_post_id", postId!);
    formData.append("first_name", firstName);
    formData.append("last_name", lastName);
    formData.append("email", email);
    formData.append("resume", resume);

    try {
      const res = await fetch("/api/job-applications", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong");

      setSuccess("Application submitted successfully!");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Apply for This Job</h2>

      {error && <p style={styles.error}>{error}</p>}
      {success && <p style={styles.success}>{success}</p>}

      <form onSubmit={handleSubmit} style={styles.form}>
        
        {/* First Name */}
        <div style={styles.field}>
          <label style={styles.label}>First Name</label>
          <input
            required
            style={styles.input}
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </div>

        {/* Last Name */}
        <div style={styles.field}>
          <label style={styles.label}>Last Name</label>
          <input
            required
            style={styles.input}
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </div>

        {/* Email */}
        <div style={styles.field}>
          <label style={styles.label}>Email</label>
          <input
            required
            type="email"
            style={styles.input}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        {/* Resume Upload */}
        <div style={styles.field}>
          <label style={styles.label}>Resume (PDF)</label>

          {/* Hidden Input */}
          <input
            id="resume-input"
            type="file"
            accept="application/pdf"
            onChange={(e) => setResume(e.target.files?.[0] ?? null)}
            style={{ display: "none" }}
          />

          {/* Custom Upload Button */}
          <button
            type="button"
            onClick={() => document.getElementById("resume-input")!.click()}
            style={styles.uploadBtn}
          >
            📄 Upload Resume
          </button>

          {/* File Name */}
          <div style={styles.fileName}>
            {resume ? resume.name : "No file selected"}
          </div>

          <small style={styles.helperText}>PDF only. Max size 2MB.</small>
        </div>

        {/* Submit Button */}
        <button type="submit" style={styles.button}>
          Submit Application
        </button>
      </form>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: "600px",
    margin: "40px auto",
    padding: "30px",
    borderRadius: "10px",
    border: "1px solid #e1e1e1",
    background: "#fff",
    boxShadow: "0 3px 12px rgba(0,0,0,0.06)",
  },
  title: {
    textAlign: "center",
    marginBottom: "25px",
  },
  form: {
    display: "grid",
    gridTemplateColumns: "1fr",
    rowGap: "18px",
  },
  field: {
    display: "flex",
    flexDirection: "column",
  },
  label: {
    marginBottom: "6px",
    fontWeight: 600,
  },
  input: {
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    fontSize: "15px",
  },
  uploadBtn: {
    padding: "10px 14px",
    background: "#f2f2f2",
    border: "1px solid #ccc",
    borderRadius: "5px",
    cursor: "pointer",
    fontWeight: 600,
    width: "fit-content",
  },
  fileName: {
    marginTop: "8px",
    fontStyle: "italic",
    color: "#444",
  },
  helperText: {
    marginTop: "5px",
    color: "#777",
    fontSize: "12px",
  },
  button: {
    marginTop: "10px",
    padding: "12px 0",
    border: "none",
    borderRadius: "5px",
    background: "#007bff",
    color: "white",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: "16px",
  },
  error: {
    color: "red",
    textAlign: "center",
    marginBottom: "10px",
  },
  success: {
    color: "green",
    textAlign: "center",
    marginBottom: "10px",
  },
};
