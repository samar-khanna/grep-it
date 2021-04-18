import React, { Component } from 'react';

import './styles/general.css';
import styles from './styles/App.module.css';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      textInputFocused: false
    }
  }

  onTextInputBlur = (e) => {
    this.setState({ textInputFocused: false })
  }

  onTextInputFocus = (e) => {
    this.setState({ textInputFocused: true })
  }

  render() {
    let borderStyle = this.state.textInputFocused ? { border: "2px solid var(--green)" } : {}
    return (
      <div className={styles.container}>
        <div className={styles.centralCol}>
          <div className={styles.logo}></div>
          <div className={styles.title}>Grep It</div>
          <div style={borderStyle} className={styles.textInputContainer}>
            <input
              type="text"
              className={styles.textInput}
              onBlur={this.onTextInputBlur}
              onFocus={this.onTextInputFocus}
              placeholder="How to add async..."
            />
          </div>
          <textarea className={styles.codeInput} />
          <div className={styles.buttonContainer}>
            <input type="Submit" className={styles.button} value="Submit" />
            <div className={styles.buttonShadow} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
