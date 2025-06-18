import { MOEX_TICKERS } from '../data/tickers';

export const searchTickers = (query) => {
  if (!query || query.length < 2) return [];
  
  const queryLower = query.toLowerCase();
  
  return MOEX_TICKERS.filter(ticker => 
    ticker.symbol.toLowerCase().includes(queryLower) || 
    ticker.name.toLowerCase().includes(queryLower)
  ).slice(0, 20); // Ограничиваем результаты
};