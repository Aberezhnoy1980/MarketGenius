import { useState } from "react";
import TickerSearch from "./TickerSearch";
import styles from "./DashboardPage.module.css";

export default function ForecastForm({
	selectedTicker,
	forecastDays,
	onTickerSelect,
	onDaysChange,
	onSubmit,
}) {
	const [daysOptions] = useState([1, 3, 7, 30, 180, 365]);

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (!selectedTicker) return;
		onSubmit(selectedTicker, forecastDays);
	};

	return (
		<div className={styles.forecastDate}>
			<form onSubmit={handleSubmit}>
				<div className={styles.forecastDateHeader}>
					<label>Выберите акцию и период прогноза</label>
					{selectedTicker && (
						<div className={styles.selectedTickerContainer}>
							<span className={styles.selectedTicker}>
								{selectedTicker}
							</span>
						</div>
					)}
				</div>

				<TickerSearch onSelect={onTickerSelect} />

				<div className={styles.datePickerWrapper}>
					<div className={styles.daysButtons}>
						{daysOptions.map((days) => (
							<button
								key={days}
								type="button"
								className={`${
									forecastDays === days ? styles.active : ""
								}`}
								onClick={() => onDaysChange(days)}>
								{days} д.
							</button>
						))}
					</div>
				</div>

				<div className={styles.forecastCalcContainer}>
					<button
						type="submit"
						className={styles.forecastCalcButton}
						disabled={!selectedTicker}>
						Получить аналитику
					</button>
				</div>
			</form>
		</div>
	);
}
