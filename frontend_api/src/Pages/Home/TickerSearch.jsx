import { useState, useEffect, useMemo } from "react";
import { searchTickers } from "../../api/stock";
import styles from "./DashboardPage.module.css";

export default function TickerSearch({ onSelect }) {
	const [query, setQuery] = useState("");
	const [results, setResults] = useState([]);
	const [isDropdownOpen, setIsDropdownOpen] = useState(false);
	const [favorites, setFavorites] = useState([]);

	useEffect(() => {
		const saved = JSON.parse(
			localStorage.getItem("favoriteTickers") || "[]"
		);
		setFavorites(saved);
	}, []);

	const searchResults = useMemo(() => {
		return searchTickers(query);
	}, [query]);

	useEffect(() => {
		setResults(searchResults);
		setIsDropdownOpen(query.length > 1 && searchResults.length > 0);
	}, [searchResults, query]);

	const addToFavorites = (ticker, e) => {
		e.stopPropagation();

		// Проверяем, нет ли уже такого тикера в избранном
		const alreadyExists = favorites.some(
			(fav) => fav.symbol === ticker.symbol && fav.name === ticker.name
		);

		if (!alreadyExists) {
			const updated = [...favorites, ticker];
			setFavorites(updated);
			localStorage.setItem("favoriteTickers", JSON.stringify(updated));
		}
	};

	const isFavorite = (symbol) => {
		return favorites.some((fav) => fav.symbol === symbol);
	};

	const handleSelect = (ticker) => {
		onSelect(ticker.symbol);
		setQuery(""); // Очищаем поле ввода
		setIsDropdownOpen(false); // Закрываем дропдаун
	};

	return (
		<div className={styles.searchContainer}>
			<input
				value={query}
				onChange={(e) => setQuery(e.target.value.trim())}
				placeholder="Поиск акций..."
				className={styles.searchInput}
				onFocus={() => query.length > 1 && setIsDropdownOpen(true)}
			/>

			{isDropdownOpen && (
				<ul className={styles.dropdown}>
					{results.map((ticker) => (
						<li
							key={ticker.symbol}
							onClick={() => handleSelect(ticker)} // Используем новую функцию
						>
							<span className={styles.tickerSymbol}>
								{ticker.symbol}
							</span>
							<span className={styles.tickerName}>
								{ticker.name}
							</span>
							<button
								onClick={(e) => addToFavorites(ticker, e)}
								className={`${styles.starButton} ${
									isFavorite(ticker.symbol)
										? styles.favorited
										: ""
								}`}>
								{isFavorite(ticker.symbol) ? "★" : "☆"}
							</button>
						</li>
					))}
				</ul>
			)}
		</div>
	);
}

