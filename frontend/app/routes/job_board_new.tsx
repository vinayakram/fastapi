import { Form, redirect, useActionData } from "react-router";
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

export async function clientAction({ request }) {
    const formData = await request.formData();

    const res = await fetch("/api/job-boards", {
        method: "POST",
        body: formData,
    });

    if (res.ok) {
        return { success: true };
		
    }

    return { success: false };
	
}

export default function NewJobBoard() {
    const actionData = useActionData();
    const [fileName, setFileName] = useState("");

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-xl border">
            <h1 className="text-2xl font-semibold mb-6">Create Job Board</h1>

            {actionData?.success && (
                <div className="p-3 mb-4 bg-green-100 border border-green-400 text-green-700 rounded">
                    Job board created successfully!
                </div>
            )}

            <Form method="post" encType="multipart/form-data" className="space-y-6">

                {/* Slug Input */}
                <div className="flex flex-col space-y-2">
                    <label className="font-medium">Slug</label>
                    <input
                        name="slug"
                        type="text"
                        required
                        className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
                        placeholder="example: google"
                    />
                </div>

                {/* Logo Upload (as Button) */}
                <div className="flex flex-col space-y-2">
                    <label className="font-medium">Logo</label>

                    <input
                        id="logo-input"
                        type="file"
                        name="logo"
                        required
                        className="hidden"
                        onChange={(e) => {
                            if (e.target.files?.length) {
                                setFileName(e.target.files[0].name);
                            }
                        }}
                    />

                    <button
                        type="button"
                        onClick={() => document.getElementById("logo-input")?.click()}
                        className="px-4 py-2 bg-gray-100 hover:bg-gray-200 border rounded-lg text-sm text-gray-700 w-fit"
                    >
                        Choose Logo
                    </button>

                    {fileName && (
                        <p className="text-sm text-gray-600">
                            Selected: <strong>{fileName}</strong>
                        </p>
                    )}
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg font-medium"
                >
                    Create Job Board
                </button>

            </Form>
        </div>
    );
}
