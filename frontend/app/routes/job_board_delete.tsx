import { Form, redirect, useLoaderData } from "react-router";

export async function clientLoader({ params }) {
    const res = await fetch(`/api/job-boards/${params.jobBoardId}`);
    return res.json();
}

export async function clientAction({ params }) {
    await fetch(`/api/job-boards/id/${params.jobBoardId}`, {
        method: "DELETE",
    });

    return redirect("/job-boards");
}

export default function DeleteJobBoard() {
    const board = useLoaderData();

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow rounded-xl border">
            <h1 className="text-2xl mb-4">Delete {board.slug}?</h1>

            <p className="mb-6">Are you sure you want to delete this job board?</p>

            <Form method="post" className="space-y-4">
                <button className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded">
                    Confirm Delete
                </button>
            </Form>
        </div>
    );
}
