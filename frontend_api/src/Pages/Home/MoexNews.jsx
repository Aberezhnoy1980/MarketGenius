import { useState } from "react";
import styles from "./DashboardPage.module.css";

export default function MoexNews({ news }) {
	const [visibleCount, setVisibleCount] = useState(5); // Начальное количество новостей

	// Функция для декодирования HTML-сущностей
	const decodeHtml = (html) => {
		const txt = document.createElement("textarea");
		txt.innerHTML = html;
		return txt.value;
	};

	return (
		<div className={styles.moexNewsContainer}>
			<h3 className={styles.moexNewsTitle}>Новости биржи</h3>
			<ul className={styles.moexNewsList}>
				{news.slice(0, visibleCount).map((item) => (
					<li key={item.id} className={styles.moexNewsItem}>
						<span>{decodeHtml(item.title)}</span>
						<a
							href={item.url}
							target="_blank"
							rel="noopener noreferrer"
							className={styles.newsLinkIcon}
							title="Читать на сайте MOEX">
							<svg viewBox="0 0 24 24" width="16" height="16">
								<path
									fill="currentColor"
									d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M11,7V9H13V7H11M11,11V17H13V11H11Z"
								/>
							</svg>
						</a>
					</li>
				))}
			</ul>
			{news.length > visibleCount && (
				<button
					className={styles.showMoreButton}
					onClick={() => setVisibleCount((prev) => prev + 5)}>
					Показать еще
				</button>
			)}
		</div>
	);
}
