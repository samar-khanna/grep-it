import React, { Component } from 'react';

import './styles/general.css';
import styles from './styles/App.module.css';
import Result from './components/Result';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      textInputFocused: false,
      text: "",
      code: "",
      results: undefined
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
      .then(results => { console.log(results); this.setState({ results: results }) });
  }

  render() {
    let borderStyle = this.state.textInputFocused ? { border: "2px solid var(--green)" } : {}
    let results = []
    console.log("Results", this.state.results)
    if (this.state.results !== undefined)
      results = this.state.results["result"].map(item => <Result {...item} />)
    console.log("Results DIV", results)
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
          <div> {results} </div>
        </div>
      </div>
    );
  }
}

export default App;
