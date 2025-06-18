import { createContext, useContext, useState, useEffect } from "react";

// 1. Создаём контекст
const ThemeContext = createContext();

// 2. Создаём провайдер
export function ThemeProvider({ children }) {
	const [isLight, setIsLight] = useState(() => {
		const saved = localStorage.getItem("theme");
		return saved ? saved === "light" : true;
	});

	useEffect(() => {
		const theme = isLight ? "light" : "dark";
		document.documentElement.setAttribute("data-theme", theme);
		localStorage.setItem("theme", theme);

		document.documentElement.style.setProperty(
			"--chart-background",
			isLight ? "#ffffff" : "#2a2a3c"
		);
	}, [isLight]);

	const toggleTheme = () => setIsLight(!isLight);

	return (
		<ThemeContext.Provider value={{ isLight, toggleTheme }}>
			{children}
		</ThemeContext.Provider>
	);
}

// 3. Создаём хук для использования
export function useTheme() {
	const context = useContext(ThemeContext);
	if (!context) {
		throw new Error("useTheme must be used within ThemeProvider");
	}
	return {
		isLight: context.isLight,
		toggleTheme: context.toggleTheme,
	};
}

// 4. Экспортируем сам контекст для случаев, когда хук useTheme не подходит
export { ThemeContext };
