import { Routes, Route, Link } from "react-router-dom";
import JobBoard from "./JobBoard";

export default function App() {
  return (
    <div style={{ padding: 20 }}>
      <h1>React + FastAPI Job Boards</h1>

      <ul>
        <li><Link to="/job/acme">ACME Jobs</Link></li>
        <li><Link to="/job/pcg">PCG Jobs</Link></li>
        <li><Link to="/job/atlas">ATLAS Jobs</Link></li>
      </ul>

      <Routes>
        <Route path="/job/:company" element={<JobBoard />} />
      </Routes>
    </div>
  );
}
