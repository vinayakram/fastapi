export async function clientLoader({ params }) {
    const res = await fetch(`/api/job-boards/${params.jobBoardId}/job-posts`);
    const jobPosts = await res.json();

    // Safety: always return an array (even if API returns nothing or error)
    const safeJobPosts = Array.isArray(jobPosts) ? jobPosts : [];

    return { jobPosts: safeJobPosts };
}

export default function JobPosts({ loaderData }) {
    // Extra safety in case something weird happens
    const jobPosts = Array.isArray(loaderData.jobPosts) ? loaderData.jobPosts : [];

    if (jobPosts.length === 0) {
        return (
            <div style={{ padding: "40px", textAlign: "center", fontFamily: "sans-serif" }}>
                <h1>No job posts yet</h1>
                <p>This board is empty.</p>
            </div>
        );
    }

    return (
        <div style={{ padding: "20px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
            <h1 style={{ fontSize: "32px", marginBottom: "30px" }}>Job Posts</h1>

            <div style={{ display: "grid", gap: "20px" }}>
                {jobPosts.map((jobPost) => (
                    <div
                        key={jobPost.id}
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "20px",
                            background: "#fff",
                            boxShadow: "0 2px 10px rgba(0,0,0,0.05)"
                        }}
                    >
                        <h2 style={{ margin: "0 0 10px 0", fontSize: "22px", color: "#1a0dab" }}>
                            {jobPost.title}
                        </h2>
                        <p style={{ margin: 0, color: "#333", lineHeight: "1.6" }}>
                            {jobPost.description || "No description provided."}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}