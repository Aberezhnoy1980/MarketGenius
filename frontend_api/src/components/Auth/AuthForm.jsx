import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import styles from "./AuthForm.module.css";

export default function AuthForm() {
	const [loginInput, setLoginInput] = useState("");
	const [passwordInput, setPasswordInput] = useState("");
	const [errors, setErrors] = useState({
		login: "",
		password: "",
		global: "",
	});
	const [isLoading, setIsLoading] = useState(false);
	const { login } = useAuth();
	const navigate = useNavigate();
	const { user } = useAuth();

	useEffect(() => {
		if (user) {
			navigate("/dashboard"); // Редирект если уже авторизован
		}
	}, [user, navigate]);

	const validate = () => {
		const newErrors = {};
		let isValid = true;

		if (!loginInput.trim()) {
			newErrors.login = "Введите логин";
			isValid = false;
		}

		if (!passwordInput) {
			newErrors.password = "Введите пароль";
			isValid = false;
		} else if (passwordInput.length < 6) {
			newErrors.password = "Пароль слишком короткий";
			isValid = false;
		}

		setErrors(newErrors);
		return isValid;
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (!validate()) return;

		try {
			setIsLoading(true);
			const result = await login({
				login: loginInput,
				password: passwordInput,
			});

			if (!result.success) {
				setErrors({
					global: result.error || "Ошибка авторизации",
					login: "",
					password: "",
				});
			} else {
				navigate("/dashboard");
			}
		} catch (err) {
			setErrors({
				global: "Сервер недоступен",
				login: "",
				password: "",
			});
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className={styles.authContainer}>
			<p className={styles.title}>Авторизация</p>
			<form onSubmit={handleSubmit}>
				<div className={styles.userBox}>
					<input
						type="text"
						name="login"
						className={`${styles.inputField} ${
							errors.login ? styles.errorInput : ""
						}`}
						value={loginInput}
						onChange={(e) => setLoginInput(e.target.value)}
						required
					/>
					<label className={styles.inputLabel}>Никнейм</label>
					{errors.login && (
						<div className={styles.errorText}>{errors.login}</div>
					)}
				</div>

				<div className={styles.userBox}>
					<input
						type="password"
						name="password"
						className={`${styles.inputField} ${
							errors.password ? styles.errorInput : ""
						}`}
						value={passwordInput}
						onChange={(e) => setPasswordInput(e.target.value)}
						required
					/>
					<label className={styles.inputLabel}>Пароль</label>
					{errors.password && (
						<div className={styles.errorText}>
							{errors.password}
						</div>
					)}
				</div>

				{/* Глобальная ошибка */}
				{errors.global && (
					<div className={styles.globalError}>{errors.global}</div>
				)}

				<button
					type="submit"
					className={styles.submitBtn}
					disabled={isLoading}>
					{isLoading ? (
						<span className={styles.loader}>⏳</span>
					) : (
						"Войти"
					)}
				</button>
			</form>
			<p className={styles.info}>
				Нет аккаунта?{" "}
				<a href="/register" className={styles.link}>
					Зарегистрироваться!
				</a>
			</p>
		</div>
	);
}
