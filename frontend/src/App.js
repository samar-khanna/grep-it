import React, { Component } from "react";

import "./styles/general.css";
import styles from "./styles/App.module.css";
import Result from "./components/Result";
import queries from "./constants/Queries";
import animation from "./animation/grepit-crypto-jumper.svg";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      textInputFocused: false,
      text: "",
      code: "",
      soResults: undefined,
      ghResults: undefined,
      tab: "so",
    };
    this.tabContainer = React.createRef();
    this.textareaRef = React.createRef();
    this.cursorPosition = 0;
    // this.query_idx = Math.floor(Math.random() * queries.length);
    this.query_idx = 0;
  }

  onTextInputBlur = (e) => {
    this.setState({ textInputFocused: false });
  };

  onTextInputFocus = (e) => {
    this.setState({ textInputFocused: true });
  };

  onTextChange = (e) => {
    this.setState({ text: e.target.value });
  };

  onCodeChange = (e) => {
    this.setState({ code: e.target.value });
  };

  onSubmit = (e) => {
    fetch("/search", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        query: this.state.text,
        query_code: this.state.code,
        function: "cosine",
        count: 5,
        input_type: "both",
      }),
    })
      .then((response) => response.json())
      .then((results) => {
        this.setState({ soResults: results.so, ghResults: results.gh });
        this.tabContainer.current.scrollIntoView(true);
      });
  };

  onShuffle = (e) => {
    this.query_idx = (this.query_idx + 1) % queries.length;
    this.setState({
      text: queries[this.query_idx]["text"],
      code: queries[this.query_idx]["code"],
    });
    fetch("/search", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        query: queries[this.query_idx]["text"],
        query_code: queries[this.query_idx]["code"],
        function: "cosine",
        count: 5,
        input_type: "both",
      }),
    })
      .then((response) => response.json())
      .then((results) => {
        this.setState({ soResults: results.so, ghResults: results.gh });
        this.tabContainer.current.scrollIntoView(true);
      });
  };

  onKeyDown = (event) => {
    if (event.keyCode === 9) {
      // tab was pressed
      event.preventDefault();
      var val = this.state.code,
        start = event.target.selectionStart,
        end = event.target.selectionEnd;
      this.setState(
        {
          code: val.substring(0, start) + "\t" + val.substring(end),
        },
        () => {
          this.textareaRef.current.selectionStart = this.textareaRef.current.selectionEnd =
            start + 1;
        }
      );
    }
  };

  render() {
    let borderStyle = this.state.textInputFocused
      ? { border: "2px solid var(--green)" }
      : {};
    let rows;
    if (this.state.results === undefined) {
      rows = 10;
    } else {
      rows = 4;
    }
    let results = [];
    let toBeMapped = this.state.tab === "so" ? this.state.soResults : this.state.ghResults;
    if (toBeMapped !== undefined) {
      results = toBeMapped.map((item, index) => {
        return (
          <Result key={index} {...item} type={this.state.tab} />
        )
      });
    }

    return (
      <div className={styles.container}>
        <div className={styles.centralCol}>
          <div className={styles.titleContainer}>
            <div className={styles.title}>Grep It</div>
            <div className={styles.animationContainer}>
              <object type="image/svg+xml" data={animation} className={styles.animation}>svg-animation</object>
            </div>
          </div>
          <div style={borderStyle} className={styles.textInputContainer}>
            <input
              type="text"
              value={this.state.text}
              className={styles.textInput}
              onBlur={this.onTextInputBlur}
              onFocus={this.onTextInputFocus}
              onChange={this.onTextChange}
              placeholder="Search a Rust inquiry"
            />
          </div>
          <textarea
            ref={this.textareaRef}
            className={styles.codeInput}
            onChange={this.onCodeChange}
            value={this.state.code}
            rows={rows}
            onKeyDown={this.onKeyDown}
            placeholder="Add relevant code to strengthen your search! (optional)"
          />
          <div className={styles.buttonContainer}>
            <input
              type="Submit"
              className={styles.button}
              value="Submit"
              onClick={this.onSubmit}
            />
            <div className={styles.buttonShadow} />
          </div>
          <div className={styles.buttonContainer}>
            <input
              type="Submit"
              className={styles.button}
              style={{ backgroundColor: "var(--blue)" }}
              value="Surprise Me!"
              onClick={this.onShuffle}
            />
            <div
              className={styles.buttonShadow}
              style={{ backgroundColor: "var(--dark-blue)" }}
            />
          </div>
          <div ref={this.tabContainer} id="tabContainer" className={styles.tabContainer}>
            <div
              onClick={() => this.setState({ tab: "so" })}
              style={ this.state.tab === "so" ? { borderBottom: "2px solid var(--black)", color: "var(--black)", top: "1px" } : {} }
            >
              Stack Overflow
            </div>
            <div
              onClick={() => this.setState({ tab: "gh" })}
              style={ this.state.tab === "gh" ? { borderBottom: "2px solid var(--black)", color: "var(--black)", top: "1px" } : {} }
            >
              GitHub
            </div>
          </div>
          <div className={styles.resultsContainer} > {results} </div>
        </div>
      </div>
    );
  }
}

export default App;