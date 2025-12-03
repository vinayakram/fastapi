import { Link, useParams } from "react-router";

export async function clientLoader({ params }) {
    const res = await fetch(`/api/job-boards/${params.jobBoardId}/job-posts`);
    const jobPosts = await res.json();

    const safeJobPosts = Array.isArray(jobPosts) ? jobPosts : [];
    return { jobPosts: safeJobPosts };
}

export default function JobPosts({ loaderData }) {
    const { jobBoardId } = useParams();   // <-- Added

    const jobPosts = Array.isArray(loaderData.jobPosts)
        ? loaderData.jobPosts
        : [];

    if (jobPosts.length === 0) {
        return (
            <div style={{ padding: "40px", textAlign: "center", fontFamily: "sans-serif" }}>
                <h1>No job posts yet</h1>
                <p>This board is empty.</p>

                {/* POST A JOB BUTTON */}
                <Link
                    to={`/job-boards/${params.jobBoardId}/post`}
                    style={{
                        display: "inline-block",
                        marginTop: "20px",
                        padding: "10px 20px",
                        background: "#007bff",
                        color: "#fff",
                        borderRadius: "6px",
                        textDecoration: "none"
                    }}
                >
                    Post a Job
                </Link>
            </div>
        );
    }

    return (
        <div style={{ padding: "20px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>

            {/* HEADER WITH POST BUTTON */}
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "25px"
            }}>
                <h1 style={{ fontSize: "32px", margin: 0 }}>Job Posts</h1>

                <Link
                    to={`/job-boards/${jobBoardId}/post`}
                    style={{
                        padding: "10px 20px",
                        background: "#007bff",
                        color: "white",
                        borderRadius: "6px",
                        textDecoration: "none",
                        fontWeight: "bold"
                    }}
                >
                    + Post Job
                </Link>
            </div>

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
