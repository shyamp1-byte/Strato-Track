"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [status, setStatus] = useState("Loading...");

  console.log("ENV BASE:", process.env.NEXT_PUBLIC_API_BASE_URL);
  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_BASE_URL;
    if (!base) {
      setStatus("Missing NEXT_PUBLIC_API_BASE_URL in .env.local");
      return;
    }

    fetch(`${base}/db/ping`, { credentials: "include" })
      .then(async (r) => {
        const data = await r.json().catch(() => ({}));
        setStatus(`${r.status} ${r.ok ? "OK" : "FAIL"} - ${JSON.stringify(data)}`);
      })
      .catch((e) => setStatus(`ERR - ${String(e)}`));
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>StratoTrack Frontend</h1>
      <p>API ping:</p>
      <pre>{status}</pre>
    </main>
  );
}