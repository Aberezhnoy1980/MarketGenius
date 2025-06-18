// Footer.jsx
import styles from "./DashboardPage.module.css";

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContent}>
        <div className={styles.footerSection}>
          <h4>MarketGenius</h4>
          <p>Прогнозирование рынка с использованием ИИ</p>
        </div>
        
        <div className={styles.footerSection}>
          <h4>Контакты</h4>
          <p>market-genius@yandex.ru</p>
          <p>+7 (999) 414-10-41</p>
        </div>
        
        <div className={styles.footerSection}>
          <h4>© 2025 MarketGenius</h4>
          <p>Все права защищены</p>
        </div>
      </div>
    </footer>
  );
}