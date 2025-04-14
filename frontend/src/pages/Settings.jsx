import React, { useEffect, useState } from "react";

export default function Settings() {
  const [content, setContent] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/settings/", {
      method: "GET",
      credentials: "include", // assuming we are using session-based auth? need to pass in userid
    })
      .then((res) => {
        if (!res.ok) throw new Error("Fetch failed");
        return res.json();
      })
      .then((data) => {
        setContent(data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return <h1>{content}</h1>;
}
