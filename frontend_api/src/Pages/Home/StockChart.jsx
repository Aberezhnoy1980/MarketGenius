import { useEffect, useRef } from "react";
import { createChart, ColorType } from "lightweight-charts";
import styles from "./DashboardPage.module.css";
import { useTheme } from "../../contexts/ThemeContext"; // Импортируем хук темы

export default function StockChart({ ticker, chartType, initialData, analysisData }) {
  const chartContainerRef = useRef(null);
  const chartInstanceRef = useRef(null);
  const seriesRef = useRef(null);
  const { isLight } = useTheme(); // Получаем текущую тему

  // Цвета для тем
  const colors = {
    light: {
      bgColor: "#ffffff",
      textColor: "#333333",
      gridColor: "#eeeeee",
      upColor: "#26a69a",
      downColor: "#ef5350",
      lineColor: "#26a69a",
      forecastColor: "#5d78ff"
    },
    dark: {
      bgColor: "#2a2a3c",
      textColor: "#ffffff",
      gridColor: "#3a3a4c",
      upColor: "rgba(38, 166, 154, 0.8)",
      downColor: "rgba(239, 83, 80, 0.8)",
      lineColor: "rgba(38, 166, 154, 0.8)",
      forecastColor: "rgba(93, 120, 255, 0.8)"
    }
  };

  // Инициализация и обновление графика
  useEffect(() => {
    if (!chartContainerRef.current) return;

    const currentColors = isLight ? colors.light : colors.dark;

    // 1. Подготовка данных (остаётся без изменений)
    const prepareData = (data) => {
      if (!data || !Array.isArray(data)) return [];
      
      return data
        .map(item => ({
          time: (item.date || item.time || '').split('T')[0],
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
          ...(item.isForecast && { 
            color: currentColors.forecastColor,
            borderColor: currentColors.forecastColor,
            wickColor: currentColors.forecastColor
          })
        }))
        .filter(item => item.time && 
          item.open !== undefined && 
          item.high !== undefined && 
          item.low !== undefined && 
          item.close !== undefined)
        .sort((a, b) => new Date(a.time) - new Date(b.time));
    };

    // 2. Получение данных для отображения (остаётся без изменений)
    let displayData = [];
    let forecastMarker = null;

    if (analysisData?.ohlc) {
      displayData = prepareData(analysisData.ohlc);
      
      if (analysisData.forecast) {
        const forecastTime = (analysisData.forecast.date || '').split('T')[0];
        if (forecastTime) {
          const forecastPoint = {
            time: forecastTime,
            open: analysisData.forecast.value,
            high: analysisData.forecast.value,
            low: analysisData.forecast.value,
            close: analysisData.forecast.value,
            isForecast: true
          };
          displayData.push(forecastPoint);
          
          forecastMarker = {
            time: forecastPoint.time,
            position: "belowBar",
            color: currentColors.forecastColor,
            shape: "arrowUp",
            text: `Прогноз: ${analysisData.forecast.value.toFixed(2)}`
          };
        }
      }
    } else if (initialData) {
      displayData = prepareData(initialData);
    }

    // 3. Инициализация графика с учётом темы
    if (!chartInstanceRef.current) {
      chartInstanceRef.current = createChart(chartContainerRef.current, {
        layout: {
          background: { type: ColorType.Solid, color: currentColors.bgColor },
          textColor: currentColors.textColor,
        },
        grid: {
          vertLines: { color: currentColors.gridColor },
          horzLines: { color: currentColors.gridColor },
        },
        width: chartContainerRef.current.clientWidth,
        height: 400,
      });
    }

    // 4. Обновление цветов графика при смене темы
    chartInstanceRef.current.applyOptions({
      layout: {
        background: { type: ColorType.Solid, color: currentColors.bgColor },
        textColor: currentColors.textColor,
      },
      grid: {
        vertLines: { color: currentColors.gridColor },
        horzLines: { color: currentColors.gridColor },
      },
    });

    // 5. Создание/обновление серии с учётом темы
    const createNewSeries = () => {
      if (seriesRef.current) {
        try {
          chartInstanceRef.current.removeSeries(seriesRef.current);
        } catch (e) {
          console.warn("Error removing old series:", e);
        }
      }

      seriesRef.current = chartType === "candle"
        ? chartInstanceRef.current.addCandlestickSeries({
            upColor: currentColors.upColor,
            downColor: currentColors.downColor,
            borderVisible: false,
            wickUpColor: currentColors.upColor,
            wickDownColor: currentColors.downColor,
          })
        : chartInstanceRef.current.addLineSeries({
            color: currentColors.lineColor,
            lineWidth: 2,
          });
    };

    if (!seriesRef.current || 
        (chartType === 'candle' && !('setData' in seriesRef.current)) ||
        (chartType === 'line' && !('setData' in seriesRef.current))) {
      createNewSeries();
    }

    // 6. Установка данных (без изменений)
    if (seriesRef.current && displayData.length > 0) {
      try {
        seriesRef.current.setData(displayData);
        if (forecastMarker) {
          seriesRef.current.setMarkers([forecastMarker]);
        }
        chartInstanceRef.current.timeScale().fitContent();
      } catch (e) {
        console.error("Error setting chart data:", e);
      }
    }

    // 7. Обработка ресайза (без изменений)
    const handleResize = () => {
      if (chartInstanceRef.current && chartContainerRef.current) {
        chartInstanceRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
      if (chartInstanceRef.current) {
        try {
          chartInstanceRef.current.remove();
        } catch (e) {
          console.warn("Error removing chart:", e);
        }
        chartInstanceRef.current = null;
        seriesRef.current = null;
      }
    };
  }, [ticker, chartType, initialData, analysisData, isLight]); // Добавляем isLight в зависимости

  if (!ticker) {
    return <div className={styles.chartHint}>Выберите тикер для отображения данных</div>;
  }

  return (
    <div className={styles.chartContainer}>
      <div ref={chartContainerRef} className={styles.chart} />
    </div>
  );
}