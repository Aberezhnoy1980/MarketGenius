import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import styles from "./AuthForm.module.css";

export default function RegistrationForm() {
	const [isLoading, setIsLoading] = useState(false);
	const [login, setLogin] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [errors, setErrors] = useState({
		login: "",
		email: "",
		password: "",
		confirmPassword: "",
		global: "",
	});
	const { register } = useAuth();
	const navigate = useNavigate();

	const validate = () => {
		const newErrors = {};
		let isValid = true;

		if (!login.trim()) {
			newErrors.login = "Введите никнейм";
			isValid = false;
		}

		if (!email.trim()) {
			newErrors.email = "Введите email";
			isValid = false;
		} else if (!/^\S+@\S+\.\S+$/.test(email)) {
			newErrors.email = "Некорректный email";
			isValid = false;
		}

		if (!password) {
			newErrors.password = "Введите пароль";
			isValid = false;
		} else if (password.length < 8) {
			// Увеличили минимальную длину до 8
			newErrors.password = "Пароль должен содержать минимум 8 символов";
			isValid = false;
		} else if (!/(?=.*\d)(?=.*[a-zA-Z])/.test(password)) {
			newErrors.password = "Пароль должен содержать буквы и цифры";
			isValid = false;
		}

		if (password !== confirmPassword) {
			newErrors.confirmPassword = "Пароли не совпадают";
			isValid = false;
		}

		setErrors(newErrors);
		return isValid;
	};

	// Обновлённый handleSubmit
	const handleSubmit = async (e) => {
		e.preventDefault();
		if (!validate()) return; // Валидация уже обновляет errors

		try {
			setIsLoading(true);
			await register({ login, email, password });
			navigate("/confirm-email");
		} catch (err) {
			let errorMessage = "Ошибка регистрации";

			if (err.response) {
				const backendError = err.response.data.detail;
				if (backendError.includes("Email уже занят")) {
					errorMessage = "Этот email уже используется";
				} else if (backendError.includes("Логин уже занят")) {
					errorMessage = "Этот логин уже занят";
				}
			}

			setErrors({
				...errors,
				global: errorMessage,
			});
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className={styles.authContainer}>
			<p className={styles.title}>Регистрация</p>
			<form onSubmit={handleSubmit}>
				{/* Поле "Никнейм" */}
				<div className={styles.userBox}>
					<input
						className={`${styles.inputField} ${
							errors.login ? styles.errorInput : ""
						}`}
						type="text"
						value={login}
						onChange={(e) => setLogin(e.target.value)}
						required
					/>
					<label className={styles.inputLabel}>Никнейм</label>
					{errors.login && (
						<div className={styles.errorText}>{errors.login}</div>
					)}
				</div>

				{/* Поле "Email" */}
				<div className={styles.userBox}>
					<input
						className={`${styles.inputField} ${
							errors.email ? styles.errorInput : ""
						}`}
						type="email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required
					/>
					<label className={styles.inputLabel}>Email</label>
					{errors.email && (
						<div className={styles.errorText}>{errors.email}</div>
					)}
				</div>

				{/* Поле "Пароль" */}
				<div className={styles.userBox}>
					<input
						className={`${styles.inputField} ${
							errors.password ? styles.errorInput : ""
						}`}
						type="password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>
					<label className={styles.inputLabel}>Пароль</label>
					{errors.password && (
						<div className={styles.errorText}>
							{errors.password}
						</div>
					)}
				</div>

				{/* Поле "Подтвердите пароль" */}
				<div className={styles.userBox}>
					<input
						className={`${styles.inputField} ${
							errors.confirmPassword ? styles.errorInput : ""
						}`}
						type="password"
						value={confirmPassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
						required
					/>
					<label className={styles.inputLabel}>
						Подтвердите пароль
					</label>
					{errors.confirmPassword && (
						<div className={styles.errorText}>
							{errors.confirmPassword}
						</div>
					)}
				</div>

				<div className={styles.errorsContainer}>
					{errors.global && (
						<div className={styles.formError}>
							⚠️ {errors.global}
						</div>
					)}
				</div>

				<button
					type="submit"
					className={styles.submitBtn}
					disabled={isLoading}>
					{isLoading ? (
						<span className={styles.loader}>⏳</span>
					) : (
						"ЗАРЕГИСТРИРОВАТЬСЯ"
					)}
				</button>
			</form>

			{/* Ссылка на авторизацию */}
			<p className={styles.info}>
				Уже есть аккаунт?{" "}
				<a
					href="#"
					onClick={(e) => {
						e.preventDefault();
						navigate("/login");
					}}
					className={styles.link}>
					Войти!
				</a>
			</p>
		</div>
	);
}
