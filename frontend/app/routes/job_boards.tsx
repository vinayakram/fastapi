import { Link } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Button } from "~/components/ui/button";

export async function clientLoader() {
    const res = await fetch("/api/job-boards");
    const job_boards = await res.json();
    return { job_boards };
}

export default function JobBoards({ loaderData }) {
    return (
        <div style={{ padding: "20px", fontFamily: "sans-serif" }}>

            {/* HEADER */}
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-semibold">Job Boards</h1>

                <Button asChild>
                    <Link to="/job-boards/new">Add New Job Board</Link>
                </Button>
            </div>

            {/* Job Board Cards */}
            <div
                style={{
                    display: "grid",
                    gap: "20px",
                    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
                }}
            >
                {loaderData.job_boards.map((board) => (
                    <div
                        key={board.id}
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "16px",
                            background: "#fff",
                            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                        }}
                    >
                        {/* Board content */}
                        <Link
                            to={`/job-boards/${board.id}/job-posts`}
                            style={{ textDecoration: "none", color: "inherit" }}
                        >
                            <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                                {board.logo_url ? (
                                    <Avatar className="w-[60px] h-[60px] rounded-md overflow-hidden bg-white">
                                        <AvatarImage
                                            src={board.logo_url}
                                            alt={board.slug}
                                            style={{
                                                width: "60px",
                                                height: "60px",
                                                objectFit: "contain",
                                                borderRadius: "15px",
                                            }}
                                        />
                                    </Avatar>
                                ) : (
                                    <div
                                        style={{
                                            width: "60px",
                                            height: "60px",
                                            background: "#f0f0f0",
                                            border: "2px dashed #aaa",
                                            borderRadius: "8px",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center",
                                            fontSize: "12px",
                                            color: "#888",
                                        }}
                                    >
                                        No logo
                                    </div>
                                )}

                                <div>
                                    <div style={{ fontSize: "18px", fontWeight: "bold", textTransform: "capitalize" }}>
                                        {board.slug}
                                    </div>
                                    <div style={{ fontSize: "12px", color: "#666" }}>
                                        ID: {board.id}
                                    </div>
                                </div>
                            </div>
                        </Link>

                        {/* ⭐ Edit/Delete buttons under card */}
                        <div className="flex justify-end gap-3 mt-4">
                            <Button asChild variant="outline" size="sm">
                                <Link to={`/job-boards/${board.id}/edit`}>Edit</Link>
                            </Button>

                            <Button asChild variant="destructive" size="sm">
                                <Link to={`/job-boards/${board.id}/delete`}>Delete</Link>
                            </Button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
