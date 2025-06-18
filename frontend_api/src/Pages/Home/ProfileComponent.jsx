import { useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './DashboardPage.module.css';

export default function ProfilePanel({ onClose }) {
  const { user, logout } = useAuth();

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  const formatDate = (dateString) => {
    if (!dateString) return 'Не активна';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
  };

  return (
    <div className={`${styles.profilePanel} ${styles.visible}`}>
      <div className={styles.profileHeader}>
        <button onClick={onClose} className={styles.closeButton}>
          &times;
        </button>
      </div>

      <div className={styles.profileContent}>
        <div className={styles.avatarPlaceholder}>
          {user?.login?.charAt(0).toUpperCase() || 'Г'}
        </div>
        
        <div className={styles.userInfo}>
          <h3>{user?.login || 'Гость'}</h3>
          <p>{user?.email || 'Не указан'}</p>
        </div>

        <div className={styles.subscriptionStatus}>
          <h4>Подписка</h4>
          <p className={user?.subscription_active ? styles.active : styles.inactive}>
            {user?.subscription_active 
              ? `Активна до: ${formatDate(user?.subscription_expiry)}` 
              : 'Не активна'}
          </p>
        </div>

        <div className={styles.profileActions}>
          <button 
            className={styles.subscribeButton}
            onClick={() => console.log('Переход к оплате')}
          >
            {user?.subscription_active ? 'Продлить' : 'Оформить подписку'}
          </button>
          
          <button 
            className={styles.logoutButton}
            onClick={logout}
          >
            Выйти
          </button>
        </div>
      </div>
    </div>
  );
}