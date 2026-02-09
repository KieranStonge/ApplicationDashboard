import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function App() {
  const [applications, setApplications] = useState([]);
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    async function load() {
      const appsRes = await fetch(`${API}/applications`);
      const sumRes = await fetch(`${API}/summary`);
      setApplications(await appsRes.json());
      setSummary(await sumRes.json());
    }
    load();
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "Arial, sans-serif" }}>
      <h1>Application Dashboard</h1>

      <h2>Applications</h2>
      <table
        style={{ borderCollapse: "collapse", width: "100%", maxWidth: 900 }}
      >
        <thead>
          <tr>
            <th style={th}>Company</th>
            <th style={th}>Role</th>
            <th style={th}>Stage</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((a) => (
            <tr key={a.id}>
              <td style={td}>{a.company}</td>
              <td style={td}>{a.role}</td>
              <td style={td}>{a.stage}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 style={{ marginTop: 24 }}>Stage Summary</h2>
      <ul>
        {summary.map((s) => (
          <li key={s.stage}>
            {s.stage}: {s.count}
          </li>
        ))}
      </ul>
    </div>
  );
}

const th = {
  border: "1px solid #ccc",
  padding: 8,
  textAlign: "left",
  background: "#f2f2f2",
};
const td = { border: "1px solid #ccc", padding: 8 };
