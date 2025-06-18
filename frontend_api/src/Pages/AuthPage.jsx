import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import AuthForm from "../components/auth/AuthForm";
import ToggleThemeButton from "../components/ToggleThemeButton";
import styles from "./AuthPage.module.css";

export default function AuthPage() {
	const navigate = useNavigate();
	const { login } = useAuth();
	const [isLogin, setIsLogin] = useState(true);
	const [error, setError] = useState("");

	const handleLogin = async (credentials) => {
		try {
			await login(credentials);
			navigate("/dashboard");
		} catch (err) {
			setError("Ошибка авторизации");
		}
	};

	return (
		<div className={styles.pageContainer}>
			<div className={styles.formWrapper}>
			<ToggleThemeButton />
				{isLogin ? (
					<AuthForm onSwitchToRegister={() => setIsLogin(false)} />
				) : (
					<RegistrationForm onSwitchToAuth={() => setIsLogin(true)} />
				)}
			</div>
		</div>
	);
}
