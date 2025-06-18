import {
	createContext,
	useContext,
	useState,
	useCallback,
	useEffect,
} from "react";
import { useNavigate } from "react-router-dom";
import client, { checkAuth } from "../api/client";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(null);
	const [isAuthLoading, setIsAuthLoading] = useState(true);
	const [authError, setAuthError] = useState(null);
	const navigate = useNavigate();

	const verifyAuth = useCallback(async () => {
		try {
			setIsAuthLoading(true);
			const { authenticated, user } = await checkAuth();
			if (authenticated) {
				setUser(user);
			} else {
				setUser(null);
			}
		} catch (error) {
			console.error("Auth verification failed:", error);
		} finally {
			setIsAuthLoading(false);
		}
	}, []);

	useEffect(() => {
		verifyAuth();
	}, [verifyAuth]);

	const login = useCallback(
		async (credentials) => {
			setIsAuthLoading(true);
			try {
				const { data } = await client.post("/auth/login", credentials);
				setUser(data.user);
				document.cookie = `mg_access_token=${data.token}; path=/; Secure; SameSite=Strict`;
				navigate("/dashboard");
			} catch (error) {
				setAuthError(
					error.response?.data?.message || "Ошибка авторизации"
				);
				return { success: false };
			} finally {
				setIsAuthLoading(false);
			}
		},
		[navigate]
	);

	const logout = useCallback(async () => {
		try {
			await client.post("/auth/logout");
			document.cookie =
				"mg_access_token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
			setUser(null);
			navigate("/login", { replace: true });
		} catch (error) {
			console.error("Logout error:", error);
		}
	}, [navigate]);

	return (
		<AuthContext.Provider
			value={{
				user,
				isAuthLoading,
        authError,
				login,
				logout,
				isAuthenticated: !!user,
			}}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const context = useContext(AuthContext);
	if (!context) {
		throw new Error("useAuth must be used within AuthProvider");
	}
	return context;
};
