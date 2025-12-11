export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = {
    login: async () => {
        try {
            const res = await fetch(`${API_URL}/auth/mock-login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });
            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Server error: ${res.status} ${text}`);
            }
            return res.json();
        } catch (e) {
            console.error("Login Error:", e);
            throw e;
        }
    },

    get: async (endpoint) => {
        const res = await fetch(`${API_URL}${endpoint}`);
        if (!res.ok) throw new Error("Fetch failed");
        return res.json();
    },

    post: async (endpoint, body) => {
        const res = await fetch(`${API_URL}${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error("Request failed");
        return res.json();
    },

    put: async (endpoint, body) => {
        const res = await fetch(`${API_URL}${endpoint}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error("Request failed");
        return res.json();
    },

    searchUser: async (username) => {
        const res = await fetch(`${API_URL}/users/search?username=${username}`);
        return res.json();
    }
};
