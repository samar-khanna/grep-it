import { Component } from "react";
import ReactDOM from 'react-dom';
import styles from '../styles/Result.module.css';

class Result extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    console.log("SHHHHHHOOOO")
    if (this.props.type == "so") {
      console.log("SOOOO")
      return (
        <div className={styles.container}>
          <div className={styles.questionContainer}>
            <div className="bold">Question:&nbsp;</div>
            <a href={this.props.url}>{this.props.title}</a>
          </div>
          <div className={styles.answerContainer}>
            <div className="bold">Answer:</div>
            <div
              className={styles.answer}
              dangerouslySetInnerHTML={{
                __html: this.props.answer
              }}
            />
          </div>
        </div>
      )
    }
    else {
      return (
        <div className={styles.container}>
          <div className={styles.questionContainer}>
            <div className="bold">Repo:&nbsp;</div>
            <a href={this.props.repo_link}>{this.props.repo_name}</a>
          </div>
          <div className={styles.answerContainer}>
            <div className="bold"><a href={this.props.raw_file}>{this.props.filepath}</a></div>
          </div>
        </div>
      )
    }
  }
}

export default Result;