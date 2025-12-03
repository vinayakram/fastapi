import { Form, useParams, redirect } from "react-router";

export async function action({ params, request }) {
  const formData = await request.formData();

  const payload = {
    title: formData.get("title"),
    description: formData.get("description"),
  };

  await fetch(`/api/job-boards/${params.jobBoardId}/job-posts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  return redirect(`/job-boards/${params.jobBoardId}/job-posts`);
}

export default function JobPostForm() {
  const { jobBoardId } = useParams();

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto" }}>
      <h1>Create Job Post</h1>

      <Form method="post" style={{ display: "grid", gap: "20px" }}>
        <div>
          <label>Job Title</label>
          <input name="title" required />
        </div>

        <div>
          <label>Job Description</label>
          <textarea name="description" rows={5} />
        </div>

        <button type="submit">Submit Job</button>
      </Form>
    </div>
  );
}
