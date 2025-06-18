// Header.jsx
import { useAuth } from "../../contexts/AuthContext";
import ToggleThemeButton from "../../components/ToggleThemeButton";
import styles from "./DashboardPage.module.css";

export default function Header({ onProfileClick }) {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        {/* <span className={styles.logoIcon}>📊</span> */}
        MarketGenius
      </div>

      <nav className={styles.nav}>
        <button
          className={styles.navIcon}
          title="Помощь"
          onClick={() => console.log("Help clicked")}
        >
          <svg viewBox="0 0 24 24" className={styles.icon}>
            <path
              fill="currentColor"
              d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"
            />
          </svg>
        </button>

        <ToggleThemeButton className={styles.themeToggle} />

        <button
          className={styles.navIcon}
          title="Профиль"
          onClick={onProfileClick}
        >
          <svg viewBox="0 0 24 24" className={styles.icon}>
            <path
              fill="currentColor"
              d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
            />
          </svg>
        </button>
      </nav>
    </header>
  );
}