document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
  
    const res = await fetch("/api/v1/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
  
    const data = await res.json();
  
    if (res.ok) {
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      window.location.href = "/api/v1/dashboard/";
    } else {
      alert("Login failed. Please check your credentials.");
    }
  });
  