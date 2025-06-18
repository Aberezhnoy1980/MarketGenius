import { useTheme } from '../contexts/ThemeContext'
import './ToggleTheme.css'

export default function ToggleThemeButton() {
  const { isLight, toggleTheme } = useTheme()
  
  return (
    <button 
      onClick={toggleTheme}
      className="theme-toggle-button"
      aria-label={isLight ? 'Переключить на тёмную тему' : 'Переключить на светлую тему'}
    >
      <span className={`theme-icon ${isLight ? 'sun' : 'moon'}`}>
        {isLight ? '☀️' : '🌙'}
      </span>
    </button>
  )
}