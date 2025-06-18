import { useState } from "react";
import styles from "./DashboardPage.module.css";

export default function NewsSection({ news }) {
	const [expanded, setExpanded] = useState({
		daily: true,
		sentiment: true,
	});

	if (!news) {
		return <div className={styles.newsLoading}>Загрузка новостей...</div>;
	}

	const formatNewsText = (text) => {
		// Обрезаем текст после "📊 Топ оценок:" или любой другой иконки с этим текстом
		const textBeforeRatings = text.split(/📊 Топ оценок:|📊 Топ оценок/)[0];

		// Разбиваем на строки и обрабатываем каждую
		return textBeforeRatings
			.split("\n")
			.map((line, i, arr) => {
				if (!line.trim()) return null;

				// Первые две строки (заголовок) оставляем как есть
				if (i < 2) {
					return (
						<div key={`line-${i}`} className={styles.newsLine}>
							<span className={styles.lineText}>{line}</span>
						</div>
					);
				}

				// Для остальных строк проверяем наличие иконки в начале
				const iconMatch = line.match(/^([🔹⚠▶✓■•→])/);
				if (iconMatch) {
					const [icon] = iconMatch;
					return (
						<div key={`line-${i}`} className={styles.newsLine}>
							<span className={styles.lineIcon}>{icon}</span>
							<span className={styles.lineText}>
								{line.substring(icon.length).trim()}
							</span>
						</div>
					);
				}

				// Если нет иконки, но строка не пустая
				return (
					<div key={`line-${i}`} className={styles.newsLine}>
						<span className={styles.lineText}>{line}</span>
					</div>
				);
			})
			.filter(Boolean); // Удаляем пустые элементы
	};

	return (
		<div className={styles.newsContainer}>
			<div className={styles.newsBlock}>
				<div
					className={styles.newsHeader}
					onClick={() =>
						setExpanded((prev) => ({ ...prev, daily: !prev.daily }))
					}>
					<h3 className={styles.newsTitle}>Ежедневный обзор</h3>
					<span className={styles.expandIcon}>
						{expanded.daily ? "−" : "+"}
					</span>
				</div>
				{expanded.daily && (
					<div className={styles.newsContent}>
						{formatNewsText(news.daily_summary.content)}
					</div>
				)}
				<div className={styles.newsFooter}>
					<a
						href="https://t.me/marketgenius_blog"
						target="_blank"
						rel="noopener noreferrer"
						className={styles.telegramLink}>
						<svg
							className={styles.telegramIcon}
							viewBox="0 0 24 24">
							<path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z" />
						</svg>
						Перейти в Telegram
					</a>
					<span className={styles.newsDate}>
						{new Date(news.daily_summary.date).toLocaleString(
							"ru-RU"
						)}
					</span>
				</div>
			</div>

			<div className={styles.newsBlock}>
				<div
					className={styles.newsHeader}
					onClick={() =>
						setExpanded((prev) => ({
							...prev,
							sentiment: !prev.sentiment,
						}))
					}>
					<h3 className={styles.newsTitle}>Анализ настроений</h3>
					<span className={styles.expandIcon}>
						{expanded.sentiment ? "−" : "+"}
					</span>
				</div>
				{expanded.sentiment && (
					<div className={styles.newsContent}>
						{formatNewsText(news.sentiment_analysis.content)}
					</div>
				)}
				<div className={styles.newsFooter}>
					<a
						href="https://t.me/marketgenius_blog"
						target="_blank"
						rel="noopener noreferrer"
						className={styles.telegramLink}>
						<svg
							className={styles.telegramIcon}
							viewBox="0 0 24 24">
							<path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z" />
						</svg>
						Перейти в Telegram
					</a>
					<span className={styles.newsDate}>
						{new Date(news.sentiment_analysis.date).toLocaleString(
							"ru-RU"
						)}
					</span>
				</div>
			</div>
		</div>
	);
}
