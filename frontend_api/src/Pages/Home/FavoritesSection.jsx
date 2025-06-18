// import { useState, useEffect } from "react";
// import styles from "./DashboardPage.module.css";

// export default function FavoritesSection({ onSelect, selectedTicker }) {
//   const [favorites, setFavorites] = useState([]);

//   useEffect(() => {
//     const saved = JSON.parse(
//       localStorage.getItem("favoriteTickers") || "[]"
//     );
//     // Удаляем дубликаты перед установкой состояния
//     const uniqueFavorites = Array.from(new Set(saved.map(JSON.stringify)))
//       .map(JSON.parse);
//     setFavorites(uniqueFavorites);
//   }, []);

//   const handleSelect = (ticker) => {
//     onSelect(ticker);
//   };

//   const removeFavorite = (ticker, e) => {
//     e.stopPropagation();
//     const updated = favorites.filter((fav) => fav.symbol !== ticker.symbol);
//     setFavorites(updated);
//     localStorage.setItem("favoriteTickers", JSON.stringify(updated));
//   };

//   return (
//     <div className={styles.favorites}>
//       <div className={styles.favoritesHeader}>
//         <span className={styles.favoritesTitle}>Избранные акции</span>
//       </div>
//       <div className={styles.favoritesList}>
//         {favorites.length > 0 ? (
//           favorites.map((ticker) => (
//             <div
//               key={`${ticker.symbol}-${ticker.name}`} // Уникальный ключ
//               className={`${styles.favoriteStock} ${
//                 selectedTicker === ticker.symbol ? styles.active : ""
//               }`}
//               onClick={() => handleSelect(ticker.symbol)}
//             >
//               <span>
//                 {ticker.name} ({ticker.symbol})
//               </span>
//               <button
//                 onClick={(e) => removeFavorite(ticker, e)}
//                 className={styles.starButton}
//               >
//                 ★
//               </button>
//             </div>
//           ))
//         ) : (
//           <div className={styles.emptyFavorites}>Нет избранных акций</div>
//         )}
//       </div>
//     </div>
//   );
// }

import { useState, useEffect } from "react";
import styles from "./DashboardPage.module.css";

export default function FavoritesSection({ onSelect, selectedTicker }) {
	const [favorites, setFavorites] = useState([]);

	useEffect(() => {
		const saved = JSON.parse(
			localStorage.getItem("favoriteTickers") || "[]"
		);
		setFavorites(saved);
	}, []);

	const handleSelectFavorite = (ticker) => {
		onSelect(ticker.symbol); // Передаем только символ тикера
	};

	const removeFavorite = (ticker, e) => {
		e.stopPropagation();
		const updated = favorites.filter((fav) => fav.symbol !== ticker.symbol);
		setFavorites(updated);
		localStorage.setItem("favoriteTickers", JSON.stringify(updated));
	};

	return (
		<div className={styles.favorites}>
			<div className={styles.favoritesHeader}>
				<span className={styles.favoritesTitle}>Быстрый выбор</span>
			</div>
			<div className={styles.favoritesList}>
				{favorites.length > 0 ? (
					favorites.map((ticker) => (
						<div
							key={`${ticker.symbol}-${ticker.name}`}
							className={`${styles.favoriteStock} ${
								selectedTicker === ticker.symbol
									? styles.active
									: ""
							}`}
							onClick={() => handleSelectFavorite(ticker)}>
							<span>
								{ticker.symbol} - {ticker.name}
							</span>
							<button
								onClick={(e) => removeFavorite(ticker, e)}
								className={styles.starButton}>
								★
							</button>
						</div>
					))
				) : (
					<div className={styles.emptyFavorites}>
						Нет избранных акций
					</div>
				)}
			</div>
		</div>
	);
}
