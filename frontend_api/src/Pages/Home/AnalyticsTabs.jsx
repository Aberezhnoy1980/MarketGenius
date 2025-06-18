import styles from "./DashboardPage.module.css";

export default function AnalyticsTabs({
    activeTab,
    onChangeTab,
    analysisData,
    ticker,
    forecastDays,
}) {
    const tabs = [
        { id: "financial", label: "Финансовые показатели" },
        { id: "technical", label: "Технические индикаторы" },
        { id: "macro", label: "Макро показатели" },
        { id: "media", label: "Media Scoring" },
    ];

    const renderValue = (value) => {
        if (value === null || value === undefined) return "Н/Д";
        if (typeof value === "number") return value.toFixed(2);
        return value;
    };

    return (
        <div className={styles.tabsContainer}>
            <div className={styles.tabsHeader}>
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        className={`${styles.tabButton} ${
                            activeTab === tab.id ? styles.activeTab : ""
                        }`}
                        onClick={() => onChangeTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            
            <div className={styles.tabContent}>
                <div className={styles.analysisHeader}>
                    <h3>Анализ для {ticker}</h3>
                    <span>Прогноз на {forecastDays} дней</span>
                </div>
                
                {activeTab === "financial" && (
                    <div className={styles.analysisSection}>
                        <h4>Финансовые показатели</h4>
                        <div className={styles.analysisGrid}>
                            {Object.entries(analysisData.factors.financial).map(([key, value]) => (
                                <div key={key} className={styles.analysisItem}>
                                    <span className={styles.analysisLabel}>{key}:</span>
                                    <span className={styles.analysisValue}>{renderValue(value)}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                
                {activeTab === "technical" && (
                    <div className={styles.analysisSection}>
                        <h4>Технические индикаторы</h4>
                        <div className={styles.analysisGrid}>
                            {Object.entries(analysisData.factors.technical).map(([key, value]) => (
                                <div key={key} className={styles.analysisItem}>
                                    <span className={styles.analysisLabel}>{key}:</span>
                                    <span className={styles.analysisValue}>{renderValue(value)}</span>
                                </div>
                            ))}
                        </div>
                        
                        <h4>Метрики модели</h4>
                        <div className={styles.analysisGrid}>
                            {Object.entries(analysisData.metrics).flatMap(([category, metrics]) => 
                                Object.entries(metrics).map(([key, value]) => (
                                    <div key={`${category}-${key}`} className={styles.analysisItem}>
                                        <span className={styles.analysisLabel}>{key}:</span>
                                        <span className={styles.analysisValue}>{renderValue(value)}</span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                )}
                
                {activeTab === "macro" && (
                    <div className={styles.analysisSection}>
                        <h4>Макроэкономические показатели</h4>
                        <div className={styles.analysisGrid}>
                            {Object.entries(analysisData.factors.macro).map(([key, value]) => (
                                <div key={key} className={styles.analysisItem}>
                                    <span className={styles.analysisLabel}>{key}:</span>
                                    <span className={styles.analysisValue}>{renderValue(value)}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                
                {activeTab === "media" && (
                    <div className={styles.analysisSection}>
                        <h4>Media Scoring</h4>
                        <p>Анализ настроений в медиа временно недоступен</p>
                    </div>
                )}
                
                {analysisData.forecast && (
                    <div className={styles.forecastSummary}>
                        <h4>Прогноз</h4>
                        <div className={styles.forecastValue}>
                            Цена через {forecastDays} дней: {analysisData.forecast.value.toFixed(2)}
                            {analysisData.forecast.deviation !== undefined && (
                                <span className={analysisData.forecast.deviation >= 0 ? styles.positive : styles.negative}>
                                    ({analysisData.forecast.deviation >= 0 ? '+' : ''}{analysisData.forecast.deviation.toFixed(2)}%)
                                </span>
                            )}
                        </div>
                        <div className={styles.forecastNote}>
                            Последняя цена закрытия: {analysisData.forecast.last_close.toFixed(2)}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}