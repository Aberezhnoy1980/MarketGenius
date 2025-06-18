import axios from "axios";

const client = axios.create({
	baseURL: "http://localhost:8000",
	timeout: 30000, // Увеличиваем таймаут для тяжелых запросов
	withCredentials: true,
	headers: {
		"Content-Type": "application/json",
	},
});

// Добавляем интерсептор для обработки ошибок
client.interceptors.response.use(
    (response) => {
        // Проверяем структуру ответа для графиков
        if (response.config.url.includes('/analysis') && response.data?.ohlc) {
            if (!Array.isArray(response.data.ohlc)) {
                throw new Error("Некорректный формат данных графика");
            }
        }
        return response;
    },
    (error) => {
        if (error.response) {
            // Обработка HTTP ошибок
            error.message = `Ошибка ${error.response.status}: ${error.response.data?.message || error.message}`;
        } else if (error.request) {
            // Ошибки без ответа от сервера
            error.message = "Сервер не отвечает, попробуйте позже";
        }
        return Promise.reject(error);
    }
);

// Флаг для избежания рекурсии
let isRefreshing = false;

// Получение токена из cookies
const getTokenFromCookies = () => {
	return document.cookie
		.split("; ")
		.find((row) => row.startsWith("mg_access_token="))
		?.split("=")[1];
};

// Интерцептор запросов
client.interceptors.request.use((config) => {
	if (config.url.includes("/auth/")) return config;

	const token = getTokenFromCookies();
	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

// Интерцептор ответов
client.interceptors.response.use(
	(response) => response,
	async (error) => {
		const originalRequest = error.config;

		if (error.response?.status === 401 && !isRefreshing) {
			isRefreshing = true;

			try {
				await client.post("/auth/refresh-token");
				return client(originalRequest);
			} catch (refreshError) {
				console.error("Refresh token failed:", refreshError);
				window.location.href = "/login";
			} finally {
				isRefreshing = false;
			}
		}

		return Promise.reject(error);
	}
);

export const checkAuth = async () => {
	try {
		const { data } = await client.get("/auth/check-auth");
		return {
			authenticated: data?.authenticated || false,
			user: data?.user || null,
		};
	} catch (error) {
		console.error("Auth check failed:", error);
		return {
			authenticated: false,
			user: null,
		};
	}
};

export default client;
