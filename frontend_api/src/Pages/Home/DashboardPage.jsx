import { useState, useEffect } from "react";
import FavoritesSection from "./FavoritesSection";
import ForecastForm from "./ForecastForm";
import StockChart from "./StockChart";
import AnalyticsTabs from "./AnalyticsTabs";
import NewsSection from "./NewsSection";
import styles from "./DashboardPage.module.css";
import client from "../../api/client";
import MoexNews from "./MoexNews";
import ToggleThemeButton from "../../components/ToggleThemeButton";
import Header from "./Header";
import Footer from "./Footer";
import ProfilePanel from "./ProfileComponent";
import ErrorBoundary from "./ErrorBoundary";

export default function DashboardPage() {
	const [activeTab, setActiveTab] = useState("financial");
	const [selectedTicker, setSelectedTicker] = useState("IMOEX");
	const [forecastDays, setForecastDays] = useState(7);
	const [chartType, setChartType] = useState("candle");
	const [interval, setInterval] = useState("1D");
	const [dashboardData, setDashboardData] = useState(null);
	const [analysisData, setAnalysisData] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [showAnalytics, setShowAnalytics] = useState(false);
	const [moexNews, setMoexNews] = useState([]);
	const [error, setError] = useState(null);
	const [showProfile, setShowProfile] = useState(false);

	useEffect(() => {
		const fetchDashboardData = async () => {
			try {
				setIsLoading(true);
				const { data } = await client.get("/init/dashboard");
				setDashboardData(data);
				setMoexNews(data.moex_news || []);
				setShowAnalytics(false);
				setError(null);
				setSelectedTicker("IMOEX");
				setAnalysisData(null);
			} catch (err) {
				console.error("Error fetching dashboard data:", err);
				setError("Не удалось загрузить данные dashboard");
			} finally {
				setIsLoading(false);
			}
		};

		fetchDashboardData();
	}, []);

	const handleSubmitAnalysis = async (ticker, days) => {
		if (!ticker) {
			setError("Пожалуйста, выберите тикер");
			return;
		}

		try {
			setIsLoading(true);
			setError(null);
			const tickerUpper = ticker.toUpperCase();
			const { data } = await client.get(
				`/analysis/${tickerUpper}/forecast/${days}`
			);

			setAnalysisData({
				...data,
				ticker: tickerUpper,
				forecastDays: days,
			});
			setSelectedTicker(tickerUpper);
			setForecastDays(days);
			setShowAnalytics(true);
			setActiveTab("financial");
		} catch (err) {
			console.error("Error fetching analysis data:", err);
			setError(`Ошибка при получении данных для ${ticker}`);
			setShowAnalytics(false);
		} finally {
			setIsLoading(false);
		}
	};

	const resetToDefault = () => {
		setSelectedTicker("IMOEX");
		setForecastDays(7);
		setAnalysisData(null);
		setShowAnalytics(false);
		setError(null);
	};

	// if (isLoading && !dashboardData) {
	//     return <div className={styles.loading}>Загрузка данных...</div>;
	// }

	return (
		<div style={{ display: "flex", flexDirection: "column" }}>
			{showProfile && (
				<div
					className={styles.profileOverlay}
					onClick={() => setShowProfile(false)}
				/>
			)}

			{/* <Header onProfileClick={() => setShowProfile(true)} /> */}
			<div className={styles.dashboard}>
				<div className={styles.sidebar}>
					<FavoritesSection
						onSelect={setSelectedTicker}
						selectedTicker={selectedTicker}
					/>
					<ForecastForm
						selectedTicker={selectedTicker}
						forecastDays={forecastDays}
						onTickerSelect={setSelectedTicker}
						onDaysChange={setForecastDays}
						onSubmit={handleSubmitAnalysis}
						onReset={resetToDefault}
						error={error}
					/>
				</div>

				<div className={styles.main}>
					<div className={styles.chartControls}>
						<div className={styles.chartTypeToggle}>
							<button
								className={`${styles.chartTypeButton} ${
									chartType === "line" ? styles.active : ""
								}`}
								onClick={() => setChartType("line")}>
								Линия
							</button>
							<button
								className={`${styles.chartTypeButton} ${
									chartType === "candle" ? styles.active : ""
								}`}
								onClick={() => setChartType("candle")}>
								Свечи
							</button>
						</div>
						<div className={styles.intervalSelector}>
							{["1D", "1W", "1M", "6M"].map((int) => (
								<button
									key={int}
									className={`${styles.intervalButton} ${
										interval === int ? styles.active : ""
									}`}
									onClick={() => setInterval(int)}>
									{int}
								</button>
							))}
						</div>
					</div>

					{error && !showAnalytics && (
						<div className={styles.error}>{error}</div>
					)}

					<ErrorBoundary>
						<StockChart
							ticker={selectedTicker}
							days={forecastDays}
							chartType={chartType}
							interval={interval}
							initialData={dashboardData?.chart_data}
							analysisData={analysisData}
							isLoading={isLoading}
						/>
					</ErrorBoundary>

					{showAnalytics ? (
						<AnalyticsTabs
							activeTab={activeTab}
							onChangeTab={setActiveTab}
							analysisData={analysisData}
							ticker={selectedTicker}
							forecastDays={forecastDays}
						/>
					) : (
						<MoexNews news={moexNews} />
					)}
				</div>

				<div className={styles.rightbar}>
					<NewsSection news={dashboardData?.telegram_news} />
				</div>

				{showProfile && (
					<ProfilePanel onClose={() => setShowProfile(false)} />
				)}
			</div>
			{/* <Footer /> */}
		</div>
	);
}
