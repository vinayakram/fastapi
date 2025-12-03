import { Form, useLoaderData, redirect, useNavigation } from "react-router";

import { userContext } from "~/context";



// ---------------------
// LOAD EXISTING BOARD
// ---------------------

export async function clientLoader({ context, params }: ClientLoaderFunctionArgs) {
  // 1️⃣ ADMIN CHECK
  const me = context.get(userContext);
  const isAdmin = me?.is_admin ?? false;

  if (!isAdmin) {
    throw redirect("/admin-login");
  }

  // 2️⃣ FETCH JOB BOARD DETAILS
  const res = await fetch(`/api/job-boards/id/${params.jobBoardId}`);

  if (!res.ok) {
    throw new Response("Board not found", { status: 404 });
  }

  const board = await res.json();

  return { board };
}


// ---------------------
// HANDLE UPDATE
// ---------------------
export async function clientAction({ request, params }) {
    const formData = await request.formData();

    const response = await fetch(`/api/job-boards/${params.jobBoardId}`, {
        method: "PUT",
        body: formData,
    });

    if (!response.ok) {
        const text = await response.text();
        console.error("🔥 PUT ERROR STATUS:", response.status);
        console.error("🔥 PUT ERROR BODY:", text);
        throw new Error("Failed to update job board");
    }

    return redirect("/job-boards");
}


// ---------------------
// REACT COMPONENT
// ---------------------
export default function EditJobBoard() {
    const board = useLoaderData();
    const navigation = useNavigation();

    const isSubmitting = navigation.state === "submitting";

    return (
        <div className="max-w-lg mx-auto mt-10 p-6 bg-white shadow rounded-xl border">
            <h1 className="text-2xl font-semibold mb-6">
                Edit Job Board: {board.slug}
            </h1>

            {/* CURRENT LOGO */}
            <div className="mb-6 text-center">
                <p className="text-sm text-gray-600 mb-2">Current Logo</p>
                <img
                    src={`${board.logo_url}?v=${Date.now()}`}
                    alt="Logo"
                    className="w-28 h-28 object-contain border rounded mx-auto"
                />
            </div>

            <Form method="post" encType="multipart/form-data" className="space-y-5">

                {/* SLUG */}
                <div className="flex flex-col space-y-2">
                    <label className="font-medium">Slug</label>
                    <input
                        name="slug"
                        defaultValue={board.slug}
                        className="border rounded px-3 py-2"
                        required
                        minLength={3}
                        maxLength={20}
                    />
                </div>

                {/* LOGO UPLOAD */}
                <div className="flex flex-col space-y-2">
                    <label className="font-medium">Upload New Logo (optional)</label>
                    <input
                        type="file"
                        name="logo"
                        accept="image/png,image/jpeg"
                        className="border rounded px-3 py-2"
                    />
                </div>

                <button
                    className={`w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded ${
                        isSubmitting ? "opacity-70 cursor-not-allowed" : ""
                    }`}
                    disabled={isSubmitting}
                >
                    {isSubmitting ? "Updating..." : "Update Job Board"}
                </button>
            </Form>
        </div>
    );
}
