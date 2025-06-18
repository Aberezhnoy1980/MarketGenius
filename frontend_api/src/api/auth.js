import client from "./client";

export default {
	login: (credentials) => client.post("/auth/login", credentials),
	register: (data) => client.post("/auth/register", data),
	checkAuth: () => client.get("/auth/check-auth"),
	logout: () => client.post("/auth/logout"),
};
