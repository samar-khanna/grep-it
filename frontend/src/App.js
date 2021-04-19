import React, { Component } from 'react';

import './styles/general.css';
import styles from './styles/App.module.css';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      textInputFocused: false,
      textVal: "",
      codeVal: "",
    }
  }

  onTextInputBlur = () => {
    this.setState({ textInputFocused: false })
  }

  onTextInputFocus = () => {
    this.setState({ textInputFocused: true })
  }

  onTextChange = (e) => {
    this.setState({ textVal: e.target.value })
  }

  onCodeChange = (e) => {
    this.setState({ codeVal: e.target.value })
  }

  onSubmit = () => {
    let params = new URLSearchParams();
    params.append("search", this.state.textVal);

    console.log(`https://grep-it.herokuapp.com/search?${params.toString()}`)

    const req = new Request(`https://grep-it.herokuapp.com/search?${params.toString()}`, {
      method: "GET",
      mode: "no-cors",
      headers: { "Access-Control-Allow-Origin": "*" }
    });

    fetch(req)
      .then(res => {
        console.log(res)
        return res.json()
      })
      .then(
        (result) => {
          console.log('No error')
          console.log(result)
        },
        (error) => {
          console.log('Error')
          console.log(error)
        }
      )
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
          <textarea
            className={styles.codeInput}
            onChange={this.onCodeChange}
          />
          <div className={styles.buttonContainer}>
            <input
              type="Submit"
              className={styles.button}
              onClick={this.onSubmit}
              value="Submit"
            />
            <div className={styles.buttonShadow} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
