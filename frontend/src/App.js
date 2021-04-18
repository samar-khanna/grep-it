import './styles/general.css';
import styles from './styles/App.module.css';

function App() {
  return (
    <div className={styles.container}>
      <div className={styles.centralCol}>
        <div className={styles.logo}></div>
        <div className={styles.title}>Grep It</div>
        <div className={styles.textInputContainer}>
          <input type="search" placeholder="How to add async..."/>
        </div>
        <div className={styles.codeInputContainer}></div>
        <div className={styles.buttonContainer}></div>
      </div>
    </div>
  );
}

export default App;
