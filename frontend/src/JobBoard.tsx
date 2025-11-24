import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

export default function JobBoard() {
  const { company } = useParams();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await fetch(`/api/job-boards/${company}`);
        if (!res.ok) throw new Error("Server returned " + res.status);

        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message);
      }
    };

    fetchJobs();
  }, [company]);

  if (error) return <h2 style={{ color: "red" }}>Error: {error}</h2>;
  if (!data) return <h2>Loading...</h2>;

  return (
    <div style={{ padding: 20 }}>
      <h2>Jobs at {data.slug.toUpperCase()}</h2>

      <img
        src={data.logo}
        width="120"
        alt={data.slug}
        style={{ marginBottom: 20 }}
      />

      {data.jobs.map((job: any) => (
        <div key={job.id} style={{ border: "1px solid #ccc", padding: 15, marginBottom: 10 }}>
          <h3>{job.title}</h3>
          <p>{job.description}</p>
        </div>
      ))}
    </div>
  );
}
