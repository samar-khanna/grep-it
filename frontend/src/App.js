import React, { Component } from 'react';

import './styles/general.css';
import styles from './styles/App.module.css';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      textInputFocused: false,
      text: "",
      code: ""
    }
  }

  onTextInputBlur = (e) => {
    this.setState({ textInputFocused: false })
  }

  onTextInputFocus = (e) => {
    this.setState({ textInputFocused: true })
  }

  onTextChange = (e) => {
    this.setState({ text: e.target.value })
  }

  onCodeChange = (e) => {
    this.setState({ code: e.target.value })
  }

  onSubmit = (e) => {
    fetch('/search',
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({
          query: this.state.text,
          query_code: this.state.code,
          function: 'cosine',
          input_type: 'both'
        })
      }
    )
      .then(response => response.json())
      .then(data => console.log(data));
  }

  render() {
    let borderStyle = this.state.textInputFocused ? { border: "2px solid var(--green)" } : {}
    return (
      <div className={styles.container}>
        <div className={styles.centralCol}>
          <div className={styles.title}>Grep It</div>
          <div style={borderStyle} className={styles.textInputContainer}>
            <input
              type="text"
              className={styles.textInput}
              onBlur={this.onTextInputBlur}
              onFocus={this.onTextInputFocus}
              onChange={this.onTextChange}
              placeholder="How to add async..."
            />
          </div>
          <textarea className={styles.codeInput} onChange={this.onCodeChange} />
          <div className={styles.buttonContainer}>
            <input type="Submit" className={styles.button} value="Submit" onClick={this.onSubmit} />
            <div className={styles.buttonShadow} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
